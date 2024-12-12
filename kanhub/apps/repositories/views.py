__all__ = ()

import django.conf
import django.shortcuts

import apps.repositories.models


class RepositoryList(django.views.generic.ListView):
    template_name = "repositories/repository_list.html"
    context_object_name = "repositories"
    queryset = apps.repositories.models.Repository.objects.filter(
        is_published=True
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context["my_repositories"] = (
                self.request.user.repositories_contributed.all(),
            )
            context["repositories"] = context["repositories"].exclude(
                users=self.request.user,
            )

        return context


class RepositoryDetail(django.views.generic.DetailView):
    template_name = "repositories/repository_detail.html"
    context_object_name = "repository"
    queryset = apps.repositories.models.Repository.objects.all()


class RepositoryCalendar(django.views.generic.DetailView):
    template_name = "repositories/repository_calendar.html"
    context_object_name = "repository"
    queryset = apps.repositories.models.Repository.objects.all()


class RepositoryTasks(django.views.generic.DetailView):
    template_name = "repositories/repository_detail.html"
    context_object_name = "repository"
    queryset = apps.repositories.models.Repository.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        repository = self.object
        commits = apps.repositories.models.Commit.objects.filter(
            repository=repository,
        ).all()
        commit = commits.last()
        tasks = apps.repositories.models.Task.objects.filter(
            commit=commit,
        ).all()
        context["tasks"] = tasks
        return context


class RepositorySettings(django.views.generic.DetailView):
    template_name = "repositories/repository_detail.html"
    context_object_name = "repository"
    queryset = apps.repositories.models.Repository.objects.all()


class RepositoryMaterials(django.views.generic.DetailView):
    template_name = "repositories/repository_materials.html"
    context_object_name = "repository"
    queryset = apps.repositories.models.Repository.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        repository = self.object
        commits = apps.repositories.models.Commit.objects.filter(
            repository=repository,
        ).all()
        commit = commits.last()
        materials = apps.repositories.models.Redirect.objects.filter(
            commit=commit,
        ).all()
        context["materials"] = materials
        return context
