from loguru import logger

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from apps.stt.models import Ticket, TicketHolderTeam
from apps.stt.tasks import send_ticket_holder_team_confirmed, send_to_slack
from apps.stt.utils import (
    create_ticket_created_slack_message,
    create_ticket_holder_team_slack_message,
    create_ticket_status_cancelled_slack_message,
)
from config.components.global_settings import DEBUG


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
        send_ticket_holder_team_confirmed(
            user_email=instance.ticket_holder.user.email, team_name=instance.team.name
        )
        # send_ticket_holder_team_confirmed.delay(
        #     user_email=instance.ticket_holder.user.email,
        #     team_name=instance.team.name
        # )


@receiver(post_save, sender=Ticket)
def ticket_post_save(sender, instance, **kwargs):
    """Send a Slack notification when a ticket is created or cancelled."""
    if kwargs.get('created', False):
        message = create_ticket_created_slack_message(instance)
        if DEBUG:
            logger.info(
                'DEBUG MODE: Slack notification has not been sent due to DEBUG mode.'
            )
            return
        send_to_slack(message)
        # send_to_slack.delay(message)
        return

    if len(instance.history.all()) < 2:
        return

    previous_status = instance.history.all()[1].listing_status
    if previous_status == 'Cancelled' or instance.listing_status != 'Cancelled':
        return

    message = create_ticket_status_cancelled_slack_message(instance)

    if DEBUG:
        logger.info(
            'DEBUG MODE: Slack notification has not been sent due to DEBUG mode.'
        )
        return

    send_to_slack(message)
    # send_to_slack.delay(message)


@receiver(post_save, sender=TicketHolderTeam)
def ticket_holder_team_post_save(sender, instance, **kwargs):
    if not kwargs.get('created', False):
        return

    message = create_ticket_holder_team_slack_message(instance)

    if DEBUG:
        logger.info(
            'DEBUG MODE: Slack notification has not been sent due to DEBUG mode.'
        )
        return

    send_to_slack(message)
    # send_to_slack.delay(message)
