from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import User, Profile
from django.core import mail
from accounts.forms import UserRegistrationForm, UserChangeForm, UserCreationForm




class TestViews(TestCase):
    """
    Test the views.py file
    """
    def setUp(self):
        """
        Set up the test client
        """
        self.client = Client()

    def test_user_creation_GET(self):
        """
        Test the user creation view
        """
        response = self.client.get(reverse('accounts:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')
        self.failUnless(response.context['form'], UserRegistrationForm)

    def test_user_creation_POST_valid(self):
        response = self.client.post(reverse('accounts:register'), data={
            'username': 'testuser', 'email': 'email@email.com', 'full_name':'testfull', 'password': 'testpass'
        })
        mail.send_mail(
            'subject test', 'test message', 'biroghlam@email.com', ['mohammad@email.com'], fail_silently=False
        )
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(mail.outbox[0].subject, 'subject test')

    def test_user_creation_POST_invalid(self):
        response = self.client.post(reverse('accounts:register'), data={})
        mail.send_mail('', '', '', [], fail_silently=False)
        self.assertEqual(len(mail.outbox), 0)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 0)
        self.assertFormError(response, 'form', 'username', 'This field is required.')

        

