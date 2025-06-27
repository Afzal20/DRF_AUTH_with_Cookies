from django.urls import path


from .views import CustomTokenRefreshView, CustomTokenVerifyView, LogoutView, UserLoginView, UserProfileView, UserRegistrationView

urlpatterns = [
    path('user/register/', UserRegistrationView.as_view(), name='user_register'),
    path('user/login/', UserLoginView.as_view(), name='user_login'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', CustomTokenVerifyView.as_view(), name='token_verify'),
    path('user/profile/', UserProfileView.as_view(), name='user_profile'),
    path('logout/', LogoutView.as_view(), name='user_logout'),
]