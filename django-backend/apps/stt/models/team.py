from uuid import uuid4

from django.db import models

from apps.stt.models.venue import Venue


class Team(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    skybox_id = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=255)
    name_short = models.CharField(max_length=255)
    abbreviation = models.CharField(max_length=255)
    league = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    home_venue = models.ForeignKey(Venue, on_delete=models.PROTECT, null=True, related_name='home_teams')
    logo = models.FileField(upload_to='logos/', null=True, blank=True)
    ticketmaster_id = models.IntegerField(null=True, blank=True)
    timezone = models.CharField(max_length=255)
    credentials_website = models.CharField(max_length=255)
    automatiq_credentials_website_id = models.IntegerField(
        null=True,
        blank=True,
    )
    ticketmaster_name = models.CharField(max_length=255)
    vendor_id = models.CharField(max_length=255, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content"."team'
        verbose_name = 'Team'
        verbose_name_plural = 'Teams'
        permissions = (
            ('import_events', 'Can import'),
            ('export_events', 'Can export'),
        )

    def __str__(self):
        return f'{self.name}'
