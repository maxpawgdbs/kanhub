__all__ = ()
import os
import pathlib

import django.utils.translation
import dotenv


def load_bool(name, default):
    env_value = os.getenv(name, default=str(default)).lower()
    return env_value in ("true", "yes", "1", "y", "t", "on")


BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
dotenv_path = BASE_DIR.parent.joinpath(".env")
dotenv.load_dotenv(dotenv_path=dotenv_path)

SECRET_KEY = os.getenv("KANHUB_DJANGO_SECRET_KEY", default="default_key")

DEBUG = load_bool("KANHUB_DJANGO_DEBUG", True)
DEFAULT_USER_IS_ACTIVE = load_bool("KANHUB_DJANGO_IS_ACTIVE", DEBUG)
MAX_AUTH_ATTEMPTS = int(
    os.getenv("KANHUB_DJANGO_MAX_AUTH_ATTEMPTS", default=3),
)
if DEBUG:
    def show_toolbar(request):
        return True
    DEBUG_TOOLBAR_CONFIG = {
        "SHOW_TOOLBAR_CALLBACK" : show_toolbar,
    }

ALLOWED_HOSTS = os.getenv("KANHUB_DJANGO_ALLOWED_HOSTS", default="*").split(
    ",",
)

INSTALLED_APPS = [
    "apps.users.apps.UsersConfig",
    "apps.about.apps.AboutConfig",
    "apps.homepage.apps.HomepageConfig",
    "apps.api.apps.ApiConfig",
    "apps.repositories.apps.RepositoriesConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "tinymce",
    "active_link",
    "sorl.thumbnail",
    "rest_framework",
    "rest_framework.authtoken",
    "ckeditor",
    "allauth",
    "allauth.account",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

if DEBUG:
    MIDDLEWARE.append("debug_toolbar.middleware.DebugToolbarMiddleware")
    INSTALLED_APPS.append("debug_toolbar")

ROOT_URLCONF = "kanhub.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "kanhub.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    },
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation"
        ".UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation"
        ".MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation"
        ".CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation"
        ".NumericPasswordValidator",
    },
]

AUTH_USER_MODEL = "users.User"

AUTHENTICATION_BACKENDS = [
    "apps.users.backends.AuthenticateBackend",
]

CKEDITOR_UPLOAD_PATH = "content/ckeditor/"

LANGUAGE_CODE = "ru-ru"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

LANGUAGES = (
    (
        "en",
        django.utils.translation.gettext_lazy("English"),
    ),
    (
        "ru",
        django.utils.translation.gettext_lazy("Русский"),
    ),
    (
        "de",
        django.utils.translation.gettext_lazy("Deutsch"),
    ),
)

LOCALE_PATHS = [
    BASE_DIR / "locale",
]

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static_dev"]
STATIC_ROOT = "static"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

LOGIN_URL = "/auth/login/"
LOGIN_REDIRECT_URL = "/auth/profile/"
LOGOUT_REDIRECT_URL = "/auth/login/"

EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = BASE_DIR / "send_mail"
MESSAGE_STORAGE = "django.contrib.messages.storage.session.SessionStorage"

ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_CHANGE_EMAIL = True
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1
ACCOUNT_EMAIL_VERIFICATION = "none" if DEFAULT_USER_IS_ACTIVE else "mandatory"
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_EMAIL_SUBJECT_PREFIX = "<[KANHUB]>"
SITE_ID = 1

EMAIL_HOST = os.getenv("KANHUB_MAIL_HOST", default="smtp.mail.ru")
EMAIL_PORT = os.getenv("KANHUB_MAIL_PORT", default=2525)
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
DEFAULT_FROM_EMAIL = os.getenv(
    "KANHUB_MAIL_USER",
    default="webmaster@localhost",
)
EMAIL_HOST_USER = os.getenv("KANHUB_MAIL_USER", default="webmaster@localhost")
EMAIL_HOST_PASSWORD = os.getenv(
    "KANHUB_MAIL_PASSWORD",
    default="secret_key",
)

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}
