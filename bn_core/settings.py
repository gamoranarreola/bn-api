import io
import os
from datetime import timedelta

import environ

if os.environ.get("GOOGLE_CLOUD_PROJECT", None):
    from google.cloud import secretmanager


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

env = environ.Env(DEBUG=(bool, False))
env_file = os.path.join(BASE_DIR, ".env")

if os.path.isfile(env_file):
    env.read_env(env_file)
elif os.getenv("GOOGLE_CLOUD_PROJECT", None):
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT", None)
    client = secretmanager.SecretManagerServiceClient()
    settings_name = os.getenv("SETTINGS_NAME", "django_settings")
    name = f"projects/{project_id}/secrets/{settings_name}/versions/latest"
    payload = client.access_secret_version(name=name).payload.data.decode("UTF-8")

    env.read_env(io.StringIO(payload))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/
if os.getenv("GOOGLE_CLOUD_PROJECT", None):
    DEBUG = False

    ALLOWED_HOSTS = ["*"]
    SECRET_KEY = env("SECRET_KEY")

    CORS_ORIGIN_WHITELIST = [
        "https://beauty-now-313716.wl.r.appspot.com",
        "https://beautynow.app",
        "https://www.beautynow.app",
    ]

else:
    DEBUG = True

    ALLOWED_HOSTS = [
        "127.0.0.1",
        "localhost",
    ]

    SECRET_KEY = "7j+o-t^gvqr5yice#l4fn9(mydgvo1y#^*g8y0fq+o8%jw@05m"

    CORS_ORIGIN_WHITELIST = [
        "https://localhost:8100",
        "http://localhost:8100",
    ]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "bn_app",
    "bn_utils",
    "rest_framework",
    "rest_framework.authtoken",
    "corsheaders",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "bn_app/html")],
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

OAUTH2_PROVIDER = {
    # this is the list of available scopes
    "SCOPES": {
        "read": "Read scope",
        "write": "Write scope",
        "groups": "Access to your groups",
    }
}

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ],
}

SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": ("JWT",),
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=12),
    "REFRESH_TOKEN_LIFETIME": timedelta(hours=12),
}

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "bn_core.urls"

WSGI_APPLICATION = "bn_core.wsgi.application"

if os.getenv("USE_CLOUD_SQL_AUTH_PROXY", None):
    DATABASES = {"default": env.db()}
    DATABASES["default"]["HOST"] = "/cloudsql/beauty-now-313716:us-central1:beautnow"
    # DATABASES['default']['HOST'] = 'localhost'
    DATABASES["default"]["PORT"] = 5432
    DATABASES["default"]["ENGINE"] = "django.db.backends.postgresql"
    DATABASES["default"]["NAME"] = "beautynow"
    DATABASES["default"]["USER"] = "beautynow"
    DATABASES["default"]["PASSWORD"] = env("DB_PASS")
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "beauty_now_db_dev",
            "USER": "beauty_now_db_dev",
            "PASSWORD": "beauty_now_db_dev",
            "HOST": "localhost",
            "PORT": "5432",
        }
    }

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "America/Los_Angeles"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_ROOT = "static"
STATIC_URL = "/static/"

AUTHENTICATION_BACKENDS = (
    # Django
    "django.contrib.auth.backends.ModelBackend",
)

AUTH_USER_MODEL = "bn_app.AuthUser"

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST_USER = "registro@beautynow.mx"
EMAIL_HOST_PASSWORD = "7qFEd&9xC3R#"
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
EMAIL_HOST = "beautynow.mx"
EMAIL_PORT = 465

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"
