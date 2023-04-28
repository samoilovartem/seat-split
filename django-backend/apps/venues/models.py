import uuid

from django.contrib.gis.db import models


class TimeStampedMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Venues(UUIDMixin, TimeStampedMixin, models.Model):
    name = models.CharField(max_length=255, blank=True)
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    country_code = models.CharField(max_length=255, blank=True)
    postal_code = models.CharField(max_length=255, blank=True)
    state_code = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=255, blank=True)
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = "content\".\"venues"
        verbose_name = 'Venue'
        verbose_name_plural = 'Venues'
        unique_together = ['name', 'address']
        ordering = ['name']
        permissions = (
            ('import_venues', 'Can import'),
            ('export_venues', 'Can export'),
        )
