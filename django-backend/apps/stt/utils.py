from uuid import UUID

import requests
from rest_framework.exceptions import ValidationError

from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from apps.stt.models import Ticket, TicketHolderTeam
from apps.users.models import User
from config.components.slack_integration import (
    STT_NOTIFICATIONS_CHANNEL_TICKET_HOLDER_URL,
    STT_NOTIFICATIONS_CHANNEL_TICKET_URL,
    STT_NOTIFICATIONS_EMOJI,
)
from config.components.smtp_and_email import (
    EMAIL_FRONTEND_BASE_URL,
    SMTP2GO_API_BASE_URL,
    SMTP2GO_API_KEY,
    SMTP2GO_EMAIL_CONFIRMATION_TEMPLATE_ID,
    SMTP2GO_FROM_EMAIL,
)


def decode_uid(uidb64):
    """
    Decodes a URL-safe base64-encoded UUID and returns a UUID object.
    Raises a `ValidationError` if the input is not a valid UUID.
    """
    try:
        uid_str = force_str(urlsafe_base64_decode(uidb64))
        return UUID(uid_str)
    except (ValueError, TypeError, OverflowError) as e:
        raise ValidationError(f"Invalid UID: {e}")


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


def create_ticket_status_cancelled_slack_message(instance: Ticket) -> dict[str, str]:
    """Function to create the Slack message payload."""
    return {
        'text': f'Ticket {instance.id} for {instance.ticket_holder} - {instance.event} has been cancelled!',
        'blocks': [
            {
                'type': 'header',
                'text': {
                    'type': 'plain_text',
                    'text': f'Ticket Delisting Alert {STT_NOTIFICATIONS_EMOJI["TICKET_DELISTING_REQUEST"]}',
                },
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


def create_ticket_holder_team_slack_message(
    instance: TicketHolderTeam,
) -> dict[str, str]:
    """Function to create the Slack message payload for TicketHolderTeam."""
    return {
        'text': f"New Ticket Holder's Team {instance.id} for {instance.ticket_holder} - {instance.team} has been added!",
        'blocks': [
            {
                'type': 'header',
                'text': {
                    'type': 'plain_text',
                    'text': f"New Ticket Holder's Team Alert {STT_NOTIFICATIONS_EMOJI['TICKET_HOLDER_TEAM_CREATED']}",
                },
            },
            {
                'type': 'section',
                'fields': [
                    {
                        'type': 'mrkdwn',
                        'text': f"*TICKET HOLDER:*\n{instance.ticket_holder}",
                    },
                    {
                        'type': 'mrkdwn',
                        'text': f"*TICKET HOLDER ID:*\n`{instance.ticket_holder.id}`",
                    },
                    {
                        'type': 'mrkdwn',
                        'text': f"*TEAM:*\n{instance.team}",
                    },
                    {
                        'type': 'mrkdwn',
                        'text': f"*TICKET HOLDER'S TEAM ID:*\n`{instance.id}`",
                    },
                ],
            },
            {'type': 'divider'},
            {
                'type': 'section',
                'text': {
                    'type': 'mrkdwn',
                    'text': f"The above record for the ticket holder's team has been added. "
                    f"Please review the details and *confirm* the team if data is correct. \n\n"
                    f"<{STT_NOTIFICATIONS_CHANNEL_TICKET_HOLDER_URL}/{instance.ticket_holder.id}/change/|View Record>",
                },
            },
        ],
    }


def create_ticket_created_slack_message(
    ticket_holder: str,
    event: str,
    section: str,
    row: str,
    tickets_data: list[dict[str, str]],
) -> dict[str, str]:
    """Function to create the Slack message payload for newly created Tickets."""

    seats_links = [
        f"<{STT_NOTIFICATIONS_CHANNEL_TICKET_URL}/{ticket['id']}/change/|{ticket['seat']}>"
        for ticket in tickets_data
    ]
    seats_text = ", ".join(seats_links)
    tickets_data_length = len(tickets_data)

    return {
        'text': f"New Tickets for {ticket_holder} have been created!",
        'blocks': [
            {
                'type': 'header',
                'text': {
                    'type': 'plain_text',
                    'text': f"New Ticket Alert {STT_NOTIFICATIONS_EMOJI['TICKET_CREATED']}"
                    if tickets_data_length == 1
                    else f"New Tickets Alert {STT_NOTIFICATIONS_EMOJI['TICKET_CREATED']}",
                },
            },
            {
                'type': 'section',
                'fields': [
                    {
                        'type': 'mrkdwn',
                        'text': f"*TICKET HOLDER:*\n{ticket_holder}",
                    },
                    {
                        'type': 'mrkdwn',
                        'text': f"*EVENT:*\n{event}",
                    },
                    {
                        'type': 'mrkdwn',
                        'text': f"*SECTION:*\n{section}",
                    },
                    {
                        'type': 'mrkdwn',
                        'text': f"*ROW:*\n{row}",
                    },
                    {
                        'type': 'mrkdwn',
                        'text': f"*SEAT :*\n{seats_text}"
                        if tickets_data_length == 1
                        else f"*SEATS :*\n{seats_text}",
                    },
                ],
            },
            {'type': 'divider'},
            {
                'type': 'section',
                'text': {
                    'type': 'mrkdwn',
                    'text': "New ticket has been created. Please review the details and take necessary actions."
                    if tickets_data_length == 1
                    else "New tickets have been created. "
                    "Please review the details and take necessary actions.",
                },
            },
        ],
    }
