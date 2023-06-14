import logging

from config.components.global_settings import DEBUG


class ColorizedFormatter(logging.Formatter):
    GREEN = '\033[32m'
    RESET = '\033[0m'

    def format(self, record):
        message = super().format(record)
        if 'django.db.backends' in record.name:
            return self.GREEN + message + self.RESET
        return message


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'colorized': {
            '()': ColorizedFormatter,
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG' if DEBUG else 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'colorized',
        },
    },
    'loggers': {
        'django': {
            'level': 'DEBUG' if DEBUG else 'INFO',
            'handlers': ['console'],
        },
        'django.db.backends': {
            'level': 'DEBUG' if DEBUG else 'INFO',
            'handlers': ['console'],
            'propagate': False,
        },
        'django.utils.autoreload': {
            'level': 'WARNING',
            'handlers': ['console'],
            'propagate': False,
        },
    },
}
