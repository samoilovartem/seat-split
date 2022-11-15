from .common import *
from pathlib import Path
from . import local

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = local.SECRET_KEY
ALLOWED_HOSTS = []
DEBUG = True


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]


# Standard Database

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


# DATABASES = {
#     'default': {
#         'ENGINE': local.PSQL_ENGINE,
#         'NAME': local.PSQL_NAME,
#         'USER': local.PSQL_USER,
#         'PASSWORD': local.PSQL_PASSWORD,
#         'HOST': local.PSQL_HOST,
#         'PORT': local.PSQL_PORT,
#     }
# }

# DOCKER POSTGRES

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'postgres',
#         'USER': 'postgres',
#         'PASSWORD': 'postgres',
#         'HOST': 'pgdb',
#         'PORT': 5432
#     }
# }


# USE IT ONLY FOR LOCAL / DOCKER DEVELOPMENT
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'config/static')
]

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda request: DEBUG,
}

DJANGO_TABLES2_TEMPLATE = "django_tables2/bootstrap-responsive.html"

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

SIMPLE_JWT['SIGNING_KEY'] = SECRET_KEY



