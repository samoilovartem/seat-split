import uuid

from simple_history.models import HistoricalRecords

from django.contrib.auth import get_user_model
from django.db import models

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


class MobileNumberTransaction(UUIDMixin, TimeStampedMixin):
    phone = models.CharField(max_length=20, blank=True)
    email = models.ForeignKey(Accounts, on_delete=models.PROTECT, blank=True)
    service_name = models.CharField(max_length=50, blank=True)
    order_id = models.CharField(max_length=100, blank=True)
    service_id = models.CharField(max_length=100, blank=True)

    class TypeChoice(models.TextChoices):
        TEMPORARY = 'temporary'
        RENTAL = 'rental'
        NOT_APPLICABLE = 'not applicable'

    type = models.TextField(
        choices=TypeChoice.choices, default=TypeChoice.NOT_APPLICABLE
    )
    requested_by = models.ForeignKey(User, on_delete=models.PROTECT)
    price = models.IntegerField(blank=True, default=0)
    expiration_date = models.DateTimeField(null=True, blank=True)

    class StatusChoice(models.TextChoices):
        EXPIRING_SOON = 'expiring soon'
        EXPIRED = 'expired'
        OFFLINE = 'offline'
        ONLINE = 'online'
        NOT_APPLICABLE = 'not applicable'

    status = models.TextField(
        choices=StatusChoice.choices, default=StatusChoice.NOT_APPLICABLE
    )
    awake_until = models.DateTimeField(null=True, blank=True)
    service_main_response = models.JSONField(blank=True)
    account_created = models.BooleanField(default=False)
    history = HistoricalRecords()

    def __str__(self):
        return self.phone

    class Meta:
        db_table = "content\".\"mobile_number_transactions"
        verbose_name = 'Mobile Number Transaction'
        verbose_name_plural = 'Mobile Number Transactions'
        ordering = ['-created_at']
        unique_together = ['phone', 'order_id']
        permissions = (
            ('import_accounts', 'Can import'),
            ('export_accounts', 'Can export'),
        )
