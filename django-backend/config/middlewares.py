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
