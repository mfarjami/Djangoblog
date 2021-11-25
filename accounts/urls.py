from django.urls import path, include, re_path
from django.contrib.auth import views as auth_views 
from . import views

app_name = 'accounts'

urlpatterns = [
    path('profile_edit/<str:username>/', views.UserEditProfileView.as_view(), name='profile_edit'),
    path('profile/<int:user_id>/', views.UserProfileView.as_view(), name='profile'),
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', views.activate, name='activate'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('phone_login/', views.PhoneLoginView.as_view(), name='phone_login'),
    path('verify/', views.verify_code, name='verify'),
    path('password_change/', views.PasswordChangeView.as_view(), name='password_change'),
    path('', include('django.contrib.auth.urls')),
]