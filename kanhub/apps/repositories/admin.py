import django.contrib.admin
import django.core.exceptions

from apps.repositories.models import Commit, Redirect, Repositorion, Tag, Task


@django.contrib.admin.register(Repositorion)
class RepositorionAdmin(django.contrib.admin.ModelAdmin):
    list_display = (
        Repositorion.name.field.name,
        Repositorion.is_published.field.name,
    )
    list_editable = (Repositorion.is_published.field.name,)
    list_display_links = (Repositorion.name.field.name,)
    filter_horizontal = (Repositorion.users.field.name,)
    readonly_fields = (
        Repositorion.created_at.field.name,
        Repositorion.updated_at.field.name,
    )


@django.contrib.admin.register(Task)
class TaskAdmin(django.contrib.admin.ModelAdmin):
    list_display = (
        Task.name.field.name,
        Task.text.field.name,
        Task.start_at.field.name,
        Task.end_at.field.name,
    )
    filter_horizontal = (Task.tags.field.name,)
    list_display_links = (Task.name.field.name,)


@django.contrib.admin.register(Commit)
class CommitAdmin(django.contrib.admin.ModelAdmin):
    list_display = (Commit.name.field.name,)
    list_display_links = (Task.name.field.name,)
    readonly_fields = (Repositorion.created_at.field.name,)


@django.contrib.admin.register(Redirect)
class RedirectAdmin(django.contrib.admin.ModelAdmin):
    list_display = (Redirect.link.field.name,)


@django.contrib.admin.register(Tag)
class TagAdmin(django.contrib.admin.ModelAdmin):
    list_display = (Tag.name.field.name,)


__all__ = ()
