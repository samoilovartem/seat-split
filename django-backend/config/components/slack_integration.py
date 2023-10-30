import os

from slack_sdk import WebClient

from config.components.global_settings import DJANGO_HOST_URL

STT_NOTIFICATIONS_EMOJI = {
    'TICKET_CREATED': os.environ.get('TICKET_CREATED', ':season_ticket:'),
    'TICKET_HOLDER_TEAM_CREATED': os.environ.get(
        'TICKET_HOLDER_TEAM_CREATED', ':sparkle:'
    ),
    'TICKET_DELISTING_REQUEST': os.environ.get('TICKET_DELISTING_REQUEST', ':x:'),
}

STT_NOTIFICATIONS_CHANNEL_WEBHOOK_URL = os.environ.get(
    'STT_NOTIFICATIONS_CHANNEL_WEBHOOK_URL'
)
STT_NOTIFICATIONS_CHANNEL_TICKET_URL = f'{DJANGO_HOST_URL}/admin/stt/ticket'
STT_NOTIFICATIONS_CHANNEL_TICKET_HOLDER_URL = (
    f'{DJANGO_HOST_URL}/admin/stt/ticketholder'
)
STT_NOTIFICATIONS_BOT_API_TOKEN = os.environ.get('STT_NOTIFICATIONS_BOT_API_TOKEN')
STT_NOTIFICATIONS_CHANNEL_ID = os.environ.get('STT_NOTIFICATIONS_CHANNEL_ID')

slack_client = WebClient(token=STT_NOTIFICATIONS_BOT_API_TOKEN)
