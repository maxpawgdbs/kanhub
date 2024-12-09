import django.contrib.admin
import django.core.exceptions

import apps.repositories.models


@django.contrib.admin.register(apps.repositories.models.Repository)
class RepositoryAdmin(django.contrib.admin.ModelAdmin):
    list_display = (
        apps.repositories.models.Repository.name.field.name,
        apps.repositories.models.Repository.is_published.field.name,
    )
    list_editable = (
        apps.repositories.models.Repository.is_published.field.name,
    )
    list_display_links = (apps.repositories.models.Repository.name.field.name,)
    filter_horizontal = (apps.repositories.models.Repository.users.field.name,)
    readonly_fields = (
        apps.repositories.models.Repository.created_at.field.name,
        apps.repositories.models.Repository.updated_at.field.name,
    )


@django.contrib.admin.register(apps.repositories.models.Task)
class TaskAdmin(django.contrib.admin.ModelAdmin):
    list_display = (
        apps.repositories.models.Task.name.field.name,
        apps.repositories.models.Task.text.field.name,
        apps.repositories.models.Task.start_at.field.name,
        apps.repositories.models.Task.end_at.field.name,
    )
    filter_horizontal = (apps.repositories.models.Task.tags.field.name,)
    list_display_links = (apps.repositories.models.Task.name.field.name,)


@django.contrib.admin.register(apps.repositories.models.Commit)
class CommitAdmin(django.contrib.admin.ModelAdmin):
    list_display = (
        apps.repositories.models.Commit.name.field.name,
        apps.repositories.models.Commit.repository.field.name,
    )
    list_display_links = (apps.repositories.models.Commit.name.field.name,)
    readonly_fields = (apps.repositories.models.Commit.created_at.field.name,)


@django.contrib.admin.register(apps.repositories.models.Redirect)
class RedirectAdmin(django.contrib.admin.ModelAdmin):
    list_display = (apps.repositories.models.Redirect.link.field.name,)


@django.contrib.admin.register(apps.repositories.models.Tag)
class TagAdmin(django.contrib.admin.ModelAdmin):
    list_display = (apps.repositories.models.Tag.name.field.name,)


__all__ = ()
