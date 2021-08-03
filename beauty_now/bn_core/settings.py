import os
from datetime import timedelta


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '2mcb5#xm33_*ozkyqm!e4n_t2vq#&rrlx+vr^cmghtv7)h9t$t'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# ALLOWED_HOSTS
ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    'beauty-now-api.herokuapp.com',
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bn_app',
    'bn_utils',
    'rest_framework',
    'rest_framework.authtoken',
    'oauth2_provider',
    'social_django',
    'rest_framework_social_oauth2',
    'djoser',
    'corsheaders'
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'bn_app/html')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

OAUTH2_PROVIDER = {
    # this is the list of available scopes
    'SCOPES': {'read': 'Read scope', 'write': 'Write scope', 'groups': 'Access to your groups'}
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',  # django-oauth-toolkit >= 1.0.0
        'rest_framework_social_oauth2.authentication.SocialAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
}

SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('JWT',),
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=12),
    'REFRESH_TOKEN_LIFETIME': timedelta(hours=12),
}

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware'
]

ROOT_URLCONF = 'bn_core.urls'

WSGI_APPLICATION = 'bn_core.wsgi.application'


# DATABASES
DATABASES = {
    'default': {
        'ENGINE': os.environ.get('SQL_ENGINE', 'django.db.backends.postgresql'),
        'NAME': os.environ.get('SQL_DATABASE', 'beauty_now_db_dev'),
        'USER': os.environ.get('SQL_USER', 'beauty_now_db_dev'),
        'PASSWORD': os.environ.get('SQL_PASSWORD', 'beauty_now_db_dev'),
        'HOST': os.environ.get('SQL_HOST', 'localhost'),
        'PORT': os.environ.get('SQL_PORT', '5432'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Los_Angeles'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_ROOT = 'static'
STATIC_URL = '/static/'


# CORS_ORIGIN_WHITELIST
CORS_ORIGIN_WHITELIST = [
    'http://localhost:8100',
    'https://localhost:8100',
    'https://beauty-now-client.herokuapp.com',
]

AUTHENTICATION_BACKENDS = (
    # Facebook
    'social_core.backends.facebook.FacebookAppOAuth2',
    'social_core.backends.facebook.FacebookOAuth2',
    # Google
    'social_core.backends.google.GoogleOAuth2',
    # Django Rest Framework
    'rest_framework_social_oauth2.backends.DjangoOAuth2',
    # Django
    'django.contrib.auth.backends.ModelBackend',
)

AUTH_USER_MODEL = 'bn_app.AuthUser'

# FACEBOOK
SOCIAL_AUTH_FACEBOOK_KEY = '435891111073407'
SOCIAL_AUTH_FACEBOOK_SECRET = '05893ed4a038e05bab84bf9dce59c0fb'
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']

SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
    'fields': 'id, name, email'
}

# Google config
# SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '1029659652093-a0m8ab8i3kupn9hetvf140ut049r477u.apps.googleusercontent.com'
# SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'of72yGw80_lCzdWHIlyuh985'

# Define SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE to get extra permissions from Google.
# SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    # 'https://www.googleapis.com/auth/userinfo.email',
    # 'https://www.googleapis.com/auth/userinfo.profile',
# ]

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST_USER = 'registro@beautynow.mx'
EMAIL_HOST_PASSWORD = '7qFEd&9xC3R#'
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
EMAIL_HOST = 'beautynow.mx'
EMAIL_PORT = 465

DJOSER = {
    'PASSWORD_RESET_CONFIRM_URL': 'password/reset/confirm/{uid}/{token}',
    'USERNAME_RESET_CONFIRM_URL': 'username/reset/confirm/{uid}/{token}',
    'ACTIVATION_URL': 'activate/{uid}/{token}',
    'SEND_ACTIVATION_EMAIL': True,
    'SEND_CONFIRMATION_EMAIL': True,
    'PASSWORD_CHANGED_EMAIL_CONFIRMATION': True,
    'USERNAME_CHANGED_EMAIL_CONFIRMATION': True,
    'SERIALIZERS': {
        'user_create': 'bn_app.serializers.UserCreateSerializer'
    },
}

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
