from uuid import uuid4

from django.db import models
from django.db.models import UniqueConstraint
from simple_history.models import HistoricalRecords

from config.components.business_related import SUPPORTED_LEAGUES


class Season(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(
        max_length=255,
        help_text='The name or title of the season. For example, "2023", "2023-2024".',
    )
    start_year = models.IntegerField(help_text='The calendar year when the season starts')
    league = models.CharField(
        max_length=255,
        choices=((league, league) for league in SUPPORTED_LEAGUES),
        help_text='The sports league to which the season belongs',
    )
    official_start_date = models.DateField(
        blank=True, null=True, help_text='The date when the season officially starts'
    )
    official_end_date = models.DateField(
        blank=True, null=True, help_text='The date when the season officially ends'
    )

    start_selling_season_date = models.DateField(
        blank=True,
        null=True,
        help_text='The date when sales for season-related tickets begin',
    )

    start_regular_season_date = models.DateField(
        blank=True,
        null=True,
        help_text='The date when the regular season is scheduled to begin',
    )
    end_regular_season_date = models.DateField(
        blank=True,
        null=True,
        help_text='The date when the regular season is scheduled to end',
    )

    start_playoff_date = models.DateField(
        blank=True,
        null=True,
        help_text='The date when the playoff season is scheduled to begin',
    )
    end_playoff_date = models.DateField(
        blank=True,
        null=True,
        help_text='The date when the playoff season is scheduled to end',
    )

    is_selling_season = models.BooleanField(
        default=False,
        help_text='A boolean indicating if the season is currently in the selling period',
    )
    is_regular_season = models.BooleanField(
        default=False,
        help_text='A boolean indicating if the season is currently in the regular season period',
    )
    is_playoff_season = models.BooleanField(
        default=False,
        help_text='A boolean indicating if the season is currently in the playoff period',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()

    class Meta:
        db_table = 'content"."season'
        verbose_name = 'Season'
        verbose_name_plural = 'Seasons'
        constraints = (
            UniqueConstraint(
                fields=('name', 'league', 'start_year'),
                name='unique_season_details',
            ),
        )

    def __str__(self):
        return f'{self.name} - {self.league}'
