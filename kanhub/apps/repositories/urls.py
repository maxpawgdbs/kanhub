__all__ = ()
import django.urls

import apps.repositories.views

app_name = "repositories"
urlpatterns = [
    django.urls.path(
        "",
        apps.repositories.views.RepositoryList.as_view(),
        name="list",
    ),
    django.urls.path(
        "<int:pk>/",
        apps.repositories.views.RepositoryDetail.as_view(),
        name="detail",
    ),
    django.urls.path(
        "new/",
        apps.repositories.views.RepositoryNew.as_view(),
        name="new",
    ),
    django.urls.path(
        "<int:pk>/tasks/<int:task_pk>/",
        apps.repositories.views.RepositoryTask.as_view(),
        name="task",
    ),
    django.urls.path(
        '<int:pk>/task/<int:task_pk>/edit/',
        apps.repositories.views.EditTaskView.as_view(),
        name='edit_task',
    ),
    django.urls.path(
        "<int:pk>/tasks/",
        apps.repositories.views.RepositoryTasks.as_view(),
        name="tasks",
    ),
    django.urls.path(
        "<int:pk>/history/",
        apps.repositories.views.RepositoryHistory.as_view(),
        name="history",
    ),
    django.urls.path(
        "<int:pk>/calendar/",
        apps.repositories.views.RepositoryCalendar.as_view(),
        name="calendar",
    ),
    django.urls.path(
        "<int:pk>/settings/",
        apps.repositories.views.RepositorySettings.as_view(),
        name="settings",
    ),
    django.urls.path(
        "<int:pk>/task_new/",
        apps.repositories.views.RepositoryTaskNew.as_view(),
        name="task_new",
    ),
]
