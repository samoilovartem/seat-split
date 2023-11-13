import re
from logging import Filter

from config.components.global_settings import DEBUG


class SensitiveInfoFilter(Filter):
    def filter(self, record):
        if hasattr(record, 'msg'):
            # This pattern looks for any key that contains 'password'
            pattern = r'(".*password"\s*:\s*")([^"]+)'
            replacement = r'\1********'
            record.msg = re.sub(pattern, replacement, record.msg)

            # Handle the case where the log message is a bytes object
            if isinstance(record.msg, bytes):
                decoded_msg = record.msg.decode('utf-8')
                masked_msg = re.sub(pattern, replacement, decoded_msg)
                record.msg = masked_msg.encode('utf-8')
        return True


LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S",
        },
    },
    'filters': {
        'mask_sensitive': {
            '()': 'config.components.logger.SensitiveInfoFilter',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
            'filters': ['mask_sensitive'],
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'WARN',
            'propagate': True,
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'WARN',
            'propagate': False,
        },
        'website': {
            'handlers': ['console'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': False,
        },
    },
}
