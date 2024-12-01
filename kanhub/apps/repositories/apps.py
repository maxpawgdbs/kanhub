__all__ = ()
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class RepositoriesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.repositories"
    verbose_name = _("repositories")
