from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "",
        include("apps.about.urls"),
    ),
    path(
        "repositories/",
        include("apps.repositories.urls"),
    ),
    path(
        "ckeditor/",
        include("ckeditor_uploader.urls"),
    ),
    path("auth/", include("apps.users.urls")),
]
urlpatterns += i18n_patterns(
    path(
        "set_language/",
        include("django.conf.urls.i18n"),
        name="set_language",
    ),
)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
