import requests
from rest_framework.request import Request

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from apps.users.models import User
from config.components.smtp_and_email import (
    EMAIL_CONTENT_TYPE,
    EMAIL_FRONTEND_BASE_URL,
    EMAIL_PROJECT_NAME,
    SMTP2GO_API_BASE_URL,
    SMTP2GO_API_KEY,
    SMTP2GO_EMAIL_CONFIRMATION_TEMPLATE_ID,
    SMTP2GO_FROM_EMAIL,
)


def send_email_confirmation_with_api(
    to: list, confirm_url: str, sender: str = SMTP2GO_FROM_EMAIL
):
    """Sends email confirmation to user using SMTP2GO API."""
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


def send_email_confirmation(request: Request, user: User):
    """Sends email confirmation to user using standard Django email backend."""
    mail_subject = f'Activate your account in {EMAIL_PROJECT_NAME}'
    message = render_to_string(
        'emails/account_verification.html',
        {
            'email': user.email,
            'link': get_confirmation_link(request, user),
            'project_name': EMAIL_PROJECT_NAME,
        },
    )
    to_email = user.email
    email = EmailMessage(
        subject=mail_subject,
        body=message,
        to=[to_email],
        from_email=SMTP2GO_FROM_EMAIL,
    )
    email.content_subtype = EMAIL_CONTENT_TYPE
    try:
        email.send()
    except Exception as e:
        print(e)  # TODO: replace with logger
        return


def send_email_confirmed(request: Request, user: User):
    """Sends email notifying that email is confirmed to user using standard Django email backend."""
    mail_subject = f'Your account in {EMAIL_PROJECT_NAME} is confirmed'
    message = render_to_string(
        'emails/account_verified.html',
        {
            'email': user.email,
            'link': f'{"https" if request.is_secure() else "http"}://{EMAIL_FRONTEND_BASE_URL}/',
            'project_name': EMAIL_PROJECT_NAME,
        },
    )
    to_email = user.email
    email = EmailMessage(
        subject=mail_subject,
        body=message,
        to=[to_email],
        from_email=SMTP2GO_FROM_EMAIL,
    )
    email.content_subtype = EMAIL_CONTENT_TYPE
    try:
        email.send()
    except Exception as e:
        print(e)
        return


def get_confirmation_link(request: Request, user: User):
    """Returns link for email confirmation."""
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    confirmation_link = f'{"https" if request.is_secure() else "http"}://{EMAIL_FRONTEND_BASE_URL}/api/confirm-email/{uid}/{token}/'
    return confirmation_link
