from decimal import Decimal
from uuid import UUID

from celery import shared_task
from loguru import logger

from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from apps.stt.utils import calculate_price_with_expenses, get_confirmation_link
from config.components.smtp_and_email import (
    EMAIL_CONTENT_TYPE,
    EMAIL_FRONTEND_BASE_URL,
    EMAIL_PROJECT_NAME,
    LOGO_IMG_URL,
    SMTP2GO_FROM_EMAIL,
)


@shared_task
def send_email_confirmation(user_email: str, user_id: UUID):
    """Sends email confirmation to user using standard Django email backend."""
    mail_subject = f'Activate your account in {EMAIL_PROJECT_NAME}'
    message = render_to_string(
        'emails/account_verification.html',
        {
            'email': user_email,
            'link': get_confirmation_link(user_id=user_id, specific_path='confirm-email'),
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
def send_email_confirmed(user_email: str):
    """Sends email notifying that email is confirmed to user using standard Django email backend."""
    mail_subject = f'Your account in {EMAIL_PROJECT_NAME} is confirmed'
    message = render_to_string(
        'emails/account_verified.html',
        {
            'email': user_email,
            'link': f'https://{EMAIL_FRONTEND_BASE_URL}/',  # noqa: E231
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
def send_ticket_holder_team_confirmed(user_email: str, team_name: str):
    """Sends email notifying that ticket holder team is confirmed to user using standard Django email backend."""
    mail_subject = f'Your team "{team_name}" data has been verified'
    message = render_to_string(
        'emails/ticket_holder_team_confirmed.html',
        {
            'email': user_email,
            'team_name': team_name,
            'link': f'https://{EMAIL_FRONTEND_BASE_URL}/',  # noqa: E231
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
def send_ticket_sold_email(
    ticket_holder_email: str,
    event_name: str,
    event_date: str,
    section: str,
    row: str,
    seat: str,
    price: Decimal,
) -> None:
    """Sends email notification that ticket holder's ticket has been sold."""
    mail_subject = 'Your ticket has been sold'
    message = render_to_string(
        'emails/ticket_sold.html',
        {
            'event_name': event_name,
            'event_date': event_date,
            'section': section,
            'row': row,
            'seat': seat,
            'price': calculate_price_with_expenses(price),
            'project_name': EMAIL_PROJECT_NAME,
            'logo_img_url': LOGO_IMG_URL,
        },
    )

    email = EmailMessage(
        subject=mail_subject,
        body=message,
        to=[ticket_holder_email],
        from_email=SMTP2GO_FROM_EMAIL,
    )
    email.content_subtype = EMAIL_CONTENT_TYPE
    try:
        email.send()
        logger.info(
            '`Ticket sold` email has been successfully sent to {}',
            ticket_holder_email,
        )
    except Exception as e:
        logger.exception(
            'There is an error sending `ticket sold` email to {}. Error: {}',
            ticket_holder_email,
            e,
        )
        return
