__all__ = ()

import django.conf
import django.contrib.auth
from django.contrib.auth.mixins import LoginRequiredMixin
import django.shortcuts

import apps.repositories.forms
import apps.repositories.models


class RepositoryList(LoginRequiredMixin, django.views.generic.ListView):
    template_name = "repositories/repository_list.html"
    context_object_name = "repositories"

    def get_queryset(self):
        return self.request.user.repositories_contributed.all()


class RepositoryHistory(LoginRequiredMixin, django.views.generic.ListView):
    template_name = "repositories/repository_history.html"
    context_object_name = "histories"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        repository = django.shortcuts.get_object_or_404(
            apps.repositories.models.Repository,
            pk=self.kwargs["pk"],
        )
        context["repository"] = repository
        return context

    def get_queryset(self):
        repository = django.shortcuts.get_object_or_404(
            apps.repositories.models.Repository,
            pk=self.kwargs["pk"],
        )
        return apps.repositories.models.Commit.objects.filter(
            repository=repository,
        )


class RepositoryHistoryTasks(
    LoginRequiredMixin,
    django.views.generic.ListView,
):
    template_name = "repositories/repository_history_tasks.html"
    context_object_name = "tasks"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        repository = django.shortcuts.get_object_or_404(
            apps.repositories.models.Repository,
            pk=self.kwargs["pk"],
        )
        context["repository"] = repository
        return context

    def get_queryset(self):
        commit_id = self.kwargs["commit_id"]

        return apps.repositories.models.Task.objects.filter(
            first_commit__id__lte=commit_id,
            commit__id__gte=commit_id,
        )


class RepositoryDetail(django.views.generic.DetailView):
    template_name = "repositories/repository_detail.html"
    context_object_name = "repository"
    queryset = apps.repositories.models.Repository.objects.all()


class RepositoryNew(LoginRequiredMixin, django.views.generic.CreateView):
    model = apps.repositories.models.Repository
    template_name = "repositories/repository_new.html"
    form_class = apps.repositories.forms.RepositoryForm
    success_url = django.urls.reverse_lazy("repositories:list")

    def form_valid(self, form):
        repository = form.save(commit=False)
        repository.user = self.request.user
        repository.save()
        repository.users.add(self.request.user)
        return super().form_valid(form)


class RepositoryDelete(LoginRequiredMixin, django.views.generic.DeleteView):
    model = apps.repositories.models.Repository
    template_name = "repositories/repository_delete.html"
    success_url = django.urls.reverse_lazy("repositories:list")

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        django.contrib.messages.success(request, "Репозиторий успешно удален!")
        return response


class RepositoryTaskNew(LoginRequiredMixin, django.views.generic.CreateView):
    model = apps.repositories.models.Task
    template_name = "repositories/task_new.html"
    form_class = apps.repositories.forms.TaskForm

    def form_valid(self, form):
        repository = django.shortcuts.get_object_or_404(
            apps.repositories.models.Repository,
            pk=self.kwargs["pk"],
        )

        last_commit = apps.repositories.models.Commit.objects.filter(
            repository=repository,
        ).last()

        commit = apps.repositories.models.Commit.objects.create(
            name=f"Create task {form.cleaned_data['name']}",
            user=self.request.user,
            repository=repository,
        )

        form.instance.repository = repository
        form.instance.first_commit = commit
        form.instance.commit = commit

        if last_commit:
            apps.repositories.models.Task.objects.filter(
                commit=last_commit,
            ).update(
                commit=commit,
            )

        django.contrib.messages.success(
            self.request,
            "Задание успешно создано!",
        )
        return super().form_valid(form)

    def get_success_url(self):
        return django.urls.reverse(
            "repositories:detail",
            kwargs={"pk": self.kwargs["pk"]},
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        repository = django.shortcuts.get_object_or_404(
            apps.repositories.models.Repository,
            pk=self.kwargs["pk"],
        )
        context["repository"] = repository
        return context


class RepositoryCalendar(django.views.generic.DetailView):
    template_name = "repositories/repository_calendar.html"
    context_object_name = "repository"
    queryset = apps.repositories.models.Repository.objects.all()


class RepositoryTasks(django.views.generic.DetailView):
    template_name = "repositories/repository_tasks.html"
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

        user = self.request.user
        users = repository.users.all()

        context["tasks"] = tasks
        context["is_can"] = user in users

        task_to_edit = (
            self.request.POST.get("task_pk")
            if "task_pk" in self.request.POST
            else None
        )
        if task_to_edit:
            context["task_to_edit"] = django.shortcuts.get_object_or_404(
                apps.repositories.models.Task,
                id=task_to_edit,
            )

        return context


class RepositoryTask(django.views.generic.DetailView):
    template_name = "repositories/repository_tasks.html"
    context_object_name = "task"
    queryset = apps.repositories.models.Task.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["repository"] = self.object.commit.repository
        return context


class RepositoryTaskDelete(django.views.generic.View):
    def get(self, request, *args, **kwargs):
        repository_id = self.kwargs.get("pk")
        task_id = self.kwargs.get("task_pk")

        repository = django.shortcuts.get_object_or_404(
            apps.repositories.models.Repository,
            pk=repository_id,
        )
        task = django.shortcuts.get_object_or_404(
            apps.repositories.models.Task,
            id=task_id,
            commit__repository=repository,
        )

        last_commit = apps.repositories.models.Commit.objects.filter(
            repository=repository,
        ).last()

        commit = apps.repositories.models.Commit.objects.create(
            name=f"Delete task {task.name}",
            user=request.user,
            repository=repository,
        )

        if last_commit:
            apps.repositories.models.Task.objects.filter(
                commit=last_commit,
            ).update(commit=commit)
            task.commit = last_commit
            task.save()

        django.contrib.messages.success(
            request,
            "Задача успешно удалена.",
        )

        return django.shortcuts.redirect(
            "repositories:tasks",
            pk=repository_id,
        )


class EditTaskView(django.views.generic.edit.UpdateView):
    model = apps.repositories.models.Task
    template_name = "repositories/task_update.html"
    form_class = apps.repositories.forms.TaskForm

    def get_object(self):
        task_id = self.kwargs.get("task_pk")
        repository_id = self.kwargs.get("pk")
        return django.shortcuts.get_object_or_404(
            apps.repositories.models.Task,
            id=task_id,
            commit__repository_id=repository_id,
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = self.object
        repository = task.commit.repository
        context["repository"] = repository
        context["last_task"] = task
        return context

    def form_valid(self, form):
        last_commit = apps.repositories.models.Commit.objects.filter(
            repository=self.get_object().commit.repository,
        ).last()
        last_task_id = self.request.POST.get("last_task")
        last_task = apps.repositories.models.Task.objects.get(id=last_task_id)

        last_task = apps.repositories.models.Task.objects.create(
            name=last_task.name,
            text=last_task.text,
            start_at=last_task.start_at,
            end_at=last_task.end_at,
            commit=last_commit,
            first_commit=last_task.first_commit,
        )

        task = form.save(commit=False)

        commit = apps.repositories.models.Commit.objects.create(
            name=f"Edit task {task.name}",
            user=self.request.user,
            repository=self.get_object().commit.repository,
        )

        if last_commit:
            apps.repositories.models.Task.objects.filter(
                commit=last_commit,
            ).update(
                commit=commit,
            )

        task.commit = commit
        task.first_commit = commit
        last_task.commit = last_commit
        last_task.save()

        django.contrib.messages.success(
            self.request,
            "Задача успешно обновлена!",
        )
        return super().form_valid(form)

    def get_success_url(self):
        return django.urls.reverse(
            "repositories:tasks",
            kwargs={"pk": self.object.commit.repository.id},
        )


class RepositorySettings(django.views.generic.DetailView):
    template_name = "repositories/repository_settings.html"
    context_object_name = "repository"
    queryset = apps.repositories.models.Repository.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["settings_form"] = apps.repositories.forms.SettingsForm(
            instance=self.object,
        )
        return context

    def post(self, *args, **kwargs):
        rep = self.get_object()
        data = apps.repositories.forms.SettingsForm(self.request.POST)
        if data.is_valid():
            if self.request.user == rep.user:
                if (
                    data.cleaned_data["name"]
                    and rep.name != data.cleaned_data["name"]
                ):
                    rep.name = data.cleaned_data["name"]
                    django.contrib.messages.success(
                        self.request,
                        "Репозиторий переименован",
                    )

                if rep.is_published != data.cleaned_data["is_published"]:
                    rep.is_published = data.cleaned_data["is_published"]
                    django.contrib.messages.success(
                        self.request,
                        "Статус публикации сменён",
                    )

                if data.cleaned_data["add_user"]:
                    try:
                        new_user = (
                            django.contrib.auth.get_user_model().objects.get(
                                username=data.cleaned_data["add_user"],
                            )
                        )
                        rep.users.add(new_user)
                        django.contrib.messages.error(
                            self.request,
                            "Юзер добавлен",
                        )
                    except Exception:
                        django.contrib.messages.error(
                            self.request,
                            "Юзер не найден",
                        )

                if data.cleaned_data["del_selected_users"]:
                    for user in data.cleaned_data["users"]:
                        rep.users.remove(user)

                rep.full_clean()
                rep.save()
            else:
                django.contrib.messages.error(
                    self.request,
                    "У вас нет прав на изменение этого репозитория",
                )

        else:
            for error in data.errors:
                django.contrib.messages.success(
                    self.request,
                    error,
                )

        return django.shortcuts.redirect("repositories:settings", pk=rep.id)
