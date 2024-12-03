__all__ = ()
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import User
import django.forms

import apps.users.models


class CustomUserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            "username",
            "email",
            "password1",
            "password2",
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()

        return user


class ChangeProfile(django.forms.ModelForm):
    class Meta(UserChangeForm.Meta):
        model = apps.users.models.Profile
        fields = ("image",)
