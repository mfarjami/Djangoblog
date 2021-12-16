from django.test import TestCase, SimpleTestCase
from accounts.forms import UserCreationForm, UserChangeForm, UserLoginForm, UserRegistrationForm, EditProfileForm, PhoneLoginForm, VerifyCodeForm
from django.core.files.uploadedfile import SimpleUploadedFile
from accounts.models import User
from django.urls import reverse


class TestUserCreationForm(TestCase):
    """
    Test the UserCreationForm.
    """
    def test_valid_data(self):
        """
        Test with valid data.
        """
        form = UserCreationForm(data={'username': 'newuser', 'email':'newuser@gmail.com', 'full_name':'newuser mari', 'password1': 'newpass', 'password2': 'newpass'})
        self.assertTrue(form.is_valid())

    def test_invalid_data(self):
        """
        Test with invalid data.
        """
        form = UserCreationForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 4)

    
class TestUserChangeForm(TestCase):
    """
    Test the UserChangeForm.
    """
    def test_valid_data(self):
        """
        Test with valid data.
        """
        form = UserChangeForm(data={'username': 'newuser', 'email':'newuser@gmail.com', 'full_name':'newuser mari', 'password': 'newpass', 'is_active': True, 'is_staff': True,})

    def test_invalid_data(self):
        """
        Test with invalid data.
        """
        form = UserChangeForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 3)


class TestUserLoginForm(SimpleTestCase):
    """
    Test the UserLoginForm.
    """
    def test_valid_data(self):
        """
        Test with valid data.
        """
        form = UserLoginForm(data={'username': 'newuser', 'password': 'newpass'})
        self.assertTrue(form.is_valid())

    def test_invalid_data(self):
        """
        Test with invalid data.
        """
        form = UserLoginForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 2)


class TestUserRegistrationForm(TestCase):
    """
    Test the UserRegistrationForm.
    """
    def test_valid_data(self):
        """
        Test with valid data.
        """
        form = UserRegistrationForm(data={'username': 'newuser', 'email':'newuser@email.com', 'full_name':'newuser mari', 'password': 'newpass', 'password2': 'newpass'})
        self.assertTrue(form.is_valid())

    def test_invalid_data(self):
        """
        Test with invalid data.
        """
        form = UserRegistrationForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 5)


class TestEditProfileForm(TestCase):
    """
    Test the EditProfileForm.
    """ 
    def test_valid_data(self):
        upload_file = open('accounts/avatar/1.jpg', 'rb')
        file_dict = {'avatar': SimpleUploadedFile(upload_file.name, upload_file.read())}
        form = EditProfileForm(data={'avatar':file_dict, 'bio': 'new bio', 'phone':'123456789', 'birth_date':'2020-01-01'})
        self.assertTrue(form.is_valid())


class TestPhoneLoginForm(TestCase):
    """
    Test the PhoneLoginForm.
    """
    def test_valid_data(self):
        """
        Test with valid data.
        """
        form = PhoneLoginForm(data={'phone': 12323056755})
        self.assertTrue(form.is_valid())
    
    def test_invalid_data(self):
        """
        Test with invalid data.
        """
        form = PhoneLoginForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)


class TestVerifyCodeForm(TestCase):
    """
    Test the VerifyCodeForm.
    """
    def test_valid_data(self):
        """
        Test with valid data.
        """
        form = VerifyCodeForm(data={'code': '123456'})
        self.assertTrue(form.is_valid())
        self.assertEquals(len(form.errors), 0)

    def test_invalid_data(self):
        """
        Test with invalid data.
        """
        form = VerifyCodeForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)