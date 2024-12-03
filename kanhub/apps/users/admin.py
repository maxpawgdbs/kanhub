import django.contrib
import django.contrib.auth.admin
import django.contrib.auth.models

from apps.users.models import Profile


class ProfileInline(django.contrib.admin.TabularInline):
    model = Profile
    can_delete = False
    readonly_fields = [
        Profile.image.field.name,
    ]


class UserAdmin(django.contrib.auth.admin.UserAdmin):
    inlines = (ProfileInline,)


__all__ = ()
