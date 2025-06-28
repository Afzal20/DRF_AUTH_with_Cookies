from django.urls import path


from .views import CustomTokenRefreshView, CustomTokenVerifyView, LogoutView, OTPVerificationAPIView, PasswordResetAPIView, PasswordResetRequestAPIView, UserLoginView, UserProfileView, UserRegistrationView

urlpatterns = [
    path('user/register/', UserRegistrationView.as_view(), name='user_register'),
    path('user/login/', UserLoginView.as_view(), name='user_login'),
    path('user/profile/', UserProfileView.as_view(), name='user_profile'),
    path("password-reset/request/", PasswordResetRequestAPIView.as_view(), name="password-reset-request"),
    path("password-reset/verify-otp/", OTPVerificationAPIView.as_view(), name="password-reset-verify-otp"), 
    path("password-reset/change-password/", PasswordResetAPIView.as_view(), name="password-reset-change"),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', CustomTokenVerifyView.as_view(), name='token_verify'),
    path('logout/', LogoutView.as_view(), name='user_logout'),
]