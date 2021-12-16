from django.test import TestCase, SimpleTestCase
from blog.forms import PostCreateForm, ContactUsForm, SharePostForm
from django.core import mail
from django.core.files.uploadedfile import SimpleUploadedFile



class TestPostCreateForm(SimpleTestCase):
    def test_post_create_form_is_valid(self):
        upload_file = open('accounts/avatar/1.jpg', 'rb')
        file_dict = {'image': SimpleUploadedFile(upload_file.name, upload_file.read())}
        form = PostCreateForm(data={
            'title': 'Test Title',
            'body': 'Test Content',
            'snippet': 'Test Snippet',
            'status': True,
        }, files=file_dict)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['title'], 'Test Title')

    def test_post_create_form_is_invalid(self):
        form = PostCreateForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['title'], ['This field is required.'])


class TestContactUsForm(SimpleTestCase):
    def test_contact_us_form_is_valid(self):
        # mail.send_mail('Test name', 'Test Subject', ['Testemail@yahoo.com'], '09146954245', 'This is a test message', fail_silently=False)
        form = ContactUsForm(data={
            'name': 'Test name',
            'subject': 'Test Subject',
            'email': 'mohammad@email.com',
            'phone': '09146954245',
            'message': 'This is a test message',
        })
        self.assertTrue(form.is_valid())

    def test_contact_us_form_is_invalid(self):
        form = ContactUsForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['name'], ['This field is required.'])


class TestSharePostForm(SimpleTestCase):
    def test_share_post_form_is_valid(self):
        form = SharePostForm(data={
            'name': 'Test name',
            'to': 'mohamma@email.com',
            'message': 'This is a test message',
        })
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['name'], 'Test name')

    def test_share_post_form_is_invalid(self):
        form = SharePostForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['name'], ['This field is required.'])