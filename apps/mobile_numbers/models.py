import uuid

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
    requested_by = models.ForeignKey(User, on_delete=models.PROTECT)
    service_main_response = models.JSONField(blank=True)
    account_created = models.BooleanField(default=False)

    def __str__(self):
        return self.phone

    class Meta:
        verbose_name = 'Mobile Number Transaction'
        verbose_name_plural = 'Mobile Number Transactions'
        ordering = ['-created_at']
        unique_together = ['phone', 'order_id']
        permissions = (
            ('import_accounts', 'Can import'),
            ('export_accounts', 'Can export'),
        )
