import json
from datetime import timedelta
from decimal import Decimal
from uuid import UUID

from celery import shared_task
from django_celery_results.models import TaskResult
from loguru import logger
from slack_sdk.errors import SlackApiError

from django.core.mail import EmailMessage
from django.core.management import call_command
from django.template.loader import render_to_string
from django.utils.timezone import now

from apps.stt.services.github_issues_reporter import GitHubIssuesReporter
from apps.stt.utils import (
    calculate_price_with_expenses,
    create_ticket_created_slack_message,
    get_confirmation_link,
)
from config.components.business_related import GITHUB_ACCESS_TOKEN
from config.components.celery import (
    CELERY_GENERAL_COUNTDOWN,
    CELERY_TASK_RESULT_MAX_AGE,
)
from config.components.redis import redis_celery_connection
from config.components.slack_integration import (
    STT_NOTIFICATIONS_CHANNEL_ID,
    STT_WEEKLY_ISSUES_REPO_NAMES,
    STT_WEEKLY_ISSUES_REPORT_CHANNEL_ID,
    slack_client,
)
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
            'link': get_confirmation_link(
                user_id=user_id, specific_path='confirm-email'
            ),
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
def send_slack_notification(message: dict[str, str], channel: str) -> None:
    try:
        slack_client.chat_postMessage(
            channel=channel,
            text=message['text'],
            blocks=message['blocks'],
        )
    except SlackApiError as e:
        logger.error('There is an error sending a notification to slack. Error: {}', e)


@shared_task
def send_aggregated_slack_notification(event_id: UUID, ticket_holder_id: UUID) -> None:
    redis_key = f'new_tickets_{event_id}_{ticket_holder_id}'

    raw_tickets_data = redis_celery_connection.lrange(redis_key, 0, -1)
    tickets_data = [json.loads(data.decode('utf-8')) for data in raw_tickets_data]
    redis_celery_connection.delete(redis_key)

    if tickets_data:
        representative_ticket_data = tickets_data[0]

        message_payload = create_ticket_created_slack_message(
            ticket_holder=representative_ticket_data['ticket_holder'],
            event=representative_ticket_data['event'],
            section=representative_ticket_data['section'],
            row=representative_ticket_data['row'],
            tickets_data=tickets_data,
        )

        try:
            slack_client.chat_postMessage(
                channel=STT_NOTIFICATIONS_CHANNEL_ID, **message_payload
            )
        except SlackApiError as e:
            logger.error(
                'There is an error sending a notification to slack. Error: {}', e
            )


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


@shared_task
def custom_backend_result_cleanup(max_age: int = None) -> None:
    """Custom backend result cleanup task."""
    if max_age is not None:
        max_age = timedelta(days=max_age)
    else:
        max_age = CELERY_TASK_RESULT_MAX_AGE

    expiration_time = now() - max_age
    TaskResult.objects.filter(date_done__lt=expiration_time).delete()


@shared_task
def fetch_and_send_issues_report():
    """
    Fetches closed issues from GitHub and sends a report in multiple Slack messages if needed.
    Important: executes every Sunday.
    """
    reporter = GitHubIssuesReporter(GITHUB_ACCESS_TOKEN)
    issues_by_user = reporter.generate_report(STT_WEEKLY_ISSUES_REPO_NAMES)

    slack_messages = reporter.format_slack_messages(issues_by_user)

    for message in slack_messages:
        send_slack_notification.apply_async(
            args=(message, STT_WEEKLY_ISSUES_REPORT_CHANNEL_ID),
            countdown=CELERY_GENERAL_COUNTDOWN,
        )


@shared_task
def clean_duplicate_history(minutes=None, excluded_fields=None, use_base_manager=False):
    """Removes duplicate historical records."""
    command_options = {'auto': True}
    if minutes:
        command_options['minutes'] = minutes
    if excluded_fields:
        command_options['excluded_fields'] = excluded_fields
    if use_base_manager:
        command_options['base_manager'] = True

    logger.info('Cleaning duplicate history...')
    call_command('clean_duplicate_history', **command_options)
    logger.info('Cleaning duplicate history finished.')


@shared_task
def clean_old_history(days=30):
    """Removes historical records that have existed for a certain amount of time."""
    logger.info('Cleaning old history...')
    call_command('clean_old_history', auto=True, days=days)
    logger.info('Cleaning old history finished.')
