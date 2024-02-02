import json
from uuid import UUID

from celery import shared_task
from loguru import logger
from slack_sdk.errors import SlackApiError

from apps.stt.utils import create_ticket_created_slack_message
from config.components.redis import redis_celery_connection
from config.components.slack_integration import (
    STT_NOTIFICATIONS_CHANNEL_ID,
    slack_client,
)


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
            slack_client.chat_postMessage(channel=STT_NOTIFICATIONS_CHANNEL_ID, **message_payload)
        except SlackApiError as e:
            logger.error('There is an error sending a notification to slack. Error: {}', e)
