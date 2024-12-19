from django.urls import path, include

from apps.api import views

app_name = "api"

urlpatterns = [
    path("repositories/", views.RepositoryAPIView.as_view(), name="repository-list"),
    path('repositories/<int:pk>/', views.RepositoryAPIView.as_view(), name='repository-detail'),
    path("commits/", views.CommitAPIView.as_view(), name="commit-list"),
    path("repositories/<int:repository_id>/tasks/", views.TaskAPIView.as_view(), name="task-list"),
    path('repositories/<int:repository_id>/tasks/<int:pk>/', views.TaskAPIView.as_view(), name='task-detail'),
    path("docs/", views.APIDocsPreambleView.as_view(), name="docs_preamble"),
    path(
        "docs/qr_code_get",
        views.APIDocsCommitGetView.as_view(),
        name="docs_commits_get",
    ),
    path(
        "docs/repository_get",
        views.APIDocsRepositoryGetView.as_view(),
        name="docs_repository_get",
    ),
    path(
        "docs/repository_create",
        views.APIDocsRepositoryCreateView.as_view(),
        name="docs_repository_create",
    ),
    path(
        "docs/repository_update",
        views.APIDocsRepositoryUpdateView.as_view(),
        name="docs_repository_update",
    ),
    path(
        "docs/repository_delete",
        views.APIDocsRepositoryDeleteView.as_view(),
        name="docs_repository_delete",
    ),
    path(
        "docs/task_get",
        views.APIDocsTaskGetView.as_view(),
        name="docs_task_get",
    ),
    path(
        "docs/task_create",
        views.APIDocsTaskCreateView.as_view(),
        name="docs_task_create",
    ),
    path(
        "docs/task_update",
        views.APIDocsTaskUpdateView.as_view(),
        name="docs_task_update",
    ),
    path(
        "docs/task_delete",
        views.APIDocsTaskDeleteView.as_view(),
        name="docs_task_delete",
    ),
    path(
        "docs/token_get",
        views.APIDocsTokenGetView.as_view(),
        name="docs_token_get",
    ),
    path(
        "docs/token_create",
        views.APIDocsTokenCreateView.as_view(),
        name="docs_token_create",
    ),
]
