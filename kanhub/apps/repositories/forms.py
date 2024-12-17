from django import forms
from django.utils.translation import gettext_lazy as _

import apps.repositories.models
import apps.repositories.forms


class SettingsForm(forms.ModelForm):
    class Meta:
        model = apps.repositories.models.Repository
        fields = ("name", "is_published", "users")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields["users"].queryset = self.fields["users"].queryset.exclude(id=self.instance.user.id)

class RepositoryForm(forms.ModelForm):
    class Meta:
        model = apps.repositories.models.Repository
        fields = ('name', 'is_published')


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