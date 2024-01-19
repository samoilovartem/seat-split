import os

from config.components.global_settings import DEBUG

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True') == 'True'
EMAIL_PORT = os.environ.get('EMAIL_PORT')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_PROJECT_NAME = os.environ.get('EMAIL_PROJECT_NAME')
EMAIL_FRONTEND_BASE_URL = os.environ.get('EMAIL_FRONTEND_BASE_URL')
EMAIL_CONTENT_TYPE = os.environ.get('EMAIL_CONTENT_TYPE')

SMTP2GO_FROM_EMAIL = os.environ.get('SMTP2GO_FROM_EMAIL')
SMTP2GO_SUPPORT_EMAIL = os.environ.get('SMTP2GO_SUPPORT_EMAIL')

LOGO_IMG_URL = 'https://www.seatsplit.com/_next/image?url=/_next/static/media/seat_split_logo.1977230b.png&w=1080&q=75'

if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
