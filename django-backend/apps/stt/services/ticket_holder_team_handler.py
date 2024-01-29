from loguru import logger
from notifications.signals import notify

from apps.stt.models import TicketHolderTeam
from apps.stt.tasks import send_slack_notification, send_ticket_holder_team_confirmed
from apps.stt.utils import create_ticket_holder_team_slack_message
from config.components.celery import CELERY_GENERAL_COUNTDOWN
from config.components.global_settings import DEBUG
from config.components.slack_integration import STT_NOTIFICATIONS_CHANNEL_ID


class TicketHolderTeamPostSaveHandler:
    def __init__(self, instance: TicketHolderTeam, created: bool):
        self.instance = instance
        self.created = created

    def handle(self):
        if self.created:
            self._handle_creation()
        else:
            self._handle_update()

    def _handle_creation(self):
        if DEBUG:
            logger.info('DEBUG MODE: Slack notification has not been sent due to DEBUG mode.')
            return

        message = create_ticket_holder_team_slack_message(self.instance)
        send_slack_notification.apply_async(
            args=(message, STT_NOTIFICATIONS_CHANNEL_ID),
            countdown=CELERY_GENERAL_COUNTDOWN,
        )

    def _handle_update(self):
        historical_records = self.instance.history.all()
        if historical_records.count() <= 1:
            return

        previous_record = historical_records[1]
        if previous_record.is_confirmed or not self.instance.is_confirmed:
            return

        send_ticket_holder_team_confirmed.apply_async(
            args=(self.instance.ticket_holder.user.email, self.instance.team.name),
            countdown=CELERY_GENERAL_COUNTDOWN,
        )
        description = (
            f'Your team with the following details has been confirmed: \n\n'
            f'Team: {self.instance.team.name} \n'
            f'Section: {self.instance.section}, Row: {self.instance.row}, Seat: {self.instance.seat} \n\n'
            f'You can start selling tickets right away.'
        )
        notify.send(
            sender=self.instance,
            recipient=self.instance.ticket_holder.user,
            verb='Team Data Confirmed',
            description=description,
        )
