__all__ = ()
import django.urls
import django.views.generic

import apps.stats.views


app_name = "stats"
urlpatterns = [
    django.urls.path(
        "<int:pk>/",
        apps.stats.views.RepositoryStatistics.as_view(),
        name="stat",
    ),
]
