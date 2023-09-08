import os.path

import dj_database_url
from dotenv import load_dotenv
from split_settings.tools import include

from config.components.global_settings import BASE_DIR, DEBUG

dotenv_file = BASE_DIR / ('.env.dev' if DEBUG else '.env.prod')
if os.path.isfile(dotenv_file):
    load_dotenv(dotenv_file)

ALLOWED_HOSTS = (
    os.environ.get('ALLOWED_HOSTS', '').split(', ')
    if os.environ.get('ALLOWED_HOSTS')
    else []
)
CSRF_TRUSTED_ORIGINS = (
    os.environ.get('CSRF_TRUSTED_ORIGINS', '').split(', ')
    if os.environ.get('CSRF_TRUSTED_ORIGINS')
    else []
)
CORS_ALLOWED_ORIGINS = (
    os.environ.get('CORS_ALLOWED_ORIGINS', '').split(', ')
    if os.environ.get('CORS_ALLOWED_ORIGINS')
    else []
)

include(
    'components/rest_framework.py',
    'components/internationalization.py',
    'components/djoser.py',
    'components/rollbar.py',
    'components/simple_jwt.py',
    'components/import_export.py',
    'components/query_count.py',
    'components/django_filters.py',
    'components/swagger.py',
    'components/logger.py',
    'components/smtp_and_email.py',
)

INSTALLED_APPS = [
    # ---- Django standard apps ---- #
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # ---- Third party apps ---- #
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
    # ---- Project's apps ---- #
    'apps.users.apps.UsersConfig',
    'apps.stt.apps.SttConfig',
    'apps.email_domains.apps.EmailDomainsConfig',
]

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
    'config.middlewares.CustomRollbarNotifierMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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
        default=os.environ.get('DOCKER_PGDB_URL'),
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

STATIC_ROOT = BASE_DIR / 'static'
STATIC_URL = '/static/'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

INTERNAL_IPS = os.environ.get('INTERNAL_IPS', '').split(', ')

APPEND_SLASH = False

AUTH_USER_MODEL = 'users.User'

if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
