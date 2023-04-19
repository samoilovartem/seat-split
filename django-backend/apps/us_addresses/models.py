import uuid

from django.contrib.gis.db import models
from django.contrib.gis.geos import Point


class TimeStampedMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class USAddresses(UUIDMixin, TimeStampedMixin, models.Model):
    city = models.CharField(max_length=255, blank=True)
    line = models.CharField(max_length=255, blank=True)
    street_name = models.CharField(max_length=255, blank=True)
    street_number = models.CharField(max_length=255, blank=True)
    street_suffix = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=255, blank=True)
    postal_code = models.CharField(max_length=255, blank=True)
    state_code = models.CharField(max_length=255, blank=True)
    state = models.CharField(max_length=255, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    location = models.PointField(geography=True, blank=True, null=True)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return self.line

    def save(self, *args, **kwargs):
        if self.latitude and self.longitude:
            self.location = Point(x=float(self.longitude), y=float(self.latitude))
        super().save(*args, **kwargs)

    class Meta:
        db_table = "content\".\"us_addresses"
        verbose_name = 'US Address'
        verbose_name_plural = 'US Addresses'
        ordering = ['state']
        unique_together = ['line', 'city']
        permissions = (
            ('import_accounts', 'Can import'),
            ('export_accounts', 'Can export'),
        )
