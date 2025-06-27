from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import UserProfile
from django.contrib.auth import authenticate

User = get_user_model()

# create a custom user serializer for user registration
class UserRegistratioinSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    

# create a custom user serializer for user login
class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)
        user = authenticate(email=email, password=password)
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password is not found.'
            )

        return {
            'user': user,
        }


# create a custom user profile serializer
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at')


class EmptySerializer(serializers.Serializer):
    """
    An empty serializer that can be used for testing purposes.
    """
    pass