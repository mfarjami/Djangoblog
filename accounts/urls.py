from django.urls import path, include
from . import views

app_name = 'accounts'

urlpatterns = [
    path('profile_edit/<str:username>/', views.UserEditProfileView.as_view(), name='profile_edit'),
    path('profile/<int:user_id>/', views.UserProfileView.as_view(), name='profile'),
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('phone_login/', views.PhoneLoginView.as_view(), name='phone_login'),
    path('verify/', views.verify_code, name='verify'),
]