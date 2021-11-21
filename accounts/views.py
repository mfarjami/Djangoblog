from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import View
from .forms import (EditProfileForm, PhoneLoginForm, UserLoginForm,
                    UserRegistrationForm, VerifyCodeForm)
# from django.contrib.auth import 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
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
            user.save()
            login(request, user)
            messages.success(request, 'You have successfully registered.', 'success')
            return redirect('blog:home')
        else:
            messages.error(request, 'Invalid registration', 'danger')
            return render(request, self.template_name, {'form': form})


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


# def phone_login(request):
#     if request.method == 'POST':
#         form = PhoneLoginForm(request.POST)
#         if form.is_valid():
#             global phone, rand_num
#             phone = f"0{form.cleaned_data['phone']}"
#             rand_num = randint(1000, 9999)
#             sms = ghasedak.Ghasedak('2b293411491d3129662cb353361eaf49b37f45baf693c3ebaae045d9d434a4f2')
#             sms.send({'linenumber':"10008566", 'receptor': phone, 'message':f'{rand_num}'})
#             messages.success(request, 'Verification code sent to your phone', 'success')
#             return redirect('accounts:verify')
#     else:
#         form = PhoneLoginForm()
#     return render(request, 'accounts/phone_login.html', {'form':form})


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




# class VerifyCodeView(View):
#     form_class = VerifyCodeForm
#     template_name = 'accounts/verify_code.html'

#     def get(self, request):
#         form = self.form_class
#         return render(request, self.template_name, {'form':form})

#     def post(self, request):
#         form = self.form_class(request.POST)
#         if form.is_valid():
#             if rand_num == form.cleaned_data['code']:
#                 profile = get_object_or_404(Profile, phone=phone)
#                 user = get_object_or_404(User, profile__id=profile.id)
#                 login(request, user)
#                 messages.success(request, 'Verification code is correct', 'success')
#                 return redirect('blog:home')
#             else:
#                 messages.error(request, 'Verification code is incorrect', 'warning')
#         else:
#             return render(request, self.template_name, {'form':form})
            
