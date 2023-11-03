import os

import redis

REDIS_URL = os.environ.get('REDIS_URL', 'redis://127.0.0.1:6379')
BROKER_CONNECTION_MAX_RETRIES = os.environ.get('BROKER_CONNECTION_MAX_RETRIES', None)
BROKER_POOL_LIMIT = os.environ.get('BROKER_POOL_LIMIT', 5)
REDIS_NEW_TICKETS_KEY_EXPIRE = os.environ.get('REDIS_NEW_TICKETS_KEY_EXPIRE', 300)

redis_connection = redis.from_url(REDIS_URL, db=0)
