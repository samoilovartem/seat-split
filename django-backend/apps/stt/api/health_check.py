import redis
from celery.result import AsyncResult

from django.db import connections
from django.db.utils import OperationalError
from django.http import JsonResponse

from apps.stt.tasks import celery_ping
from config.components.redis import redis_connection


def health_check(request):
    db_conn = connections['default']
    try:
        db_conn.cursor()
        db_status = 'PostgreSQL connected'
    except OperationalError:
        db_status = 'PostgreSQL connection failed'

    try:
        redis_connection.ping()
        redis_status = 'Redis connected'
    except (redis.exceptions.ConnectionError, redis.exceptions.BusyLoadingError):
        redis_status = 'Redis connection failed'

    try:
        task = celery_ping.delay()
        result = AsyncResult(task.id)
        if result.get(timeout=10) == 'pong':
            celery_status = 'Celery connected'
        else:
            celery_status = 'Celery task failed'
    except Exception as e:
        celery_status = f'Celery connection failed: {str(e)}'

    return JsonResponse(
        {'database': db_status, 'redis': redis_status, 'celery': celery_status}
    )
