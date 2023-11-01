import json

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone

from apps.stt.models import Purchase, Ticket, TicketHolderTeam
from apps.stt.tasks import (
    send_aggregated_slack_notification,
    send_slack_notification,
    send_ticket_holder_team_confirmed,
)
from apps.stt.utils import (
    create_ticket_holder_team_slack_message,
    create_ticket_status_cancelled_slack_message,
    send_debug_logger_slack_message,
)
from config.components.business_related import DELIVERY_STATUSES, MARKETPLACES
from config.components.global_settings import DEBUG
from config.components.redis import redis_connection
from config.components.slack_integration import STT_NOTIFICATIONS_CHANNEL_ID


@receiver(pre_save, sender=TicketHolderTeam)
def store_previous_is_confirmed(sender, instance, **kwargs):
    try:
        obj = sender.objects.get(pk=instance.pk)
        instance._previous_is_confirmed = obj.is_confirmed
    except sender.DoesNotExist:
        instance._previous_is_confirmed = None


@receiver(post_save, sender=TicketHolderTeam)
def send_confirmation_email(sender, instance, **kwargs):
    previous_is_confirmed = getattr(instance, '_previous_is_confirmed', None)
    if previous_is_confirmed is False and instance.is_confirmed:
        send_ticket_holder_team_confirmed.apply_async(
            args=(instance.ticket_holder.user.email, instance.team.name), countdown=5
        )


@receiver(post_save, sender=Ticket)
def ticket_post_save(sender, instance, **kwargs):
    """
    Send a Slack notification when a ticket is created or cancelled and create Purchase record
    when ticket is sold.
    """
    if kwargs.get('created', False):
        if DEBUG:
            send_debug_logger_slack_message()
            return

        redis_key = f'new_tickets_{instance.event.id}_{instance.ticket_holder.id}'

        ticket_data = json.dumps(
            {
                'id': str(instance.id),
                'ticket_holder': instance.ticket_holder.__str__(),
                'event': instance.event.__str__(),
                'seat': instance.seat,
                'row': instance.row,
                'section': instance.section,
            }
        )

        redis_connection.rpush(redis_key, ticket_data)
        redis_connection.expire(redis_key, 300)

        send_aggregated_slack_notification.apply_async(
            args=(instance.event.id, instance.ticket_holder.id), countdown=30
        )

    if len(instance.history.all()) < 2:
        return

    previous_status = instance.history.all()[1].listing_status

    if instance.listing_status == 'Sold' and previous_status != 'Sold':
        if not Purchase.objects.filter(ticket=instance).exists():
            Purchase.objects.create(
                ticket=instance,
                customer=MARKETPLACES[0][0],
                purchase_price=instance.price,
                delivery_status=DELIVERY_STATUSES[0][0],
                purchased_at=timezone.now(),
            )

    elif previous_status != 'Cancelled' and instance.listing_status == 'Cancelled':
        if DEBUG:
            send_debug_logger_slack_message()
            return

        message = create_ticket_status_cancelled_slack_message(instance)
        send_slack_notification.apply_async(
            args=(message, STT_NOTIFICATIONS_CHANNEL_ID), countdown=5
        )


@receiver(post_save, sender=TicketHolderTeam)
def ticket_holder_team_post_save(sender, instance, **kwargs):
    if not kwargs.get('created', False):
        return

    if DEBUG:
        send_debug_logger_slack_message()
        return

    message = create_ticket_holder_team_slack_message(instance)
    send_slack_notification.apply_async(
        args=(message, STT_NOTIFICATIONS_CHANNEL_ID), countdown=5
    )
