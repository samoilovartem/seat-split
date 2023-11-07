import logging
import time
import uuid

from loguru import logger
from rollbar.contrib.django.middleware import RollbarNotifierMiddleware


class CustomRollbarNotifierMiddleware(RollbarNotifierMiddleware):
    def get_payload_data(self, request, exc):
        payload_data = dict()

        if not request.user.is_anonymous:
            payload_data = {
                'person': {
                    'id': request.user.id,
                    'email': request.user.email,
                },
            }

        return payload_data


def logging_middleware(get_response):
    """Custom logging middleware that uses loguru logger instead of standard logging module."""

    def middleware(request):
        request_id = str(uuid.uuid4())

        with logger.contextualize(request_id=request_id):
            request.start_time = time.time()

            response = get_response(request)

            elapsed = time.time() - request.start_time

            # After the response is received
            logger.bind(
                path=request.path,
                method=request.method,
                status_code=response.status_code,
                response_size=len(response.content),
                elapsed=elapsed,
            ).info(
                "incoming '{method}' request to '{path}'",
                method=request.method,
                path=request.path,
            )

            response['X-Request-ID'] = request_id

            return response

    return middleware


class LogRequestTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger('django.request')

    def __call__(self, request):
        start_time = time.time()
        response = self.get_response(request)
        end_time = time.time()

        execution_time_ms = (end_time - start_time) * 1000
        self.logger.info(
            'Request %s completed. Execution time: %.2fms',
            request.path,
            execution_time_ms,
        )

        return response
