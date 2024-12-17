from django.urls import path, include

from apps.api.views import RepositoryAPIView, CommitAPIView, TaskAPIView

urlpatterns = [
    path("repositories/", RepositoryAPIView.as_view(), name="repository-list"),
    path('repositories/<int:pk>/', RepositoryAPIView.as_view(), name='repository-detail'),
    path("commits/", CommitAPIView.as_view(), name="commit-list"),
    path("repositories/<int:repository_id>/tasks/", TaskAPIView.as_view(), name="task-list"),
    path('repositories/<int:repository_id>/tasks/<int:pk>/', TaskAPIView.as_view(), name='task-detail'),
]
