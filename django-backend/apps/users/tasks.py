from uuid import UUID

from apps.stt.utils import get_confirmation_link
from celery import shared_task
from config.components.smtp_and_email import (
    EMAIL_CONTENT_TYPE,
    EMAIL_FRONTEND_BASE_URL,
    EMAIL_PROJECT_NAME,
    LOGO_IMG_URL,
    SMTP2GO_FROM_EMAIL,
)
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from loguru import logger


@shared_task
def send_email_change_confirmation(user_email: str, user_id: UUID):
    """Sends email change confirmation to user using standard Django email backend."""
    mail_subject = f'{EMAIL_PROJECT_NAME} | Email change confirmation'
    message = render_to_string(
        'emails/email_change_confirmation.html',
        {
            'email': user_email,
            'link': get_confirmation_link(user_id=user_id, specific_path='email-change'),
            'project_name': EMAIL_PROJECT_NAME,
            'logo_img_url': LOGO_IMG_URL,
        },
    )
    email = EmailMessage(
        subject=mail_subject,
        body=message,
        to=[user_email],
        from_email=SMTP2GO_FROM_EMAIL,
    )
    email.content_subtype = EMAIL_CONTENT_TYPE
    try:
        email.send()
        logger.info('Email confirmation has been successfully sent to {}', user_email)
    except Exception as e:
        logger.exception(
            'There is an error sending `email confirmation` to {}. Error: {}',
            user_email,
            e,
        )
        return


@shared_task
def send_email_change_confirmed(user_email: str):
    """Sends email notifying that email change is confirmed (email has been changed)
    to user using standard Django email backend."""
    mail_subject = f'{EMAIL_PROJECT_NAME} | Your email has been changed'
    message = render_to_string(
        'emails/email_change_confirmed.html',
        {
            'email': user_email,
            'link': f'https://{EMAIL_FRONTEND_BASE_URL}/',
            'project_name': EMAIL_PROJECT_NAME,
            'logo_img_url': LOGO_IMG_URL,
        },
    )

    email = EmailMessage(
        subject=mail_subject,
        body=message,
        to=[user_email],
        from_email=SMTP2GO_FROM_EMAIL,
    )
    email.content_subtype = EMAIL_CONTENT_TYPE
    try:
        email.send()
        logger.info('`Email confirmed` has been successfully sent to {}', user_email)
    except Exception as e:
        logger.exception(
            'There is an error sending `email confirmed` to {}. Error: {}',
            user_email,
            e,
        )
        return


@shared_task
def send_password_reset_email(user_email: str, user_id: UUID):
    """Sends a password reset email to the user."""
    mail_subject = f'{EMAIL_PROJECT_NAME} | Password Reset Request'
    message = render_to_string(
        'emails/password_reset_email.html',
        {
            'email': user_email,
            'link': get_confirmation_link(user_id=user_id, specific_path='reset-password'),
            'project_name': EMAIL_PROJECT_NAME,
            'logo_img_url': LOGO_IMG_URL,
        },
    )
    email = EmailMessage(
        subject=mail_subject,
        body=message,
        to=[user_email],
        from_email=SMTP2GO_FROM_EMAIL,
    )
    email.content_subtype = EMAIL_CONTENT_TYPE
    try:
        email.send()
        logger.info('Password reset email has been successfully sent to {}', user_email)
    except Exception as e:
        logger.exception(
            'There is an error sending password reset email to {}. Error: {}',
            user_email,
            e,
        )
        return
