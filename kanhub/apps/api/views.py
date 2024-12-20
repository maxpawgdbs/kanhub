__all__ = ()

from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.api.serializers import (
    CommitSerializer,
    RepositorySerializer,
    TaskSerializer,
)
from apps.repositories.models import Commit, Repository, Tag, Task


class APIDocsPreambleView(TemplateView):
    template_name = "api/docs/preamble.html"


class APIDocsCommitGetView(TemplateView):
    template_name = "api/docs/commits_get.html"


class APIDocsRepositoryGetView(TemplateView):
    template_name = "api/docs/repository_get.html"


class APIDocsRepositoryCreateView(TemplateView):
    template_name = "api/docs/repository_create.html"


class APIDocsRepositoryUpdateView(TemplateView):
    template_name = "api/docs/repository_update.html"


class APIDocsRepositoryDeleteView(TemplateView):
    template_name = "api/docs/repository_delete.html"


class APIDocsTaskGetView(TemplateView):
    template_name = "api/docs/task_get.html"


class APIDocsTaskCreateView(TemplateView):
    template_name = "api/docs/task_create.html"


class APIDocsTaskUpdateView(TemplateView):
    template_name = "api/docs/task_update.html"


class APIDocsTaskDeleteView(TemplateView):
    template_name = "api/docs/task_delete.html"


class APIDocsTokenGetView(TemplateView):
    template_name = "api/docs/token_get.html"


class APIDocsTokenCreateView(TemplateView):
    template_name = "api/docs/token_create.html"


class RepositoryAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        repositories = Repository.objects.filter(user=request.user)
        serializer = RepositorySerializer(repositories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = RepositorySerializer(data=request.data)
        if serializer.is_valid():
            repository = serializer.save(user=self.request.user)
            repository.users.add(self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            repository = Repository.objects.get(pk=pk, user=request.user)
        except Repository.DoesNotExist:
            return Response(
                {"error": "Repository not found or access denied"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = RepositorySerializer(repository, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        try:
            repository = Repository.objects.get(pk=pk, user=request.user)
        except Repository.DoesNotExist:
            return Response(
                {"error": "Repository not found or access denied"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = RepositorySerializer(
            repository,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            repository = Repository.objects.get(id=pk, user=request.user)
            repository.delete()
            return Response(
                {"detail": "Repository deleted successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Repository.DoesNotExist:
            return Response(
                {"error": "Repository not found or access denied"},
                status=status.HTTP_404_NOT_FOUND,
            )


class CommitAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        commits = Commit.objects.filter(repository__user=request.user)
        serializer = CommitSerializer(commits, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CommitSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, repository_id, pk=0, *args, **kwargs):
        repository = get_object_or_404(
            Repository,
            pk=repository_id,
            user=request.user,
        )

        if pk:
            tasks = Task.objects.filter(
                pk=pk,
                commit__repository=repository,
                commit__repository__user=request.user,
            )
        else:
            tasks = Task.objects.filter(
                commit__repository=repository,
                commit__repository__user=request.user,
            )

        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, repository_id, *args, **kwargs):
        repository = get_object_or_404(
            Repository, pk=repository_id, user=request.user,
        )

        last_commit = Commit.objects.filter(repository=repository).last()

        commit = Commit.objects.create(
            name=f"Create task {request.data.get('name')}",
            user=request.user,
            repository=repository,
        )

        data = request.data.copy()
        data["commit"] = commit.id
        data["first_commit"] = commit.id

        serializer = TaskSerializer(data=data)
        if serializer.is_valid():
            serializer.save()

            if last_commit:
                Task.objects.filter(commit=last_commit).update(commit=commit)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, repository_id, pk):
        task = get_object_or_404(
            Task,
            pk=pk,
            commit__repository_id=repository_id,
            commit__repository__user=request.user,
        )

        repository = task.commit.repository
        last_commit = Commit.objects.filter(repository=repository).last()

        commit = Commit.objects.create(
            name=f"Edit task {task.name}",
            user=request.user,
            repository=repository,
        )

        request_data = request.data.copy()
        request_data["commit"] = commit.id
        request_data["first_commit"] = commit.id

        if last_commit:
            Task.objects.filter(
                commit=last_commit,
            ).update(
                commit=commit,
            )

        serializer = TaskSerializer(task, data=request_data)
        if serializer.is_valid():
            updated_task = serializer.save()
            return Response(
                TaskSerializer(updated_task).data,
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, repository_id, pk):
        task = get_object_or_404(
            Task,
            pk=pk,
            commit__repository_id=repository_id,
            commit__repository__user=request.user,
        )

        repository = task.commit.repository
        last_commit = Commit.objects.filter(repository=repository).last()

        commit = Commit.objects.create(
            name=f"Edit task {task.name}",
            user=request.user,
            repository=repository,
        )

        request_data = request.data.copy()
        request_data["commit"] = commit.id
        request_data["first_commit"] = commit.id

        if last_commit:
            Task.objects.filter(
                commit=last_commit,
            ).update(
                commit=commit,
            )

        serializer = TaskSerializer(task, data=request_data, partial=True)
        if serializer.is_valid():
            updated_task = serializer.save()
            return Response(
                TaskSerializer(updated_task).data,
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        repository_id = self.kwargs.get("repository_id")
        task_id = self.kwargs.get("pk")

        repository = get_object_or_404(
            Repository,
            pk=repository_id,
            user=request.user,
        )

        task = get_object_or_404(
            Task,
            id=task_id,
            commit__repository=repository,
        )

        last_commit = Commit.objects.filter(repository=repository).last()

        commit = Commit.objects.create(
            name=f"Delete task {task.name}",
            user=request.user,
            repository=repository,
        )

        if last_commit:
            Task.objects.filter(commit=last_commit).update(commit=commit)
            task.commit = last_commit
            task.save()

        return Response(
            {
                "detail": "Task 'deleted' successfully (marked as removed with new commit).",
            },
            status=status.HTTP_200_OK,
        )
