import uuid

from django.contrib.auth import get_user_model
from django.db import models
from phone_field import PhoneField

from apps.accounts.models import Accounts

User = get_user_model()


class TimeStampedMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class MobileNumberStorage(UUIDMixin, TimeStampedMixin):
    phone = PhoneField(blank=True, unique=True, E164_only=True)
    email = models.ForeignKey(Accounts, on_delete=models.PROTECT)

    class StatusChoice(models.TextChoices):
        ASSIGNED = 'assigned'
        NOT_ASSIGNED = 'not assigned'

    status = models.TextField(choices=StatusChoice.choices, blank=False)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    last_time_used = models.DateTimeField(blank=True)
    session_data = models.JSONField(blank=True)

    def __str__(self):
        return f'{self.phone}'

    class Meta:
        verbose_name = 'Mobile Number Storage'
        verbose_name_plural = 'Mobile Numbers Storage'
        ordering = ['-created_at']
        permissions = (
            ('import_accounts', 'Can import'),
            ('export_accounts', 'Can export'),
        )
