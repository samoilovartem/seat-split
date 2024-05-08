from decimal import Decimal
from uuid import UUID

from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework.authtoken.models import Token

from apps.stt.models import Ticket, TicketHolderTeam
from apps.users.models import User
from config.components.business_related import EXPENSES_MULTIPLIER
from config.components.slack_integration import (
    STT_NOTIFICATIONS_CHANNEL_TICKET_HOLDER_URL,
    STT_NOTIFICATIONS_CHANNEL_TICKET_URL,
    STT_NOTIFICATIONS_EMOJI,
)
from config.components.smtp_and_email import EMAIL_FRONTEND_BASE_URL


def calculate_price_with_expenses(price: Decimal | None) -> str | None:
    """
    Calculate the price including expenses.

    This function takes the original price and applies an expenses multiplier
    to it, then returns the result as a string formatted to two decimal places.
    If the price is None, it returns None, indicating that no calculation is needed.

    Parameters:
    price (Decimal | None): The original price of the ticket.

    Returns:
    str | None: The price including expenses, formatted as a string,
                    or None if the input price is None.
    """
    if price is not None:
        expenses_multiplier = Decimal(EXPENSES_MULTIPLIER)
        return str((price * expenses_multiplier).quantize(Decimal('0.01')))
    return None


def invalidate_user_auth_token(user: User) -> None:
    """
    Invalidate the authentication token for the given user.

    :param user: User instance for which to invalidate the token.
    """
    Token.objects.filter(user=user).delete()


def get_confirmation_link(user_id: UUID, specific_path: str):
    """Returns link for email confirmation."""
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        raise ValueError('No such user exists.')

    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))

    confirmation_link = f'https://{EMAIL_FRONTEND_BASE_URL}/api/{specific_path}?uid={uid}&token={token}'  # noqa: E231

    return confirmation_link


def create_ticket_status_requested_for_delisting_slack_message(
    instance: Ticket,
) -> dict[str, str]:
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
                        'text': f'*TICKET HOLDER:*\n{instance.ticket_holder}',  # noqa: E231
                    },
                    {
                        'type': 'mrkdwn',
                        'text': f'*ID:*\n`{instance.ticket_holder.id}`',  # noqa: E231
                    },
                    {
                        'type': 'mrkdwn',
                        'text': f'*EVENT:*\n{instance.event}',  # noqa: E231
                    },
                    {
                        'type': 'mrkdwn',
                        'text': f'*TICKET ID:*\n`{instance.id}`',  # noqa: E231
                    },
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
        'text': f"New Ticket Holder's Team {instance.id} for "
        f'{instance.ticket_holder} - {instance.team} has been added!',
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
                        'text': f'*TICKET HOLDER:*\n{instance.ticket_holder}',  # noqa: E231
                    },
                    {
                        'type': 'mrkdwn',
                        'text': f'*TICKET HOLDER ID:*\n`{instance.ticket_holder.id}`',  # noqa: E231
                    },
                    {
                        'type': 'mrkdwn',
                        'text': f'*TEAM:*\n{instance.team}',  # noqa: E231
                    },
                    {
                        'type': 'mrkdwn',
                        'text': f"*TICKET HOLDER'S TEAM ID:*\n`{instance.id}`",  # noqa: E231
                    },
                ],
            },
            {'type': 'divider'},
            {
                'type': 'section',
                'text': {
                    'type': 'mrkdwn',
                    'text': f"The above record for the ticket holder's team has been added. "
                    f'Please review the details and *confirm* the team if data is correct. \n\n'
                    f'<{STT_NOTIFICATIONS_CHANNEL_TICKET_HOLDER_URL}/{instance.ticket_holder.id}/change/|View Record>',
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
    seats_text = ', '.join(seats_links)
    tickets_data_length = len(tickets_data)

    return {
        'text': f'New Tickets for {ticket_holder} have been created!',
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
                        'text': f'*TICKET HOLDER:*\n{ticket_holder}',  # noqa: E231
                    },
                    {
                        'type': 'mrkdwn',
                        'text': f'*EVENT:*\n{event}',  # noqa: E231
                    },
                    {
                        'type': 'mrkdwn',
                        'text': f'*SECTION:*\n{section}',  # noqa: E231
                    },
                    {
                        'type': 'mrkdwn',
                        'text': f'*ROW:*\n{row}',  # noqa: E231
                    },
                    {
                        'type': 'mrkdwn',
                        'text': f'*SEAT:*\n{seats_text}'  # noqa: E231
                        if tickets_data_length == 1
                        else f'*SEATS:*\n{seats_text}',  # noqa: E231
                    },
                ],
            },
            {'type': 'divider'},
            {
                'type': 'section',
                'text': {
                    'type': 'mrkdwn',
                    'text': 'New ticket has been created. Please review the details and take necessary actions.'
                    if tickets_data_length == 1
                    else 'New tickets have been created. '
                    'Please review the details and take necessary actions.',
                },
            },
        ],
    }


def create_ticket_relisted_slack_message(ticket: Ticket) -> dict[str, str]:
    """Function to create the Slack message payload for a relisted Ticket."""
    ticket_link = f'<{STT_NOTIFICATIONS_CHANNEL_TICKET_URL}/{ticket.id}/change/|View Ticket>'

    return {
        'text': f'Ticket for {ticket.ticket_holder} is requested to be relisted!',
        'blocks': [
            {
                'type': 'header',
                'text': {
                    'type': 'plain_text',
                    'text': f"Ticket Relisting Alert {STT_NOTIFICATIONS_EMOJI['TICKET_RELISTING_REQUEST']}",
                },
            },
            {
                'type': 'section',
                'fields': [
                    {
                        'type': 'mrkdwn',
                        'text': f'*TICKET HOLDER:*\n{ticket.ticket_holder}',  # noqa: E231
                    },
                    {
                        'type': 'mrkdwn',
                        'text': f'*EVENT:*\n{ticket.event.name}',  # noqa: E231
                    },
                    {
                        'type': 'mrkdwn',
                        'text': f'*SECTION:*\n{ticket.section}',  # noqa: E231
                    },
                    {
                        'type': 'mrkdwn',
                        'text': f'*ROW:*\n{ticket.row}',  # noqa: E231
                    },
                    {
                        'type': 'mrkdwn',
                        'text': f'*SEAT:*\n{ticket.seat}',  # noqa: E231
                    },
                ],
            },
            {'type': 'divider'},
            {
                'type': 'section',
                'text': {
                    'type': 'mrkdwn',
                    'text': 'The ticket is requested to be relisted. '
                    'Please review the details and take necessary actions. \n\n'
                    f'{ticket_link}',
                },
            },
        ],
    }
