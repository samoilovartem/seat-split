import json

from loguru import logger

from django.utils import timezone

from apps.stt.models import Purchase, Ticket
from apps.stt.tasks import send_aggregated_slack_notification, send_slack_notification
from apps.stt.utils import create_ticket_status_cancelled_slack_message
from config.components.business_related import DELIVERY_STATUSES, MARKETPLACES
from config.components.celery import (
    CELERY_AGGREGATED_SLACK_NOTIFICATION_COUNTDOWN,
    CELERY_GENERAL_COOLDOWN,
)
from config.components.global_settings import DEBUG
from config.components.redis import REDIS_NEW_TICKETS_KEY_EXPIRE, redis_connection
from config.components.slack_integration import STT_NOTIFICATIONS_CHANNEL_ID


class TicketHandler:
    def __init__(self, instance: Ticket, created: bool = False):
        """
        Initialize the ticket handler with a ticket instance and a created flag.

        :param instance: The ticket instance to be handled.
        :param created: A flag indicating if the ticket was newly created.
        """
        self.instance = instance
        self.created = created

    @staticmethod
    def _send_debug_logger_slack_message() -> None:
        logger.info(
            'DEBUG MODE: Slack notification has not been sent due to DEBUG mode.'
        )

    def handle(self) -> None:
        """Main handler method to process ticket creation or status changes."""
        if self.created:
            self._handle_ticket_creation()
        self._handle_ticket_status_change()

    def _handle_ticket_creation(self) -> None:
        """Handles the logic for ticket creation."""
        if DEBUG:
            self._send_debug_logger_slack_message()
            return
        self._cache_new_ticket_data()
        send_aggregated_slack_notification.apply_async(
            args=(self.instance.event.id, self.instance.ticket_holder.id),
            countdown=CELERY_AGGREGATED_SLACK_NOTIFICATION_COUNTDOWN,
        )

    def _cache_new_ticket_data(self) -> None:
        """Cache ticket data in Redis for newly created tickets."""
        redis_key = (
            f'new_tickets_{self.instance.event.id}_{self.instance.ticket_holder.id}'
        )
        ticket_data = json.dumps(
            {
                'id': str(self.instance.id),
                'ticket_holder': str(self.instance.ticket_holder),
                'event': str(self.instance.event),
                'seat': self.instance.seat,
                'row': self.instance.row,
                'section': self.instance.section,
            }
        )
        redis_connection.rpush(redis_key, ticket_data)
        redis_connection.expire(redis_key, REDIS_NEW_TICKETS_KEY_EXPIRE)

    def _handle_ticket_status_change(self) -> None:
        """Handles the logic for ticket status changes."""
        if len(self.instance.history.all()) < 2:
            return
        previous_status = self.instance.history.all()[1].listing_status
        if self._was_sold(previous_status):
            self._handle_ticket_sold()
        elif self._was_cancelled(previous_status):
            self._handle_ticket_cancelled()

    def _was_sold(self, previous_status: str) -> bool:
        """Check if the ticket was sold."""
        return self.instance.listing_status == 'Sold' and previous_status != 'Sold'

    def _handle_ticket_sold(self) -> None:
        """Logic for when a ticket is sold."""
        if not Purchase.objects.filter(ticket=self.instance).exists():
            Purchase.objects.create(
                ticket=self.instance,
                customer=MARKETPLACES[0][0],
                purchase_price=self.instance.price,
                delivery_status=DELIVERY_STATUSES[0][0],
                purchased_at=timezone.now(),
            )

    def _was_cancelled(self, previous_status: str) -> bool:
        """Check if the ticket was cancelled."""
        return (
            self.instance.listing_status == 'Cancelled'
            and previous_status != 'Cancelled'
        )

    def _handle_ticket_cancelled(self) -> None:
        """Logic for when a ticket is cancelled."""
        if DEBUG:
            self._send_debug_logger_slack_message()
            return
        message = create_ticket_status_cancelled_slack_message(self.instance)
        send_slack_notification.apply_async(
            args=(message, STT_NOTIFICATIONS_CHANNEL_ID),
            countdown=CELERY_GENERAL_COOLDOWN,
        )
