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


DATABASES = {
    'default': {
        'ENGINE': local.DB_ENGINE,
        'NAME': local.DB_NAME,
        'USER': local.DB_USER,
        'PASSWORD': local.DB_PASSWORD,
        'HOST': local.DB_HOST,
        'PORT': local.DB_PORT,
    }
}


