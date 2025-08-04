# users/urls.py

from django.urls import path
from .views import RegisterView, TestEmailView, VerifyEmailView, LoginView, LogoutView, UserProfileView, InviteMemberView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('test-email/', TestEmailView.as_view(), name='test-email'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify-email'),
    path('login/',        LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', UserProfileView.as_view(), name='user-profile'), 
    path('invite/', InviteMemberView.as_view(), name='invite-member'),
]
