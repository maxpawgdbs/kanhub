__all__ = ()
from django import forms
from django.utils.translation import gettext_lazy as _

import apps.repositories.forms
import apps.repositories.models


class SettingsForm(forms.ModelForm):
    add_user = forms.CharField(required=False)
    del_selected_users = forms.BooleanField(required=False)

    class Meta:
        model = apps.repositories.models.Repository
        fields = ("name", "is_published", "users")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if len(args) == 0 and self.instance and self.instance.user:
            self.fields["users"].queryset = self.instance.users.all().exclude(
                id=self.instance.user.id,
            )


class RepositoryForm(forms.ModelForm):
    class Meta:
        model = apps.repositories.models.Repository
        fields = ("name", "is_published")


class TaskForm(forms.ModelForm):
    class Meta:
        model = apps.repositories.models.Task
        fields = ("name", "tags", "text", "start_at", "end_at")
        widgets = {
            "start_at": forms.DateInput(
                attrs={"class": "form-control", "type": "date"},
                format="%Y-%m-%d",
            ),
            "end_at": forms.DateInput(
                attrs={"class": "form-control", "type": "date"},
                format="%Y-%m-%d",
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        date_start = cleaned_data.get("start_at")
        date_end = cleaned_data.get("end_at")

        if date_start and date_end and date_end < date_start:
            raise forms.ValidationError(
                _("The end date must be after the start date."),
            )

        return cleaned_data
