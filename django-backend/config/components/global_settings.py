import os

from pathlib import Path

from django.core.management.utils import get_random_secret_key

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DEBUG = os.environ.get('DEBUG', default=False) in ['True', 'true', '1']
SECRET_KEY = os.environ.get('SECRET_KEY', default=get_random_secret_key())

DJANGO_HOST_URL = os.environ.get('DJANGO_HOST_URL')
