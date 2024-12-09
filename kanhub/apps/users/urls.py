__all__ = ()
from django.contrib.auth import views
import django.urls

import apps.users.views

app_name = "users"
urlpatterns = [
    django.urls.path(
        "login/",
        views.LoginView.as_view(
            template_name="users/login.html",
        ),
        name="login",
    ),
    django.urls.path(
        "logout/",
        views.LogoutView.as_view(
            template_name="users/base.html",
        ),
        name="logout",
    ),
    django.urls.path(
        "password_change/",
        views.PasswordChangeView.as_view(
            template_name="users/base.html",
        ),
        name="password_change",
    ),
    django.urls.path(
        "password_change/done/",
        views.PasswordChangeDoneView.as_view(
            template_name="users/base.html",
        ),
        name="password_change_done",
    ),
    django.urls.path(
        "password_reset/",
        views.PasswordResetView.as_view(
            template_name="users/base.html",
        ),
        name="password_reset",
    ),
    django.urls.path(
        "password_reset/done/",
        views.PasswordResetDoneView.as_view(
            template_name="users/base.html",
        ),
        name="password_reset_done",
    ),
    django.urls.path(
        "reset/<uidb64>/<token>",
        views.PasswordResetConfirmView.as_view(
            template_name="users/base.html",
        ),
        name="password_reset_confirm",
    ),
    django.urls.path(
        "password_reset_complete/",
        views.PasswordResetCompleteView.as_view(
            template_name="users/base.html",
        ),
        name="password_reset_complete",
    ),
    django.urls.path("signup/", apps.users.views.signup, name="signup"),
    django.urls.path("signup/", apps.users.views.activate, name="activate"),
    django.urls.path("profile/", apps.users.views.profile, name="profile"),
    django.urls.path(
        "profile/change/",
        apps.users.views.change_profile,
        name="change_profile",
    ),
]
