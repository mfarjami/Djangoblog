from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import User, Profile


class UserCreationForm(forms.ModelForm):
	password1 = forms.CharField(label='password', widget=forms.PasswordInput)
	password2 = forms.CharField(label='confirm password', widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ('email', 'username', 'full_name')

	def clean_password2(self):
		cd = self.cleaned_data
		if cd['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
			raise ValidationError('passwords dont match')
		return cd['password2']

	def save(self, commit=True):
		user = super().save(commit=False)
        # Save the provided password in hashed format
		user.set_password(self.cleaned_data['password1'])
		if commit:
			user.save()
		return user



class UserChangeForm(forms.ModelForm):
    """A form for updating users. """

    password = ReadOnlyPasswordHashField

    class Meta:
        model = User
        fields = ('username', 'email', 'full_name', 'password', 'is_active', 'is_admin')


class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))


class UserRegistrationForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    full_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password confirmation'}))
    
    def clean_password2(self):
        # Check that the two password entries match
        cd = self.cleaned_data
        if cd['password'] and cd['password2'] and cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords must match.')
        return cd['password2']

    # def clean_username(self):
    #     # Check that the username is not already in use
    #     username = self.cleaned_data.get('username')
    #     qs = User.objects.filter(username=username)
    #     if qs.exists():
    #         raise forms.ValidationError("Username is taken.")

    # def clean_email(self):
    #     # Check that the email is not already in use
    #     email = self.cleaned_data.get('email')
    #     qs = User.objects.filter(email=email)
    #     if qs.exists():
    #         raise forms.ValidationError("Email is taken.")


class EditProfileForm(forms.ModelForm):
    """This form updated userprofile"""
    class Meta:
        model = Profile
        # fields = '__all__'
        fields = ('avatar', 'bio', 'phone', 'birthday')


    # def clean_phone(self):
    #     phone = self.cleaned_data['phone']
    #     if Profile.objects.filter(phone=phone).exists():
    #         raise forms.ValidationError('Phone is already registered.')
    #     return phone
        # if len(phone) == 11:
        #     return phone
        # else:
        #     raise forms.ValidationError('Phone number must be 11 digits.')
            

class PhoneLoginForm(forms.Form):
    phone = forms.IntegerField()

    def clean_phone(self):
        phone = Profile.objects.filter(phone=self.cleaned_data.get('phone'))
        if phone.exists():
            raise forms.ValidationError('Phone is already registered.')
        return self.cleaned_data.get('phone')


class VerifyCodeForm(forms.Form):
    code = forms.IntegerField()


