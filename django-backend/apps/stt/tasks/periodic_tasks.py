from datetime import timedelta

from celery import shared_task
from django_celery_results.models import TaskResult
from loguru import logger

from django.core.management import call_command
from django.utils.timezone import now

from apps.stt.services.github_issues_reporter import GitHubIssuesReporter
from apps.stt.tasks.send_slack_notifications import send_slack_notification
from config.components.business_related import GITHUB_ACCESS_TOKEN
from config.components.celery import (
    CELERY_GENERAL_COUNTDOWN,
    CELERY_TASK_RESULT_MAX_AGE,
)
from config.components.slack_integration import (
    STT_WEEKLY_ISSUES_REPO_NAMES,
    STT_WEEKLY_ISSUES_REPORT_CHANNEL_ID,
)


@shared_task
def custom_backend_result_cleanup(max_age: int = None) -> None:
    """Custom backend result cleanup task."""
    if max_age is not None:
        max_age = timedelta(days=max_age)
    else:
        max_age = CELERY_TASK_RESULT_MAX_AGE

    expiration_time = now() - max_age
    TaskResult.objects.filter(date_done__lt=expiration_time).delete()


@shared_task
def fetch_and_send_issues_report():
    """
    Fetches closed issues from GitHub and sends a report in multiple Slack messages if needed.
    Important: executes every Sunday.
    """
    reporter = GitHubIssuesReporter(GITHUB_ACCESS_TOKEN)
    issues_by_user = reporter.generate_report(STT_WEEKLY_ISSUES_REPO_NAMES)

    slack_message = reporter.format_slack_message(issues_by_user)

    send_slack_notification.apply_async(
        args=(slack_message, STT_WEEKLY_ISSUES_REPORT_CHANNEL_ID),
        countdown=CELERY_GENERAL_COUNTDOWN,
    )


@shared_task
def clean_duplicate_history(minutes=None, excluded_fields=None, use_base_manager=False):
    """Removes duplicate historical records."""
    command_options = {'auto': True}
    if minutes:
        command_options['minutes'] = minutes
    if excluded_fields:
        command_options['excluded_fields'] = excluded_fields
    if use_base_manager:
        command_options['base_manager'] = True

    logger.info('Cleaning duplicate history...')
    call_command('clean_duplicate_history', **command_options)
    logger.info('Cleaning duplicate history finished.')


@shared_task
def clean_old_history(days=30):
    """Removes historical records that have existed for a certain amount of time."""
    logger.info('Cleaning old history...')
    call_command('clean_old_history', auto=True, days=days)
    logger.info('Cleaning old history finished.')
