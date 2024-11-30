__all__ = ()
import django.urls

import apps.about.views

app_name = "about"
urlpatterns = [
    django.urls.path("", apps.about.views.main, name="main"),
]
