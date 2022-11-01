import os.path
from pathlib import Path
from . import local_settings

BASE_DIR = Path(__file__).resolve().parent.parent

# ---- HEROKU SETTINGS ----

IS_HEROKU = "DYNO" in os.environ

# SECRET_KEY = os.environ['SECRET_KEY']
SECRET_KEY = 'jango-insecure-yne8=gdjs4e555#ll)-149lm+%f6o2vi-%0l33#pk)ma!m@+o('

if 'SECRET_KEY' in os.environ:
    SECRET_KEY = os.environ["SECRET_KEY"]

if IS_HEROKU:
    ALLOWED_HOSTS = ["*"]
else:
    ALLOWED_HOSTS = []

if not IS_HEROKU:
    DEBUG = True

# ---- END OF HEROKU SETTINGS ----


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
    'accounts_team.apps.AccountsTeamConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # USE WHITENOISE ONLY FOR HEROKU DEPLOYMENT!!!
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
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


# Database

# DATABASES = {
#     'default': {
#         # 'ENGINE': 'django.db.backends.sqlite3',
#         # 'NAME': BASE_DIR / 'db.sqlite3',
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'db_lewanddowski',
#         'USER': 'usr_devmysql',
#         'PASSWORD': 'x5p5d43xsteD',
#         'HOST': 'mysql.diseasediagnostic.com',
#         'PORT': 3306
#     }
# }

# POSTGRES

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

# ---- DOCKER DB SETTINGS ----

# DATABASES = {
#     'default': {
#         'ENGINE': local_settings.DB_ENGINE,
#         'NAME': local_settings.DB_NAME,
#         'USER': local_settings.DB_USER,
#         'PASSWORD': local_settings.DB_PASSWORD,
#         'HOST': local_settings.DB_HOST,
#         'PORT': local_settings.DB_PORT,
#     }
# }

# ---- END DOCKER DB SETTINGS ----


# ---- HEROKU DB SETTINGS ----

DATABASES = {
    'default': {
        'ENGINE': os.environ['DB_ENGINE'],
        'NAME': os.environ['DB_NAME'],
        'USER': os.environ['DB_USER'],
        'PASSWORD': os.environ['DB_PASSWORD'],
        'HOST': os.environ['DB_HOST'],
        'PORT': os.environ['DB_PORT'],
    }
}

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
# STATIC_ROOT = BASE_DIR / "staticfiles"
STATIC_URL = 'static/'

# USE IT ONLY FOR LOCAL / DOCKER DEVELOPMENT
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'mysite/static')
# ]


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

INTERNAL_IPS = ["127.0.0.1"]
APPEND_SLASH = False

# DEBUG_TOOLBAR_CONFIG = {
#     'SHOW_TOOLBAR_CALLBACK': lambda request: DEBUG,
# }
