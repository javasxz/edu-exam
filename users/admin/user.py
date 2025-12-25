from django.contrib import admin
from users.models import User, UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = "Profile"


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'is_staff', 'is_active')
    inlines = (UserProfileInline,)
