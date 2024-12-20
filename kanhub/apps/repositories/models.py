from ckeditor_uploader.fields import RichTextUploadingField
import django.utils.safestring
from django.utils.translation import gettext_lazy as _


class Tag(django.db.models.Model):
    name = django.db.models.CharField(
        verbose_name=_("название"),
        max_length=150,
        null=False,
        unique=True,
        help_text=_("max 150 символов"),
        validators=[
            django.core.validators.MinLengthValidator(2),
        ],
    )
    is_published = django.db.models.BooleanField(
        verbose_name=_("опубликовано"),
        default=True,
    )

    class Meta:
        verbose_name = _("тег")
        verbose_name_plural = _("теги")

    def __str__(self):
        return self.name[:15]


class Repository(django.db.models.Model):
    name = django.db.models.CharField(
        verbose_name=_("название"),
        max_length=150,
        null=False,
        unique=False,
        help_text=_("max 150 символов"),
        validators=[
            django.core.validators.MinLengthValidator(2),
        ],
    )
    is_published = django.db.models.BooleanField(
        verbose_name=_("опубликовано"),
        default=True,
    )
    user = django.db.models.ForeignKey(
        django.conf.settings.AUTH_USER_MODEL,
        verbose_name=_("создатель"),
        on_delete=django.db.models.CASCADE,
        related_name="repositories_owned",
    )
    users = django.db.models.ManyToManyField(
        django.conf.settings.AUTH_USER_MODEL,
        verbose_name=_("пользователи"),
        related_name="repositories_contributed",
        blank=True,
    )
    created_at = django.db.models.DateTimeField(
        auto_now_add=True,
        null=True,
    )
    updated_at = django.db.models.DateTimeField(
        auto_now=True,
        null=True,
    )

    class Meta:
        verbose_name = _("репозиторий")
        verbose_name_plural = _("репозитории")

    def __str__(self):
        return self.name

    def get_statistics(self):
        commits_count = self.commit_set.count()
        tasks_count = self.task_set.count()
        unique_tags_count = (
            Tag.objects.filter(task__commit__repository=self)
            .distinct()
            .count()
        )
        active_users_count = self.users.count()

        return {
            "commits_count": commits_count,
            "tasks_count": tasks_count,
            "unique_tags_count": unique_tags_count,
            "active_users_count": active_users_count,
        }


class Commit(django.db.models.Model):
    name = django.db.models.CharField(
        verbose_name=_("название"),
        max_length=150,
        null=False,
        unique=False,
        help_text=_("max 150 символов"),
        validators=[
            django.core.validators.MinLengthValidator(2),
        ],
    )
    user = django.db.models.ForeignKey(
        django.conf.settings.AUTH_USER_MODEL,
        verbose_name=_("пользователь"),
        on_delete=django.db.models.CASCADE,
    )
    repository = django.db.models.ForeignKey(
        Repository,
        verbose_name=_("репозиторий"),
        on_delete=django.db.models.CASCADE,
    )
    created_at = django.db.models.DateTimeField(
        auto_now_add=True,
        null=True,
    )

    class Meta:
        verbose_name = _("коммит")
        verbose_name_plural = _("коммиты")

    def __str__(self):
        return self.name


class Task(django.db.models.Model):
    name = django.db.models.CharField(
        verbose_name=_("название"),
        max_length=150,
        null=False,
        unique=False,
        help_text=_("max 150 символов"),
        validators=[
            django.core.validators.MinLengthValidator(2),
        ],
    )
    tags = django.db.models.ManyToManyField(
        Tag,
        verbose_name=_("теги"),
    )
    text = RichTextUploadingField(
        verbose_name=_("текст"),
        help_text=_("Вспомогательный текст"),
    )
    start_at = django.db.models.DateField(
        null=True,
    )
    end_at = django.db.models.DateField(
        null=True,
    )
    first_commit = django.db.models.ForeignKey(
        Commit,
        verbose_name=_("первый комит"),
        on_delete=django.db.models.CASCADE,
        related_name="first_commit",
    )
    commit = django.db.models.ForeignKey(
        Commit,
        verbose_name=_("коммит"),
        on_delete=django.db.models.CASCADE,
    )

    class Meta:
        verbose_name = _("задача")
        verbose_name_plural = _("задачи")

    def __str__(self):
        return self.name


__all__ = ()
