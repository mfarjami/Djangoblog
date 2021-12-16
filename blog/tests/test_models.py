from django.test import TestCase
from accounts.models import User
from blog.models import Post


class TestModel(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='test', full_name='tests', email='mohammad@email.com', password='test')
        self.post = Post.objects.create(title='Test', body='Test', user=user)

    def test_post_create(self):
        self.assertEqual(self.post.snippet, 'test')
 
    