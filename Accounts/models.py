from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

class CustomUserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        
        if not email: 
            raise ValueError("email is requird")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True) 
        extra_fields.setdefault('is_active', True) 
        extra_fields.setdefault('is_staff', True)  

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('superuser must be is_superuser = True ')

        if extra_fields.get('is_active') is not True:
            raise ValueError('superuser must be active ')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('superuser must be staffuser')

        return self.create_user(email, password, **extra_fields)
    
class CustomUserModel(AbstractUser):

    email = models.EmailField(_('email addresh'), unique=True)
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    upozila = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='ProfileImage/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email}"

@receiver(post_save, sender=CustomUserModel)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=CustomUserModel)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()