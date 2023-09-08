import requests

from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from config.components.smtp_and_email import (
    SMTP2GO_API_BASE_URL,
    SMTP2GO_API_KEY,
    SMTP2GO_EMAIL_CONFIRMATION_TEMPLATE_ID,
    SMTP2GO_FROM_EMAIL,
)


def send_email_confirmation_with_api(
    to: list, confirm_url: str, sender: str = SMTP2GO_FROM_EMAIL
):
    url = f'{SMTP2GO_API_BASE_URL}/email/send'
    data = {
        'api_key': SMTP2GO_API_KEY,
        'to': to,
        'sender': sender,
        'template_id': SMTP2GO_EMAIL_CONFIRMATION_TEMPLATE_ID,
        'template_data': {'confirm_url': confirm_url},
    }

    try:
        requests.post(url, json=data)
    except requests.exceptions.RequestException as e:
        print(e)  # TODO: replace with logger
        return


def get_confirmation_link(request, user):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    domain = get_current_site(request).domain
    confirmation_link = f'{"https" if request.is_secure() else "http"}://{domain}/confirm-email/{uid}/{token}/'
    return confirmation_link
