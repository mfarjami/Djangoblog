from django.test import SimpleTestCase
from django.urls import reverse, resolve
from blog.views import *

# PostList
# PostDetail
# PostCreate
# PostUpdate
# PostDelete
# ContactUs
# SharePostView


class TestUrls(SimpleTestCase):

    def test_post_list_url_is_resolved(self):
        url = reverse('blog:home')
        self.assertEquals(resolve(url).func.view_class, PostList)

    def test_post_detail_url_is_resolved(self):
        url = reverse('blog:post_detail', args=[1])
        self.assertEquals(resolve(url).func.view_class, PostDetail)

    def test_post_create_url_is_resolved(self):
        url = reverse('blog:post_create')
        self.assertEquals(resolve(url).func.view_class, PostCreate)

    def test_post_update_url_is_resolved(self):
        url = reverse('blog:post_update', args=[1])
        self.assertEquals(resolve(url).func.view_class, PostUpdate)

    def test_post_delete_url_is_resolved(self):
        url = reverse('blog:post_delete', args=[1])
        self.assertEquals(resolve(url).func.view_class, PostDelete)

    def test_contact_url_is_resolved(self):
        url = reverse('blog:contact_us')
        self.assertEquals(resolve(url).func.view_class, ContactUs)


    def test_share_post_url_is_resolved(self):
        url = reverse('blog:share_post', args=[1])
        self.assertEquals(resolve(url).func.view_class, SharePostView)