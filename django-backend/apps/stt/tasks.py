from uuid import UUID

from celery import shared_task
from loguru import logger
from slack_sdk.errors import SlackApiError

from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from apps.stt.utils import get_confirmation_link
from config.components.slack_integration import slack_client
from config.components.smtp_and_email import (
    EMAIL_CONTENT_TYPE,
    EMAIL_FRONTEND_BASE_URL,
    EMAIL_PROJECT_NAME,
    SMTP2GO_FROM_EMAIL,
)


@shared_task
def send_email_confirmation(user_email: str, user_id: UUID):
    """Sends email confirmation to user using standard Django email backend."""
    # time.sleep(CELERY_GENERAL_SLEEP_TIME)

    mail_subject = f'Activate your account in {EMAIL_PROJECT_NAME}'
    message = render_to_string(
        'emails/account_verification.html',
        {
            'email': user_email,
            'link': get_confirmation_link(user_id=user_id),
            'project_name': EMAIL_PROJECT_NAME,
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
def send_email_confirmed(user_email: str):
    """Sends email notifying that email is confirmed to user using standard Django email backend."""
    # time.sleep(CELERY_GENERAL_SLEEP_TIME)

    mail_subject = f'Your account in {EMAIL_PROJECT_NAME} is confirmed'
    message = render_to_string(
        'emails/account_verified.html',
        {
            'email': user_email,
            'link': f'https://{EMAIL_FRONTEND_BASE_URL}/',
            'project_name': EMAIL_PROJECT_NAME,
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
def send_ticket_holder_team_confirmed(user_email: str, team_name: str):
    """Sends email notifying that ticket holder team is confirmed to user using standard Django email backend."""
    # time.sleep(CELERY_GENERAL_SLEEP_TIME)

    mail_subject = f'Your team "{team_name}" data has been verified'
    message = render_to_string(
        'emails/ticket_holder_team_confirmed.html',
        {
            'email': user_email,
            'team_name': team_name,
            'link': f'https://{EMAIL_FRONTEND_BASE_URL}/',
            'project_name': EMAIL_PROJECT_NAME,
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
        logger.info(
            '`Ticket holder team confirmed` has been successfully sent to {}',
            user_email,
        )
    except Exception as e:
        logger.exception(
            'There is an error sending `ticket holder team confirmed` to {}. Error: {}',
            user_email,
            e,
        )
        return


@shared_task
def send_slack_notification(message: dict[str, str], channel: str, icon_emoji: str):
    try:
        slack_client.chat_postMessage(
            channel=channel,
            text=message['text'],
            blocks=message['blocks'],
            icon_emoji=icon_emoji,
        )
    except SlackApiError as e:
        logger.error('There is an error sending a notification to slack. Error: {}', e)
