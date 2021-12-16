from django.test import SimpleTestCase
from django.urls import reverse, resolve
from accounts.views import *

# UserProfileView
# UserEditProfileView
# UserRegisterView
# UserLoginView
# UserLogoutView
# PhoneLoginView
# verify_code
# PasswordChangeView

class TestUrls(SimpleTestCase):

    def test_profile_url(self):
        url = reverse('accounts:profile', args=[1])
        self.assertEqual(resolve(url).func.view_class, UserProfileView)

    def test_edit_profile_url(self):
        url = reverse('accounts:profile_edit', args=['mohammad'])
        self.assertEqual(resolve(url).func.view_class, UserEditProfileView)

    def test_register_url(self):
        url = reverse('accounts:register')
        self.assertEqual(resolve(url).func.view_class, UserRegisterView)

    def test_login_url(self):
        url = reverse('accounts:login')
        self.assertEqual(resolve(url).func.view_class, UserLoginView)

    def test_logout_url(self):
        url = reverse('accounts:logout')
        self.assertEqual(resolve(url).func.view_class, UserLogoutView)

    def test_phone_login_url(self):
        url = reverse('accounts:phone_login')
        self.assertEqual(resolve(url).func.view_class, PhoneLoginView)

    def test_verify_code_url(self):
        url = reverse('accounts:verify')
        self.assertEqual(resolve(url).func, verify_code)

    def test_password_change_url(self):
        url = reverse('accounts:password_change')
        self.assertEqual(resolve(url).func.view_class, PasswordChangeView)
    