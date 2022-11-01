import os.path
from pathlib import Path
# from .local_settings import SECRET_KEY, DB_ENGINE, DB_USER, DB_PASSWORD, DB_HOST, DB_NAME, DB_PORT

BASE_DIR = Path(__file__).resolve().parent.parent

# ---- HEROKU SETTINGS ----

IS_HEROKU = "DYNO" in os.environ

SECRET_KEY = 'django-insecure-yne8=gdjs4e555#ll)-149lm+%f6o2vi-%0l33#pk)ma!m@+o('
if 'SECRET_KEY' in os.environ:
    SECRET_KEY = os.environ["SECRET_KEY"]

if IS_HEROKU:
    ALLOWED_HOSTS = ["*"]
else:
    ALLOWED_HOSTS = []

if not IS_HEROKU:
    DEBUG = True

# ---- END OF HEROKU SETTINGS ----

# SECRET_KEY = os.environ['SECRET_KEY']
# DEBUG = os.environ['DEBUG']
# ALLOWED_HOSTS = os.environ['ALLOWED_HOSTS']



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


# DATABASES = {
#     'default': {
#         'ENGINE': DB_ENGINE,
#         'NAME': DB_NAME,
#         'USER': DB_USER,
#         'PASSWORD': DB_PASSWORD,
#         'HOST': DB_HOST,
#         'PORT': DB_PORT,
#     }
# }


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


# STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_ROOT = BASE_DIR / "staticfiles"
STATIC_URL = 'static/'

# DON'T USE THIS ON HEROKU DEPLOY
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'mysite/static')
# ]

# Enable WhiteNoise's GZip compression of static assets.
# STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# DJANGO_TABLES2_TEMPLATE = "django_tables2/bootstrap-responsive.html"

INTERNAL_IPS = ["127.0.0.1"]
APPEND_SLASH = False

# DEBUG_TOOLBAR_CONFIG = {
#     'SHOW_TOOLBAR_CALLBACK': lambda request: DEBUG,
# }
