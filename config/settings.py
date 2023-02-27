import os.path
from datetime import timedelta
from pathlib import Path

import dj_database_url
from django.core.management.utils import get_random_secret_key
from dotenv import load_dotenv
from split_settings.tools import include

BASE_DIR = Path(__file__).resolve().parent.parent

dotenv_file = BASE_DIR / '.env'
if os.path.isfile(dotenv_file):
    load_dotenv(dotenv_file)

SECRET_KEY = os.environ.get('SECRET_KEY', default=get_random_secret_key())
DEBUG = os.environ.get('DEBUG', default=False) in ['True', 'true', '1']
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS').split(', ')

CORS_ALLOWED_ORIGINS = os.environ.get('CORS_ALLOWED_ORIGINS').split(', ')

include(
    'components/rest_framework.py',
    'components/internationalization.py',
    'components/djoser.py',
    'components/rollbar.py',
    'components/simple_jwt.py',
    'components/import_export.py',
    'components/query_count.py',
    'components/django-filters.py',
    'components/swagger.py',
)

INSTALLED_APPS = [
    # Third party apps that needs to be placed before standard apps
    # Django standard apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third party apps
    'drf_yasg',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_api_key',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'djoser',
    'django_filters',
    'import_export',
    'django_truncate',
    'corsheaders',
    'simple_history',
    # Project's apps
    'apps.cards.apps.CardsConfig',
    'apps.accounts.apps.AccountsConfig',
    'apps.users.apps.UsersConfig',
    'apps.mobile_numbers.apps.MobileNumbersConfig',
]

if DEBUG:
    INSTALLED_APPS.append('debug_toolbar')

ROOT_URLCONF = 'config.urls'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'rollbar.contrib.django.middleware.RollbarNotifierMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
]

if DEBUG:
    MIDDLEWARE.append('querycount.middleware.QueryCountMiddleware')
    MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('PGDB_URL')
        if os.environ.get('IS_DOCKER_RUNNING')
        else os.environ.get('SQLITE_PATH'),
        ssl_require=False if DEBUG else True,
        conn_max_age=600,
    )
}

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

if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

CSRF_TRUSTED_ORIGINS = os.environ.get('CSRF_TRUSTED_ORIGINS').split(', ')

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

INTERNAL_IPS = os.environ.get('INTERNAL_IPS').split(', ')
if DEBUG:
    # showing django-debug-toolbar in docker development container
    INTERNAL_IPS = type(str('c'), (), {'__contains__': lambda *a: True})()

APPEND_SLASH = False

AUTH_USER_MODEL = 'users.User'

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': True,
#     'filters': {
#         'require_debug_true': {
#             '()': 'django.utils.log.RequireDebugTrue',
#         }
#     },
#     'formatters': {
#         'default': {
#             'format': '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]',
#         },
#     },
#     'handlers': {
#         'debug-console': {
#             'class': 'logging.StreamHandler',
#             'formatter': 'default',
#             'filters': ['require_debug_true'],
#         },
#     },
#     'loggers': {
#         'django.db.backends': {
#             'level': 'DEBUG',
#             'handlers': ['debug-console'],
#             'propagate': False,
#         }
#     },
# }
