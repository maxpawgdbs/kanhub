__all__ = ()
import django.contrib.admin
import django.core.exceptions

from apps.repositories.models import Commit, Repository, Tag, Task


@django.contrib.admin.register(Repository)
class RepositoryAdmin(django.contrib.admin.ModelAdmin):
    list_display = (
        Repository.name.field.name,
        Repository.is_published.field.name,
    )
    list_editable = (Repository.is_published.field.name,)
    list_display_links = (Repository.name.field.name,)
    filter_horizontal = (Repository.users.field.name,)
    readonly_fields = (
        Repository.created_at.field.name,
        Repository.updated_at.field.name,
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
    list_display = (
        Commit.name.field.name,
        Commit.repository.field.name,
    )
    list_display_links = (Commit.name.field.name,)
    readonly_fields = (Commit.created_at.field.name,)


@django.contrib.admin.register(Tag)
class TagAdmin(django.contrib.admin.ModelAdmin):
    list_display = (Tag.name.field.name,)
