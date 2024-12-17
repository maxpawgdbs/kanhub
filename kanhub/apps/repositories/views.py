__all__ = ()

import django.conf
import django.shortcuts
from django.contrib.auth.mixins import LoginRequiredMixin

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
        queryset = apps.repositories.models.Commit.objects.filter(
            repository=repository
        )
        return queryset


class RepositoryHistoryTasks(LoginRequiredMixin, django.views.generic.ListView):
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

        queryset = apps.repositories.models.Task.objects.filter(
            first_commit__id__lte=commit_id,
            commit__id__gte=commit_id
        )
        return queryset


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
            'repositories:detail',
           kwargs={'pk': self.kwargs['pk']}
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

        task_to_edit = self.request.POST.get(
            'task_pk') if 'task_pk' in self.request.POST else None
        if task_to_edit:
            context['task_to_edit'] = django.shortcuts.get_object_or_404(
                apps.repositories.models.Task, id=task_to_edit)

        return context


class RepositoryTask(django.views.generic.DetailView):
    template_name = "repositories/repository_tasks.html"
    context_object_name = "task"
    queryset = apps.repositories.models.Task.objects.all()

    def post(self, request, *args, **kwargs):
        repository_id = int(request.POST.get("repository_pk"))
        task_id = int(request.POST.get("task_pk"))
        method = request.POST.get("_method")

        if method.upper() == "DELETE":
            if task_id:
                task = apps.repositories.models.Task.objects.get(
                    id=task_id,
                    commit__repository_id=repository_id,
                )
                repository = django.shortcuts.get_object_or_404(
                    apps.repositories.models.Repository,
                    pk=self.kwargs["pk"],
                )
                last_commit = apps.repositories.models.Commit.objects.filter(
                    repository=repository,
                ).last()
                commit = apps.repositories.models.Commit.objects.create(
                    name=f"Delete task {task.name}",
                    user=self.request.user,
                    repository=repository,
                )

                if last_commit:
                    apps.repositories.models.Task.objects.filter(
                        commit=last_commit,
                    ).update(
                        commit=commit,
                    )
                    task.commit = last_commit
                    task.save()

            return django.shortcuts.redirect(
                "repositories:tasks",
                pk=repository_id,
            )


class EditTaskView(django.views.generic.edit.UpdateView):
    model = apps.repositories.models.Task
    template_name = 'repositories/task_update.html'
    form_class = apps.repositories.forms.TaskForm

    def get_object(self):
        task_id = self.kwargs.get('task_pk')
        repository_id = self.kwargs.get('pk')
        task = django.shortcuts.get_object_or_404(
            apps.repositories.models.Task,
            id=task_id,
            commit__repository_id=repository_id,
        )
        return task

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = self.object
        repository = task.commit.repository
        context['repository'] = repository
        context['last_task'] = task
        return context

    def form_valid(self, form):
        last_commit = apps.repositories.models.Commit.objects.filter(
            repository=self.get_object().commit.repository,
        ).last()
        last_task_id = self.request.POST.get('last_task')
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
            repository=self.get_object().commit.repository
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
        return django.urls.reverse('repositories:tasks', kwargs={'pk': self.object.commit.repository.id})


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
        data = apps.repositories.forms.SettingsForm(self.request.POST,
                                                    instance=rep)
        if data.is_valid():
            if self.request.user == rep.user:
                rep.name = data.cleaned_data["name"]
                rep.is_published = data.cleaned_data["is_published"]
                users = set(data.cleaned_data["users"])
                users.add(rep.user)
                rep.users.set(users)
                rep.full_clean()
                rep.save()
            else:
                django.contrib.messages.success(
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
