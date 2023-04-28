import uuid

from simple_history.models import HistoricalRecords

from django.contrib.auth import get_user_model
from django.db import models

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


class EmailDomains(UUIDMixin, TimeStampedMixin):
    domain_name = models.CharField(unique=True, max_length=50, blank=True)

    class StatusChoice(models.TextChoices):
        ACTIVE = 'active'
        PENDING = 'pending'
        NOT_ACTIVE = 'not active'
        NOT_APPLICABLE = 'not applicable'

    status = models.TextField(
        choices=StatusChoice.choices, default=StatusChoice.NOT_APPLICABLE
    )
    expiration_date = models.DateField(null=True, blank=True)
    auto_renew = models.BooleanField(default=False)
    is_private = models.BooleanField(default=False)
    is_locked = models.BooleanField(default=False)
    is_default_route = models.BooleanField(default=False)
    is_second_domain = models.BooleanField(default=False)
    type = models.CharField(max_length=30, blank=True)
    forwarding_account = models.EmailField(blank=True)

    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    history = HistoricalRecords()

    def __str__(self):
        return self.domain_name

    class Meta:
        db_table = "content\".\"email_domains"
        verbose_name = 'Email Domain'
        verbose_name_plural = 'Email Domains'
        ordering = ['-created_at']
        permissions = (
            ('import_email_domains', 'Can import'),
            ('export_email_domains', 'Can export'),
        )
