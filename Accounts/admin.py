from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUserModel, UserProfile


class CustomUserAdmin(UserAdmin):
    """
    Custom admin for the CustomUser model
    """
    model = CustomUserModel
    list_display = ('email', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_active', 'date_joined')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

# class CustomUserProfileAdmin(admin.ModelAdmin):
#     models = Profile
#     list_display = ('user_first_name', 'user_last_name', 'profileImaqge')
#     list_filter = ('user_first_name', 'user_last_name',)

#     ordering = ('user__email',)


admin.site.register(CustomUserModel, CustomUserAdmin)
# admin.site.register(Profile, CustomUserProfileAdmin)
admin.site.register(UserProfile)
