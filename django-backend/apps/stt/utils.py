from uuid import UUID

import requests

from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from apps.stt.models import Ticket
from apps.users.models import User
from config.components.slack_integration import STT_NOTIFICATIONS_CHANNEL_TICKET_URL
from config.components.smtp_and_email import (
    EMAIL_FRONTEND_BASE_URL,
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


def get_confirmation_link(user_id: UUID):
    """Returns link for email confirmation."""
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        raise ValueError('No such user exists.')

    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    confirmation_link = (
        f'https://{EMAIL_FRONTEND_BASE_URL}/api/confirm-email?uid={uid}&token={token}'
    )

    return confirmation_link


def create_slack_message(instance: Ticket) -> dict[str, str]:
    """Function to create the Slack message payload."""
    return {
        'text': f'Ticket {instance.id} for {instance.ticket_holder} - {instance.event} has been cancelled!',
        'blocks': [
            {
                'type': 'header',
                'text': {'type': 'plain_text', 'text': 'Ticket Delisting Alert'},
            },
            {
                'type': 'section',
                'fields': [
                    {
                        'type': 'mrkdwn',
                        'text': f'*TICKET HOLDER:*\n{instance.ticket_holder}',
                    },
                    {'type': 'mrkdwn', 'text': f'*ID:*\n`{instance.ticket_holder.id}`'},
                    {'type': 'mrkdwn', 'text': f'*EVENT:*\n{instance.event}'},
                    {'type': 'mrkdwn', 'text': f'*TICKET ID:*\n`{instance.id}`'},
                ],
            },
            {'type': 'divider'},
            {
                'type': 'section',
                'text': {
                    'type': 'mrkdwn',
                    'text': f'The above ticket has been requested for delisting. Please take necessary '
                    f'actions. \n\n<{STT_NOTIFICATIONS_CHANNEL_TICKET_URL}/{instance.id}/change/|View Ticket>',
                },
            },
        ],
    }
