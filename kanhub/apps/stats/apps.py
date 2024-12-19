__all__ = ()
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class StatsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.stats"
    verbose_name = _("stats")
