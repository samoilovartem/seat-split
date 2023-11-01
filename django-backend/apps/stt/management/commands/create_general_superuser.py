from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

from apps.users.models import User
from config.settings import GENERAL_SUPERUSER_EMAIL, GENERAL_SUPERUSER_PASSWORD


class Command(BaseCommand):
    help = 'Create a general superuser if it does not exist'

    def handle(self, *args, **options):
        if not User.objects.filter(is_superuser=True).exists():
            try:
                User.objects.create_superuser(
                    GENERAL_SUPERUSER_EMAIL,
                    GENERAL_SUPERUSER_PASSWORD,
                )
                self.stdout.write(
                    self.style.SUCCESS('Successfully created a new superuser')
                )
            except IntegrityError:
                self.stdout.write(
                    self.style.WARNING('A superuser with that username already exists.')
                )
        else:
            self.stdout.write(self.style.SUCCESS('A superuser already exists.'))
