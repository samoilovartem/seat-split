from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.stt.models import TicketHolderTeam
from apps.stt.tasks import send_ticket_holder_team_confirmed


@receiver(post_save, sender=TicketHolderTeam)
def send_confirmation_email(sender, instance, **kwargs):
    if instance.is_confirmed:
        send_ticket_holder_team_confirmed(
            user_email=instance.ticket_holder.user.email, team_name=instance.team.name
        )
        # send_ticket_holder_team_confirmed.delay(
        #     user_email=instance.ticket_holder.user.email,
        #     team_name=instance.team.name
        # )
