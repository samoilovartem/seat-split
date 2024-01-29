import logging
import time
import uuid

from config.settings import GENERATE_EMAILS_TOKEN, HEALTH_CHECK_TOKEN
from django.http import HttpResponseBadRequest, HttpResponseForbidden
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

        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[0]
        else:
            ip_address = request.META.get('REMOTE_ADDR')

        execution_time_ms = (end_time - start_time) * 1000
        self.logger.info(
            'Request %s completed. Execution time: %.2fms, IP: %s',
            request.path,
            execution_time_ms,
            ip_address,
        )

        return response


class SimpleTokenAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if '/health-check/' in request.path:
            token = request.headers.get('Authorization')
            if not token == HEALTH_CHECK_TOKEN:
                return HttpResponseForbidden('Unauthorized')

        if '/generate_random_data_with_provided_domain_or_state/' in request.path:
            token = request.headers.get('Authorization')

            if not token:
                return HttpResponseBadRequest('No API token provided')

            try:
                split_token = token.split(' ')[1]
            except IndexError:
                return HttpResponseBadRequest('Token format is invalid')

            if not split_token == GENERATE_EMAILS_TOKEN:
                return HttpResponseForbidden('Unauthorized')

        return self.get_response(request)
