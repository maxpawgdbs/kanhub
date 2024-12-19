import apps.repositories.forms
from ckeditor.widgets import CKEditorWidget
from django import forms
from django.utils.translation import gettext_lazy as _


class SettingsForm(forms.ModelForm):
    class Meta:
        model = apps.repositories.models.Repository
        fields = ("name", "is_published", "users")
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control",
                                           "placeholder": _(
                                               "Enter repository name")}),
            "is_published": forms.CheckboxInput(
                attrs={"class": "form-check-input"}),
            "users": forms.SelectMultiple(attrs={"class": "form-select"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields["users"].queryset = self.fields[
                "users"].queryset.exclude(id=self.instance.user.id)


class RepositoryForm(forms.ModelForm):
    class Meta:
        model = apps.repositories.models.Repository
        fields = ('name', 'is_published')
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control",
                                           "placeholder": _(
                                               "Enter repository name")}),
            "is_published": forms.CheckboxInput(
                attrs={"class": "form-check-input"}),
        }


class TaskForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = apps.repositories.models.Task
        fields = ("name", "tags", "text", "start_at", "end_at")
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": _(
                                               "Enter task name")}),
            "tags": forms.SelectMultiple(),
            "text": CKEditorWidget(),
            "start_at": forms.DateInput(
                attrs={"type": "date"},
                format="%Y-%m-%d"),
            "end_at": forms.DateInput(
                attrs={"type": "date"},
                format="%Y-%m-%d"),
        }

    def clean(self):
        cleaned_data = super().clean()
        date_start = cleaned_data.get("start_at")
        date_end = cleaned_data.get("end_at")

        if date_start and date_end:
            if date_start >= date_end:
                raise forms.ValidationError(
                    _("The end date must be after the start date."))

        return cleaned_data
