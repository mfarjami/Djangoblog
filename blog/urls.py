from django.urls import path
from . import views
from . import bucket_views

app_name = 'blog'


urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('post/<int:pk>/', views.PostDetail.as_view(), name='post_detail'),
    path('post_create/', views.PostCreate.as_view(), name='post_create'),
    path('post_update/<int:post_id>/', views.PostUpdate.as_view(), name='post_update'),
    path('post_delete/<int:post_id>/', views.PostDelete.as_view(), name='post_delete'),
    path('contact_us/', views.ContactUs.as_view(), name='contact_us'),
    path('share_post/<int:post_id>/', views.SharePostView.as_view(), name='share_post'),
    path('add_reply/<int:post_id>/<int:comment_id>/', views.AddReplyView.as_view(), name='add_reply'),
    path('bucket/', bucket_views.BucketHome.as_view(), name='bucket_home'),
]