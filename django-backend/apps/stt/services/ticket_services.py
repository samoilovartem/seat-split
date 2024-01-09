import json

from notifications.signals import notify

from django.utils import timezone

from apps.stt.models import Purchase
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
from config.components.redis import REDIS_NEW_TICKETS_KEY_EXPIRE
from config.components.slack_integration import STT_NOTIFICATIONS_CHANNEL_ID


class TicketNotifier:
    def __init__(self, ticket):
        self.ticket = ticket

    def send_ticket_sold_email(self):
        send_ticket_sold_email.apply_async(
            args=(
                self.ticket.ticket_holder.user.email,
                self.ticket.event.name,
                self.ticket.event.date_time,
                self.ticket.section,
                self.ticket.row,
                self.ticket.seat,
                self.ticket.price,
            ),
            countdown=CELERY_GENERAL_COUNTDOWN,
        )

    def send_ticket_sold_notification(self):
        notify.send(
            sender=self.ticket,
            recipient=self.ticket.ticket_holder.user,
            verb=f'Your ticket for "{self.ticket.event.name}" with seat number "{self.ticket.seat}" has been sold '
            f'for ${calculate_price_with_expenses(self.ticket.price)}.',
        )

    def send_ticket_requested_for_delisting_notification(self):
        message = create_ticket_status_requested_for_delisting_slack_message(
            self.ticket
        )
        send_slack_notification.apply_async(
            args=(message, STT_NOTIFICATIONS_CHANNEL_ID),
            countdown=CELERY_GENERAL_COUNTDOWN,
        )

    def send_ticket_listed_notification(self):
        notify.send(
            sender=self.ticket,
            recipient=self.ticket.ticket_holder.user,
            verb=f'Your ticket for "{self.ticket.event.name}" with seat number "{self.ticket.seat}" has been '
            f'listed for ${calculate_price_with_expenses(self.ticket.price)}.',
        )

    def send_ticket_delisted_notification(self):
        notify.send(
            sender=self.ticket,
            recipient=self.ticket.ticket_holder.user,
            verb=f'Your ticket for "{self.ticket.event.name}" with seat number "{self.ticket.seat}" has been '
            f'delisted.',
        )

    def send_aggregated_slack_notification(self):
        send_aggregated_slack_notification.apply_async(
            args=(self.ticket.event.id, self.ticket.ticket_holder.id),
            countdown=CELERY_AGGREGATED_SLACK_NOTIFICATION_COUNTDOWN,
        )


class TicketStatusChecker:
    def __init__(self, ticket):
        self.ticket = ticket

    def was_sold(self, previous_status):
        return self.ticket.listing_status == 'Sold' and previous_status != 'Sold'

    def was_requested_for_delisting(self, previous_status):
        return (
            self.ticket.listing_status == 'Requested for delisting'
            and previous_status != 'Requested for delisting'
        )

    def was_listed(self, previous_status):
        return self.ticket.listing_status == 'Listed' and previous_status != 'Listed'

    def was_delisted(self, previous_status):
        return (
            self.ticket.listing_status == 'Delisted' and previous_status != 'Delisted'
        )

    def create_purchase_record_if_needed(self):
        if not Purchase.objects.filter(ticket=self.ticket).exists():
            Purchase.objects.create(
                ticket=self.ticket,
                customer=MARKETPLACES[0][0],
                purchase_price=self.ticket.price,
                delivery_status=DELIVERY_STATUSES[0][0],
                purchased_at=timezone.now(),
            )


class TicketCacheService:
    def __init__(self, ticket, redis_celery_connection):
        self.ticket = ticket
        self.redis_celery_connection = redis_celery_connection

    def cache_new_ticket_data(self):
        redis_key = f'new_tickets_{self.ticket.event.id}_{self.ticket.ticket_holder.id}'
        ticket_data = json.dumps(
            {
                'id': str(self.ticket.id),
                'ticket_holder': str(self.ticket.ticket_holder),
                'event': str(self.ticket.event),
                'seat': self.ticket.seat,
                'row': self.ticket.row,
                'section': self.ticket.section,
            }
        )
        self.redis_celery_connection.rpush(redis_key, ticket_data)
        self.redis_celery_connection.expire(redis_key, REDIS_NEW_TICKETS_KEY_EXPIRE)
