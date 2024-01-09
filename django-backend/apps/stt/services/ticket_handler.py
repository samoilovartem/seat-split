import json

from loguru import logger
from notifications.signals import notify

from django.utils import timezone

from apps.stt.models import Purchase, Ticket
from apps.stt.tasks import (
    send_aggregated_slack_notification,
    send_slack_notification,
    send_ticket_sold_email,
)
from apps.stt.utils import (
    calculate_price_with_expenses,
    create_ticket_status_requested_for_delisting_slack_message,
)
from config.components.business_related import DELIVERY_STATUSES, MARKETPLACES
from config.components.celery import (
    CELERY_AGGREGATED_SLACK_NOTIFICATION_COUNTDOWN,
    CELERY_GENERAL_COUNTDOWN,
)
from config.components.global_settings import DEBUG
from config.components.redis import (
    REDIS_NEW_TICKETS_KEY_EXPIRE,
    redis_celery_connection,
)
from config.components.slack_integration import STT_NOTIFICATIONS_CHANNEL_ID


class TicketPostSaveHandler:
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
        redis_celery_connection.rpush(redis_key, ticket_data)
        redis_celery_connection.expire(redis_key, REDIS_NEW_TICKETS_KEY_EXPIRE)

    def _handle_ticket_status_change(self) -> None:
        """Handles the logic for ticket status changes."""
        if len(self.instance.history.all()) < 2:
            return
        previous_status = self.instance.history.all()[1].listing_status
        if self._was_sold(previous_status):
            self._handle_ticket_sold()
        elif self._was_requested_for_delisting(previous_status):
            self._handle_ticket_requested_for_delisting()
        elif self._was_delisted(previous_status):
            self._handle_ticket_delisted()
        elif self._was_listed(previous_status):
            self._handle_ticket_listed()

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

        send_ticket_sold_email.apply_async(
            args=(
                self.instance.ticket_holder.user.email,
                self.instance.event.name,
                self.instance.event.date_time,
                self.instance.section,
                self.instance.row,
                self.instance.seat,
                self.instance.price,
            ),
            countdown=CELERY_GENERAL_COUNTDOWN,
        )
        notify.send(
            sender=self.instance,
            recipient=self.instance.ticket_holder.user,
            verb=f'Your ticket for "{self.instance.event.name}" with seat number "{self.instance.seat}" has been sold '
            f'for ${calculate_price_with_expenses(self.instance.price)}.',
        )

    def _was_requested_for_delisting(self, previous_status: str) -> bool:
        """Check if the ticket was requested for delisting."""
        return (
            self.instance.listing_status == 'Requested for delisting'
            and previous_status != 'Requested for delisting'
        )

    def _handle_ticket_requested_for_delisting(self) -> None:
        """Logic for when a ticket is requested for delisting."""
        if DEBUG:
            self._send_debug_logger_slack_message()
            return
        message = create_ticket_status_requested_for_delisting_slack_message(
            self.instance
        )
        send_slack_notification.apply_async(
            args=(message, STT_NOTIFICATIONS_CHANNEL_ID),
            countdown=CELERY_GENERAL_COUNTDOWN,
        )

    def _was_listed(self, previous_status: str) -> bool:
        """Check if the ticket was listed."""
        return self.instance.listing_status == 'Listed' and previous_status != 'Listed'

    def _handle_ticket_listed(self) -> None:
        """Logic for when a ticket is listed."""
        notify.send(
            sender=self.instance,
            recipient=self.instance.ticket_holder.user,
            verb=f'Your ticket for "{self.instance.event.name}" with seat number "{self.instance.seat}" has been '
            f'listed for ${calculate_price_with_expenses(self.instance.price)}.',
        )

    def _was_delisted(self, previous_status: str) -> bool:
        """Check if the ticket was delisted."""
        return (
            self.instance.listing_status == 'Delisted' and previous_status != 'Delisted'
        )

    def _handle_ticket_delisted(self) -> None:
        """Logic for when a ticket is delisted."""
        notify.send(
            sender=self.instance,
            recipient=self.instance.ticket_holder.user,
            verb=f'Your ticket for "{self.instance.event.name}" with seat number "{self.instance.seat}" has been '
            f'delisted.',
        )
