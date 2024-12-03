__all__ = ()
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import django.shortcuts
import django.utils

import apps.users.forms
import apps.users.models


def signup(request):
    if request.method == "POST":
        form = apps.users.forms.CustomUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password1"]
            last = User.objects.create_user(
                username,
                email,
                password,
            )
            last.is_active = settings.DEFAULT_USER_IS_ACTIVE
            last.save()
            apps.users.models.Profile.objects.create(user=last)
            if not settings.DEFAULT_USER_IS_ACTIVE:
                mail_url = django.urls.reverse(
                    "users:activate",
                    args=[last.username],
                )
                url = f"{request.scheme}://{request.get_host()}{mail_url}"
                result = django.core.mail.send_mail(
                    subject=last.username,
                    message="У вас 12 часов на активацию "
                    "профиля на нашем сайте\n"
                    f"вот ссылка: {url}",
                    from_email=settings.DJANGO_MAIL,
                    recipient_list=[
                        last.email,
                    ],
                    fail_silently=False,
                )

                if result:
                    message = "Отправили письмо активации на почту"
                else:
                    message = "Ошибка!"

                django.contrib.messages.success(
                    request,
                    message,
                )

            return django.shortcuts.redirect("users:login")

        for field, errors in form.errors.items():
            for error in errors:
                django.contrib.messages.error(request, f"{field}: {error}")

        return django.shortcuts.redirect("users:signup")

    form = apps.users.forms.CustomUserForm()
    context = {"form": form}
    return django.shortcuts.render(request, "users/signup.html", context)


def activate(request, username):
    obj = django.shortcuts.get_object_or_404(
        User.objects,
        username=username,
    )
    date = obj.date_joined
    hours = django.utils.timezone.now() - date
    hours = hours.total_seconds() / 3600
    if hours < 12:
        obj.is_active = True
        obj.save()

    return django.shortcuts.render(request, "users/information.html")


@login_required
def profile(request):
    context = {
        "username": request.user.username,
        "email": request.user.email,
        "profile": request.user.profile,
    }
    return django.shortcuts.render(request, "users/profile.html", context)


@login_required
def change_profile(request):
    if request.method == "POST":
        form = apps.users.forms.ChangeProfile(request.POST or None)
        if form.is_valid():
            image = request.FILES.get("image")

            user_profile = request.user.profile

            if request.POST.get("image-clear", False):
                user_profile.image.delete(save=False)

            if image:
                user_profile.image = image

            user_profile.full_clean()
            user_profile.save()

            django.contrib.messages.success(
                request,
                "Изменения сохранены",
            )
            return django.shortcuts.redirect("users:profile")

    context = {
        "username": request.user.username,
        "email": request.user.email,
        "form": apps.users.forms.ChangeProfile(instance=request.user.profile),
    }
    return django.shortcuts.render(
        request,
        "users/change_profile.html",
        context,
    )
