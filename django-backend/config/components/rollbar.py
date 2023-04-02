import os

from config.components.global_settings import BASE_DIR, DEBUG

ROLLBAR = {
    'access_token': os.environ.get('ROLLBAR_ACCESS_TOKEN'),
    'environment': 'development' if DEBUG else 'production',
    'code_version': '1.0',
    'root': BASE_DIR,
}
