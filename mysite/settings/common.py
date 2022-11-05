import os.path
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent.parent


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_tables2',
    'rest_framework',
    'debug_toolbar',
    'django_filters',
    'crispy_bootstrap5',
    'crispy_forms',
    'bootstrap5',
    'accounts_team.apps.AccountsTeamConfig',
]


ROOT_URLCONF = 'mysite.urls'

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

WSGI_APPLICATION = 'mysite.wsgi.application'



# if "DATABASE_URL" in os.environ:
#     # Configure Django for DATABASE_URL environment variable.
#     DATABASES["default"] = dj_database_url.config(
#         conn_max_age=MAX_CONN_AGE, ssl_require=True)
#
#     # Enable test database if found in CI environment.
#     if "CI" in os.environ:
#         DATABASES["default"]["TEST"] = DATABASES["default"]
#

# ---- END OF HEROKU DB SETTINGS ----

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


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = 'static/'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

INTERNAL_IPS = ["127.0.0.1"]
APPEND_SLASH = False
