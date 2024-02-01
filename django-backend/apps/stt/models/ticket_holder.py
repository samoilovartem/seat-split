from hashlib import md5
from uuid import uuid4

from pytz import common_timezones
from simple_history.models import HistoricalRecords

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


def ticket_holder_avatar_path(instance, filename):
    """Generate unique path for ticket holder avatar."""
    ext = filename.split('.')[-1]

    unique_filename = f'{uuid4().hex}.{ext}'

    user = instance.user
    hash_string = md5(f'{user.email}{user.id}'.encode()).hexdigest()

    return f'avatars/{hash_string}/{unique_filename}'


class TicketHolder(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    user = models.OneToOneField(User, related_name='ticket_holder_user', on_delete=models.CASCADE)
    phone = models.CharField(
        verbose_name='Phone number',
        blank=True,
        max_length=255,
    )
    address = models.CharField(max_length=255, blank=True)
    is_card_interest = models.BooleanField(default=False)
    is_season_ticket_interest = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    avatar = models.ImageField(upload_to=ticket_holder_avatar_path, null=True, blank=True)
    timezone = models.CharField(max_length=255, choices=[(tz, tz) for tz in common_timezones], default='UTC')
    history = HistoricalRecords()

    class Meta:
        db_table = 'content"."ticket_holder'
        verbose_name = 'Ticket Holder'
        verbose_name_plural = 'Ticket Holders'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
