from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "",
        include("apps.about.urls"),
    ),
    path(
        "ckeditor/",
        include("ckeditor_uploader.urls"),
    ),
]
urlpatterns += i18n_patterns(
    path(
        "set_language/",
        include("django.conf.urls.i18n"),
        name="set_language",
    ),
)
