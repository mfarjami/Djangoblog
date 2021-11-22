from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import View
from .forms import (EditProfileForm, PhoneLoginForm, UserLoginForm,
                    UserRegistrationForm, VerifyCodeForm)
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.http import HttpResponse
from django.core.mail import EmailMessage, send_mail
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from .models import User, Profile
import ghasedak
from random import randint
# Create your views here.

class UserLoginView(View):
    form_class = UserLoginForm
    template_name = 'accounts/login.html'

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'You have successfully logged in.', 'success')
                return redirect('blog:home')
            else:
                messages.error(request, 'Invalid login', 'danger')
                return redirect('accounts:login')


class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, 'You have successfully logged out.', 'success')
        return redirect('blog:home')

    
class UserRegisterView(View):
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.create_user(cd['username'], cd['email'], cd['full_name'], cd['password'])
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('accounts/activate_account.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration.')
        else:
            messages.error(request, 'Invalid registration', 'danger')
            return render(request, self.template_name, {'form': form})


def activate(request, uidb64, token):
    """ uidb64 is the user id in base64 format and token is the token generated by the function account_activation_token.make_token in accounts/tokens.py file """
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Invalid activation link Please try <a href="/accounts/register">register</a>!')


class UserProfileView(LoginRequiredMixin, View):
    template_name = 'accounts/profile.html'

    def get(self, request, user_id):
        form = get_object_or_404(Profile, user=user_id)
        self_profile = False
        if request.user.is_admin or request.user.id == user_id:
            self_profile = True
        return render(request, self.template_name, {'form': form, 'self_profile': self_profile})


class UserEditProfileView(LoginRequiredMixin, View):
    """Edited a user profile  """
    form_class = EditProfileForm
    template_name = 'accounts/profile_edit.html'

    def get(self, request, username): # username is passed as kwargs
        if request.user.is_admin or request.user.username == username:
            form = self.form_class(instance=request.user.profile)
            user = get_object_or_404(User, username=username)
            return render(request, self.template_name, {'form':form, 'user':user}) 
        else:
            return redirect('blog:home')

    def post(self, request, *args, **kwargs): 
        if request.user.is_admin or request.user.username == kwargs['username']:
            form = self.form_class(request.POST, request.FILES, instance=request.user.profile)
            if form.is_valid():
                form.save()
                messages.success(request, 'Profile updated successfully', 'success')
                return redirect('accounts:profile', request.user.id)
            else:
                messages.error(request, 'Profile update failed', 'danger')
                return render(request, self.template_name, { 'form':form})
        else:
            return redirect('blog:home')


class PhoneLoginView(View):
    form_class = PhoneLoginForm
    template_name = 'accounts/phone_login.html'

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form':form})
        
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            global rand_num, phone
            phone = f"0{form.cleaned_data['phone']}"
            rand_num = randint(1000, 9999)
            sms = ghasedak.Ghasedak('2b293411491d3129662cb353361eaf49b37f45baf693c3ebaae045d9d434a4f2')
            sms.send({'linenumber':"10008566", 'receptor': phone, 'message':f'{rand_num}'})
            messages.success(request, 'Verification code sent to your phone', 'success')
            return redirect('accounts:verify')
        else:
            messages.error(request, 'Invalid phone number', 'danger')
            return render(request, self.template_name, {'form':form})


def verify_code(request):
    if request.method == 'POST':
        form = VerifyCodeForm(request.POST)
        if form.is_valid():
            if rand_num == form.cleaned_data['code']:
                profile = get_object_or_404(Profile, phone=phone)
                user = get_object_or_404(User, profile__id=profile.id)
                login(request, user)
                messages.success(request, 'Verification code is correct', 'success')
                return redirect('blog:home')
            else:
                messages.error(request, 'Verification code is incorrect', 'warning')
    else:
        form = VerifyCodeForm()
    return render(request, 'accounts/verify_code.html', {'form':form})


class PasswordChangeView(LoginRequiredMixin, View):
    form_class = PasswordChangeForm
    template_name = 'accounts/password_change.html'

    def get(self, request):
        form = self.form_class(request.user.id)
        return render(request, self.template_name, {'form':form})

    def post(self, request):
        form = self.form_class(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Password changed successfully', 'success')
            return redirect('blog:home')
        else:
            messages.error(request, 'Password change failed', 'danger')
            return render(request, self.template_name, {'form':form})
