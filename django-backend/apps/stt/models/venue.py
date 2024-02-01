from uuid import uuid4

from django.db import models
from django.db.models import UniqueConstraint


class Venue(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    skybox_venue_id = models.IntegerField()
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    timezone = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content"."venue'
        verbose_name = 'Venue'
        verbose_name_plural = 'Venues'
        permissions = (
            ('import_events', 'Can import'),
            ('export_events', 'Can export'),
        )
        constraints = (
            UniqueConstraint(
                fields=('skybox_venue_id', 'name'),
                name='skybox_venue_id_name_idx',
            ),
        )

    def __str__(self):
        return f'{self.name}'
