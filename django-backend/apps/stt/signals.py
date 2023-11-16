from loguru import logger

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from apps.stt.models import Ticket, TicketHolderTeam
from apps.stt.services.ticket_handler import TicketHandler
from apps.stt.tasks import send_slack_notification, send_ticket_holder_team_confirmed
from apps.stt.utils import create_ticket_holder_team_slack_message
from config.components.celery import CELERY_GENERAL_COUNTDOWN
from config.components.global_settings import DEBUG
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
            args=(instance.ticket_holder.user.email, instance.team.name),
            countdown=CELERY_GENERAL_COUNTDOWN,
        )


@receiver(post_save, sender=Ticket)
def ticket_post_save(sender, instance, **kwargs):
    """
    Send a Slack notification when a ticket is created or cancelled and create Purchase record
    when ticket is sold.
    """
    handler = TicketHandler(instance, created=kwargs.get('created', False))
    handler.handle()


@receiver(post_save, sender=TicketHolderTeam)
def ticket_holder_team_post_save(sender, instance, **kwargs):
    if not kwargs.get('created', False):
        return

    if DEBUG:
        logger.info(
            'DEBUG MODE: Slack notification has not been sent due to DEBUG mode.'
        )
        return

    message = create_ticket_holder_team_slack_message(instance)
    send_slack_notification.apply_async(
        args=(message, STT_NOTIFICATIONS_CHANNEL_ID), countdown=CELERY_GENERAL_COUNTDOWN
    )
