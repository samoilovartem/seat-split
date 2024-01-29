from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.stt.models import Ticket, TicketHolderTeam
from apps.stt.services.ticket_holder_team_handler import (
    TicketHolderTeamPostSaveHandler,
)
from apps.stt.services.ticket_post_save_handler import TicketPostSaveHandler
from config.components.redis import redis_celery_connection


@receiver(post_save, sender=TicketHolderTeam)
def ticket_holder_team_post_save(sender, instance, created, **kwargs):
    """
    Send a Slack notification when a ticket holder team is created.
    Send an email when a ticket holder team is confirmed.
    """
    handler = TicketHolderTeamPostSaveHandler(instance, created)
    handler.handle()


@receiver(post_save, sender=Ticket)
def ticket_post_save(sender, instance, created, **kwargs):
    """
    Send a Slack notification when a ticket is created or requested for delisting.
    Create Purchase record and send an email when ticket is sold.
    """
    handler = TicketPostSaveHandler(instance, created, redis_celery_connection)
    handler.handle()
