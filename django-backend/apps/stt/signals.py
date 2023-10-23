from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from apps.stt.models import TicketHolderTeam
from apps.stt.tasks import send_ticket_holder_team_confirmed


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
