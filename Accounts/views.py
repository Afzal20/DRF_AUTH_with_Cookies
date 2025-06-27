from django.shortcuts import render
from rest_framework.response import Response
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from Accounts.serializers import (
    UserLoginSerializer,
    UserProfileSerializer,
    UserRegistratioinSerializer,
    EmptySerializer
)

from rest_framework_simplejwt.views import TokenVerifyView
from rest_framework import permissions
from rest_framework import generics, status
from Accounts.models import CustomUserModel, UserProfile

# create a custom user login view and save the login credentials in cookies
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


@method_decorator(csrf_exempt, name='dispatch')
class UserRegistrationView(generics.CreateAPIView):
    """
    View to handle user registration.
    """
    serializer_class = UserRegistratioinSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'message': 'User registered successfully',
            'user': {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            }
        }, status=status.HTTP_201_CREATED)


@method_decorator(csrf_exempt, name='dispatch')
class UserLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        request_body=UserLoginSerializer,
        responses={
            200: openapi.Response(
                description="Login successful",
                examples={
                    "application/json": {
                        "message": "Login successful",
                        "user": {
                            "id": 1,
                            "email": "user@example.com",
                            "first_name": "John",
                            "last_name": "Doe"
                        }
                    }
                }
            ),
            400: "Invalid credentials"
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token

        response = Response({
            'message': 'Login successful',
            'user': {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            }
        }, status=status.HTTP_200_OK)

        # Set tokens in HTTP-only cookies
        response.set_cookie(
            key='access_token',
            value=str(access_token),
            httponly=True,
            secure=True,
            samesite='None',
            path='/',
        )

        response.set_cookie(
            key='refresh_token',
            value=str(refresh),
            httponly=True,
            secure=True,
            samesite='None',
            path='/',
        )

        return response

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile

    # get is for retrieving the user profile
    def get(self, request, *args, **kwargs):
        profile = self.get_object()
        serializer = self.get_serializer(profile)
        return Response(serializer.data)

    # put is for updating the user profile
    def put(self, request, *args, **kwargs):
        profile = self.get_object()
        serializer = self.get_serializer(profile, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class CustomTokenRefreshView(TokenRefreshView):
    """
    Reads refresh token from HTTP-only cookie, refreshes access and refresh tokens,
    and sets them back as cookies in the response.
    """
    def post(self, request, *args, **kwargs):
        # Try to get refresh token from cookie
        refresh_token = request.COOKIES.get('refresh_token')

        if not refresh_token:
            return Response({'detail': 'Refresh token not provided.'}, status=status.HTTP_401_UNAUTHORIZED)

        # Create data dict for serializer
        data = {'refresh': refresh_token}

        serializer = self.get_serializer(data=data)

        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response({'detail': 'Invalid or expired refresh token.'}, status=status.HTTP_401_UNAUTHORIZED)

        access_token = serializer.validated_data.get('access')
        new_refresh_token = serializer.validated_data.get('refresh', refresh_token)  # use new if provided

        response = Response({'detail': 'Token refreshed successfully'})

        # Set tokens in HTTP-only cookies
        response.set_cookie(
            key='access_token',
            value=access_token,
            httponly=True,
            secure=True,  # Only over HTTPS in production
            samesite='Lax',
            max_age=60 * 5,  # adjust to match your access token lifetime
        )

        response.set_cookie(
            key='refresh_token',
            value=new_refresh_token,
            httponly=True,
            secure=True,
            samesite='Lax',
            max_age=60 * 60 * 24 * 7,  # adjust to match your refresh token lifetime
        )

        return response
    
class CustomTokenVerifyView(TokenVerifyView):
    """
    it should read tokens from HTTP-only cookies and verify them.
    If the token is valid, it returns a success response
    """
    def post(self, request, *args, **kwargs):
        access_token = request.COOKIES.get('access_token')

        if not access_token:
            return Response({'detail': 'Access token not provided.'}, status=status.HTTP_401_UNAUTHORIZED)

        data = {'token': access_token}
        serializer = self.get_serializer(data=data)

        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response({'detail': 'Invalid or expired access token.'}, status=status.HTTP_401_UNAUTHORIZED)

        return Response({'detail': 'token_is_valid'}, status=status.HTTP_200_OK)
    

class LogoutView(APIView):
    """
    View to handle user logout. it should delete the access and refresh tokens from cookies.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):

        response = Response({'detail': 'Logged out successfully'}, status=status.HTTP_200_OK)
        # Clear cookies
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')

        return response