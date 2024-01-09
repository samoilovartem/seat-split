from loguru import logger

from apps.stt.models import Ticket
from apps.stt.services.ticket_services import (
    TicketCacheService,
    TicketNotifier,
    TicketStatusChecker,
)


class TicketPostSaveHandler:
    def __init__(
        self, instance: Ticket, created: bool = False, redis_celery_connection=None
    ):
        self.instance = instance
        self.created = created
        self.notifier = TicketNotifier(instance)
        self.status_checker = TicketStatusChecker(instance)
        self.cache_service = TicketCacheService(instance, redis_celery_connection)

    @staticmethod
    def _send_debug_logger_slack_message() -> None:
        logger.info(
            'DEBUG MODE: Slack notification has not been sent due to DEBUG mode.'
        )

    def handle(self) -> None:
        if self.created:
            self._handle_ticket_creation()
        self._handle_ticket_status_change()

    def _handle_ticket_creation(self) -> None:
        self.cache_service.cache_new_ticket_data()
        self.notifier.send_aggregated_slack_notification()

    def _handle_ticket_status_change(self) -> None:
        history = self.instance.history.all()
        if len(history) < 2:
            return
        previous_status = history[1].listing_status

        if self.status_checker.was_sold(previous_status):
            self.status_checker.create_purchase_record_if_needed()
            self.notifier.send_ticket_sold_email()
            self.notifier.send_ticket_sold_notification()
        elif self.status_checker.was_requested_for_delisting(previous_status):
            self.notifier.send_ticket_requested_for_delisting_notification()
        elif self.status_checker.was_listed(previous_status):
            self.notifier.send_ticket_listed_notification()
        elif self.status_checker.was_delisted(previous_status):
            self.notifier.send_ticket_delisted_notification()
