from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User, UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = "Profile"


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ('id', 'email', 'is_staff', 'is_active')
    inlines = (UserProfileInline,)
    fieldsets = (
        
        (
            'Personal info',
            {
                'fields': ('display_name', 'email', 'phone_number'),
            },
        ),
        (
            'Permissions',
            {
                'fields': (
                    ('is_active', 'is_staff', 'is_superuser'),
                    ('groups', 'user_permissions'),
                ),
            },
        ),
        (
            'Important dates',
            {
                'fields': ('last_login', 'date_joined'),
            },
        ),
    )
    add_fieldsets = ((
        None,
        {
            'fields': ('display_name', 'email', 'password1', 'password2'),
        },
    ),)
    ordering = ('-date_joined',)
