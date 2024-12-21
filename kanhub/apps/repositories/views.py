__all__ = ()

import calendar
from datetime import datetime, timedelta

import django.conf
import django.contrib.auth
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
import django.shortcuts
from django.utils.translation import gettext_lazy

import apps.repositories.forms
import apps.repositories.models


def check_repository_access(repository, user):
    if (
        not repository.is_published
        and user not in repository.users.all()
        and repository.user != user
    ):
        raise Http404("Репозиторий недоступен.")


class RepositoryList(LoginRequiredMixin, django.views.generic.ListView):
    template_name = "repositories/repository_list.html"
    context_object_name = "repositories"

    def get_queryset(self):
        return self.request.user.repositories_contributed.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["choice"] = gettext_lazy("Опубликовано, Не опубликовано")
        return context


class RepositoryHistory(django.views.generic.ListView):
    template_name = "repositories/repository_history.html"
    context_object_name = "histories"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        repository = django.shortcuts.get_object_or_404(
            apps.repositories.models.Repository,
            pk=self.kwargs["pk"],
        )
        check_repository_access(repository, self.request.user)
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


class RepositoryHistoryTasks(django.views.generic.ListView):
    template_name = "repositories/repository_history_tasks.html"
    context_object_name = "tasks"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        repository = django.shortcuts.get_object_or_404(
            apps.repositories.models.Repository,
            pk=self.kwargs["pk"],
        )

        check_repository_access(repository, self.request.user)

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

    def get_context_data(self, **kwargs):
        repository = django.shortcuts.get_object_or_404(
            apps.repositories.models.Repository,
            pk=self.kwargs["pk"],
        )
        check_repository_access(repository, self.request.user)
        return super().get_context_data(**kwargs)


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
        django.contrib.messages.success(request, "Репозиторий успешно удален!")
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        repository = django.shortcuts.get_object_or_404(
            apps.repositories.models.Repository,
            pk=self.kwargs["pk"],
        )
        check_repository_access(repository, self.request.user)

        context["repository"] = repository
        return context


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
        check_repository_access(repository, self.request.user)

        context["repository"] = repository
        return context


class RepositoryCalendar(django.views.generic.ListView):
    template_name = "repositories/repository_calendar.html"

    def get_queryset(self):
        repository = django.shortcuts.get_object_or_404(
            apps.repositories.models.Repository,
            pk=self.kwargs["pk"],
        )

        commit = apps.repositories.models.Commit.objects.filter(
            repository=repository,
        ).last()

        if not commit:
            return apps.repositories.models.Task.objects.none()

        queryset = apps.repositories.models.Task.objects.filter(commit=commit)

        tag = self.request.GET.get("tag")
        if tag:
            queryset = queryset.filter(tags__name__icontains=tag)

        start_date = self.request.GET.get("start_at")
        if start_date:
            try:
                start_date_obj = datetime.strptime(
                    start_date,
                    "%Y-%m-%d",
                ).date()
                queryset = queryset.filter(start_at__gte=start_date_obj)
            except ValueError:
                pass

        end_date = self.request.GET.get("end_at")
        if end_date:
            try:
                end_date_obj = datetime.strptime(end_date, "%Y-%m-%d").date()
                queryset = queryset.filter(end_at__lte=end_date_obj)
            except ValueError:
                pass

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        repository = django.shortcuts.get_object_or_404(
            apps.repositories.models.Repository,
            pk=self.kwargs["pk"],
        )
        check_repository_access(repository, self.request.user)

        context["tasks"] = self.get_queryset()

        date = self.request.GET.get("date")
        if date:
            try:
                input_date = datetime.strptime(date, "%Y-%m-%d").date()
                date_delta = input_date.weekday()
            except ValueError:
                input_date = datetime.now().date()
                date_delta = input_date.weekday()
        else:
            input_date = datetime.now().date()
            date_delta = input_date.weekday()

        queryset = self.get_queryset()
        grouped_task = {}

        for task in queryset:
            start_date = task.start_at
            end_date = task.end_at
            current_date = start_date
            while current_date <= end_date:
                year = current_date.year
                month = current_date.month
                day = current_date.day

                date_key = f"{year}-{month:02d}-{day:02d}"

                if date_key not in grouped_task:
                    grouped_task[date_key] = []

                grouped_task[date_key].append(task)
                current_date += timedelta(days=1)

        _, days_in_month = calendar.monthrange(
            input_date.year,
            input_date.month,
        )
        weeks = []
        current_week = [None] * date_delta
        for day in range(1, days_in_month + 1):
            date_key = f"{input_date.year}-{input_date.month:02d}-{day:02d}"
            tasks_for_day = grouped_task.get(date_key, [])
            current_week.append({"date": day, "tasks": tasks_for_day})

            if len(current_week) == 7:
                weeks.append(current_week)
                current_week = []

        if current_week:
            weeks.append(current_week)

        context["calendar_weeks"] = weeks

        context["tags"] = apps.repositories.models.Tag.objects.values_list(
            "name",
            flat=True,
        ).distinct()
        commit_objects = apps.repositories.models.Commit.objects
        context["commits"] = (
            commit_objects.filter(
                repository=self.kwargs["pk"],
            )
            .values_list("name", flat=True)
            .distinct()
        )

        context["repository"] = repository
        context["day_week_list"] = [
            gettext_lazy("Monday"),
            gettext_lazy("Tuesday"),
            gettext_lazy("Wednesday"),
            gettext_lazy("Thursday"),
            gettext_lazy("Friday"),
            gettext_lazy("Saturday"),
            gettext_lazy("Sunday"),
        ]

        return context


class RepositoriesCalendar(django.views.generic.ListView):
    template_name = "repositories/repositories_calendar.html"
    model = apps.repositories.models.Repository
    context_object_name = "repositories"

    def get_queryset(self):
        queryset = apps.repositories.models.Repository.objects.filter(
            is_published=True,
        )

        # Фильтр по дате создания
        created_from = self.request.GET.get("created_from")
        if created_from:
            try:
                created_from_date = datetime.strptime(
                    created_from,
                    "%Y-%m-%d",
                ).date()
                queryset = queryset.filter(created_at__gte=created_from_date)
            except ValueError:
                pass

        created_to = self.request.GET.get("created_to")
        if created_to:
            try:
                created_to_date = datetime.strptime(
                    created_to,
                    "%Y-%m-%d",
                ).date()
                queryset = queryset.filter(created_at__lte=created_to_date)
            except ValueError:
                pass

        # Фильтр по дате обновления
        updated_from = self.request.GET.get("updated_from")
        if updated_from:
            try:
                updated_from_date = datetime.strptime(
                    updated_from,
                    "%Y-%m-%d",
                ).date()
                queryset = queryset.filter(updated_at__gte=updated_from_date)
            except ValueError:
                pass

        updated_to = self.request.GET.get("updated_to")
        if updated_to:
            try:
                updated_to_date = datetime.strptime(
                    updated_to,
                    "%Y-%m-%d",
                ).date()
                queryset = queryset.filter(updated_at__lte=updated_to_date)
            except ValueError:
                pass

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Генерация данных для календаря
        date = self.request.GET.get("date")
        if date:
            try:
                input_date = datetime.strptime(date, "%Y-%m-%d").date()
                date_delta = input_date.weekday()
            except ValueError:
                input_date = datetime.now().date()
                date_delta = input_date.weekday()
        else:
            input_date = datetime.now().date()
            date_delta = input_date.weekday()

        queryset = self.get_queryset()
        grouped_repositories = {}

        for repository in queryset:
            created_date = repository.created_at.date()
            year = created_date.year
            month = created_date.month
            day = created_date.day
            date_key = f"{year}-{month:02d}-{day:02d}"

            if date_key not in grouped_repositories:
                grouped_repositories[date_key] = []

            grouped_repositories[date_key].append(repository)

        _, days_in_month = calendar.monthrange(
            input_date.year,
            input_date.month,
        )
        weeks = []
        current_week = [None] * date_delta
        for day in range(1, days_in_month + 1):
            date_key = f"{input_date.year}-{input_date.month:02d}-{day:02d}"
            repositories_for_day = grouped_repositories.get(date_key, [])
            current_week.append(
                {"date": day, "repositories": repositories_for_day},
            )

            if len(current_week) == 7:
                weeks.append(current_week)
                current_week = []

        if current_week:
            weeks.append(current_week)

        context["calendar_weeks"] = weeks
        context["day_week_list"] = [
            gettext_lazy("Monday"),
            gettext_lazy("Tuesday"),
            gettext_lazy("Wednesday"),
            gettext_lazy("Thursday"),
            gettext_lazy("Friday"),
            gettext_lazy("Saturday"),
            gettext_lazy("Sunday"),
        ]

        return context


class RepositoryTasks(django.views.generic.DetailView):
    template_name = "repositories/repository_tasks.html"
    context_object_name = "repository"
    queryset = apps.repositories.models.Repository.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        repository = self.object

        check_repository_access(repository, self.request.user)

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
        repository = context["repository"]

        check_repository_access(repository, self.request.user)

        return context


class RepositoryTaskDelete(django.views.generic.View):
    def get(self, request, *args, **kwargs):
        repository_id = self.kwargs.get("pk")
        task_id = self.kwargs.get("task_pk")

        repository = django.shortcuts.get_object_or_404(
            apps.repositories.models.Repository,
            pk=repository_id,
        )

        check_repository_access(repository, self.request.user)

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

        check_repository_access(repository, self.request.user)

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
        obj = self.object
        context["settings_form"] = apps.repositories.forms.SettingsForm(
            instance=obj,
        )
        check_repository_access(self.object, self.request.user)
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
