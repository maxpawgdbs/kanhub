from django.forms import ModelForm
import apps.repositories.models


class SettingsForm(ModelForm):
    class Meta:
        model = apps.repositories.models.Repository
        fields = ("name", "is_published", "user", "users")
