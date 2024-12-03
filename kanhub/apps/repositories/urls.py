__all__ = ()
import django.urls

import apps.repositories.views

app_name = "repositories"
urlpatterns = [
    django.urls.path("", apps.repositories.views.RepositoryList.as_view(), name="list"),
    django.urls.path("<int:pk>/", apps.repositories.views.RepositoryDetail.as_view(), name="detail"),
    django.urls.path("<int:pk>/tasks/", apps.repositories.views.RepositoryTasks.as_view(), name="tasks"),
    django.urls.path("<int:pk>/materials/", apps.repositories.views.RepositoryMaterials.as_view(), name="materials"),
    django.urls.path("<int:pk>/calendar/", apps.repositories.views.RepositoryCalendar.as_view(), name="calendar"),
    django.urls.path("<int:pk>/settings/", apps.repositories.views.RepositorySettings.as_view(), name="settings"),
]
