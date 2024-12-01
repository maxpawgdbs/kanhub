import pathlib
import uuid

import django.conf
import django.db.models
import sorl.thumbnail
import django.utils.safestring
from django.utils.translation import gettext_lazy as _


class ProfileManager(django.db.models.Manager):
    def user_detail(self, pk):
        return (
            self.get_queryset()
            .filter(pk=pk)
            .values(
                django.conf.settings.AUTH_USER_MODEL.email.field.name,
                django.conf.settings.AUTH_USER_MODEL.first_name.field.name,
                django.conf.settings.AUTH_USER_MODEL.last_name.field.name,
                Profile.image.field.name,
            )
        )


class Profile(django.db.models.Model):
    def get_upload_file(self, filename):
        ext = filename.split(".")[-1]
        filename = f"{uuid.uuid4()}.{ext}"
        return pathlib.Path("users") / str(self.id) / filename

    objects = ProfileManager()

    user = django.db.models.OneToOneField(
        django.conf.settings.AUTH_USER_MODEL,
        verbose_name=_("пользователь"),
        on_delete=django.db.models.CASCADE,
    )
    image = django.db.models.ImageField(
        verbose_name=_("изображение"),
        upload_to=get_upload_file,
        blank=True,
        null=True,
        help_text=_("Аватарка"),
    )

    class Meta:
        verbose_name = _("дополнительное поле")
        verbose_name_plural = _("дополнительные поля")
        ordering = ("user",)

    def __str__(self):
        return self.user.username

    def get_image_350x350(self):
        return sorl.thumbnail.get_thumbnail(
            self.image,
            "350x350",
            crop="center",
            quality=85,
        )


__all__ = ()
