__all__ = ()

import calendar
from datetime import datetime

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

    def get_queryset(self):
        queryset = apps.repositories.models.Repository.objects.all()

        date = self.request.GET.get("date")
        if date:
            try:
                input_date = datetime.strptime(date, "%Y-%m-%d").date()
                _, last_day_of_month = calendar.monthrange(input_date.year,
                                                           input_date.month)
                last_day_of_month = input_date.replace(day=last_day_of_month)
                queryset = queryset.filter(
                    created_at__lte=last_day_of_month,
                    updated_at__gte=input_date,
                )
            except ValueError:
                pass
        else:
            today = datetime.today()
            first_day_of_month = today.replace(day=1)
            _, last_day_of_month = calendar.monthrange(today.year, today.month)
            last_day_of_month = first_day_of_month.replace(
                day=last_day_of_month)
            queryset = queryset.filter(
                created_at__lte=last_day_of_month,
                updated_at__gte=first_day_of_month,
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["page_obj"] = self.get_queryset
        context["disciplines"] = (
            meropriations.models.Discipline.objects.values_list(
                "name",
                flat=True,
            )
            .distinct()
            .order_by("name")
        )
        context["tips"] = (
            meropriations.models.Meropriation.objects.values_list(
                "tip__name",
                flat=True,
            )
            .distinct()
            .order_by("tip__name")
        )
        context["structures"] = (
            meropriations.models.Meropriation.objects.values_list(
                "structure__name",
                flat=True,
            )
            .distinct()
            .order_by("structure__name")
        )
        context["regions"] = (
            meropriations.models.Meropriation.objects.values_list(
                "region__name",
                flat=True,
            )
            .distinct()
            .order_by("region__name")
        )
        context["request"] = self.request
        context["day_week_list"] = [
            "Понедельник",
            "Вторник",
            "Среда",
            "Четверг",
            "Пятница",
            "Суббота",
            "Воскресенье",
        ]

        date = self.request.GET.get("date")

        if date:
            try:
                input_date = datetime.strptime(date, "%Y-%m-%d").date()
                date_delta = input_date.weekday()
            except ValueError:
                input_date = datetime.now()
                date_delta = input_date.weekday()
        else:
            input_date = datetime.now()
            date_delta = input_date.weekday()

        queryset = self.get_queryset()
        grouped_events = defaultdict(list)
        for event in queryset:
            start_date = event.date_start
            end_date = event.date_end
            current_date = start_date
            while current_date <= end_date:
                grouped_events[current_date.day].append(event)
                current_date += timedelta(days=1)

        _, days_in_month = calendar.monthrange(
            input_date.year,
            input_date.month,
        )
        weeks = []
        current_week = [0] * date_delta
        for day in range(1, days_in_month + 1):
            events_for_day = grouped_events.get(day, [])
            current_week.append({"date": day, "events": events_for_day})

            if len(current_week) == 7:
                weeks.append(current_week)
                current_week = []

        if current_week:
            weeks.append(current_week)

        context["calendar_weeks"] = weeks
        return context


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
            apps.repositories.models.Task.objects.filter(commit=last_commit).update(commit=commit)
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
