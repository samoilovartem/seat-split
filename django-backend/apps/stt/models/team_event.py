from uuid import uuid4

from simple_history.models import HistoricalRecords

from django.db import models
from django.db.models import UniqueConstraint

from apps.stt.models.event import Event
from apps.stt.models.team import Team


class TeamEvent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()

    class Meta:
        db_table = 'content"."team_event'
        verbose_name = "Event's Team"
        verbose_name_plural = "Event's Teams"
        constraints = (
            UniqueConstraint(
                fields=('event', 'team'),
                name='event_team_idx',
            ),
        )

    def __str__(self):
        return f'{self.event} - {self.team} - {self.id}'
