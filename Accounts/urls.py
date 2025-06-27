from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from rest_framework_simplejwt.views import TokenVerifyView
from .views import UserLoginView, UserProfileView, UserRegistrationView

urlpatterns = [
    path('user/register/', UserRegistrationView.as_view(), name='user_register'),
    path('user/login/', UserLoginView.as_view(), name='user_login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('user/profile/', UserProfileView.as_view(), name='user_profile'),
]