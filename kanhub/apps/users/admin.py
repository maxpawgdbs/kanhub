import django.contrib
import django.contrib.auth.admin
import django.contrib.auth.models

import apps.users.models


class ProfileInline(django.contrib.admin.TabularInline):
    model = apps.users.models.Profile
    can_delete = False
    readonly_fields = [
        apps.users.models.Profile.image.field.name,
    ]


class UserAdmin(django.contrib.auth.admin.UserAdmin):
    inlines = (ProfileInline,)


__all__ = ()
