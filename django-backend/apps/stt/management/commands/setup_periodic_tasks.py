from django_celery_beat.models import (
    CrontabSchedule,
    IntervalSchedule,
    PeriodicTask,
)

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Sets up periodic tasks for the project.'

    def handle(self, *args, **options):
        # Every day
        interval_schedule_daily, _ = IntervalSchedule.objects.get_or_create(
            every=1,
            period=IntervalSchedule.DAYS,
        )

        # Every day at 03:00 AM (Clean Old History Daily, Clean Duplicate History Daily)
        (
            crontab_schedule_daily_for_history_cleanup,
            _,
        ) = CrontabSchedule.objects.get_or_create(
            minute='0',
            hour='3',
            day_of_week='*',
            day_of_month='*',
            month_of_year='*',
            timezone='UTC',
        )

        # Every day at 04:00 AM (Backend Results Cleanup)
        crontab_schedule_daily, _ = CrontabSchedule.objects.get_or_create(
            minute='0',
            hour='4',
            day_of_week='*',
            day_of_month='*',
            month_of_year='*',
            timezone='UTC',
        )

        # Every Sunday at 01:00 PM (Weekly reports)
        crontab_schedule_weekly, _ = CrontabSchedule.objects.get_or_create(
            minute='0',
            hour='13',
            day_of_week='0',
            day_of_month='*',
            month_of_year='*',
            timezone='UTC',
        )

        # Create or update the periodic task for cleaning duplicate history
        PeriodicTask.objects.update_or_create(
            name='Clean Duplicate History Daily',
            defaults={
                'crontab': crontab_schedule_daily_for_history_cleanup,
                'task': 'apps.stt.tasks.clean_duplicate_history',
            },
        )

        # Create or update the periodic task for cleaning old history
        PeriodicTask.objects.update_or_create(
            name='Clean Old History Daily',
            defaults={
                'crontab': crontab_schedule_daily_for_history_cleanup,
                'task': 'apps.stt.tasks.clean_old_history',
            },
        )

        # Create or update the periodic task for sending weekly reports to Slack
        PeriodicTask.objects.update_or_create(
            name='Weekly Reports',
            defaults={
                'crontab': crontab_schedule_weekly,
                'task': 'apps.stt.tasks.fetch_and_send_issues_report',
            },
        )

        # Create or update the periodic task for backend results cleanup
        PeriodicTask.objects.update_or_create(
            name='Backend Results Cleanup',
            defaults={
                'crontab': crontab_schedule_daily,
                'task': 'apps.stt.tasks.custom_backend_result_cleanup',
            },
        )

        self.stdout.write(self.style.SUCCESS('Successfully set up periodic tasks.'))
