from django.urls import path
from . import views

app_name = 'blog'


urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('post/<int:pk>/', views.PostDetail.as_view(), name='post_detail'),
    path('post_create/', views.PostCreate.as_view(), name='post_create'),
    path('post_update/<int:post_id>/', views.PostUpdate.as_view(), name='post_update'),
    path('post_delete/<int:post_id>/', views.PostDelete.as_view(), name='post_delete'),
]