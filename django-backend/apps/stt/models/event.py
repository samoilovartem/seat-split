from uuid import uuid4

from simple_history.models import HistoricalRecords

from django.db import models
from django.db.models import UniqueConstraint


class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    skybox_event_id = models.CharField(max_length=255, blank=True, default='')
    name = models.CharField(max_length=255)
    additional_info = models.CharField(max_length=255, default='')
    date_time = models.DateTimeField()
    season = models.ForeignKey('Season', on_delete=models.SET_NULL, null=True, related_name='events')
    venue = models.ForeignKey('Venue', on_delete=models.SET_NULL, null=True, related_name='events')
    stubhub_event_url = models.TextField(blank=True, default='')
    league = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()

    class Meta:
        db_table = 'content"."event'
        verbose_name = 'Event'
        verbose_name_plural = 'Events'
        constraints = (
            UniqueConstraint(
                fields=('name', 'date_time', 'season'),
                name='name_date_time_season_idx',
            ),
        )
        permissions = (
            ('import_events', 'Can import'),
            ('export_events', 'Can export'),
        )

    def __str__(self):
        return f'{self.name} | {self.date_time.strftime("%m/%d/%Y")}'

    def get_formatted_name(self):
        if self.additional_info:
            return f'{self.name} ({self.additional_info})'
        return self.name
