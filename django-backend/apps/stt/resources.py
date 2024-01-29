from apps.stt.models import Event, Team, TeamEvent, Venue
from dateutil.parser import parser
from import_export.fields import Field
from import_export.resources import ModelResource
from import_export.widgets import ForeignKeyWidget


class EventResource(ModelResource):
    skybox_venue_id = Field(
        attribute='venue',
        column_name='skybox_venue_id',
        widget=ForeignKeyWidget(Venue, 'skybox_venue_id'),
    )

    def before_import_row(self, row, **kwargs):
        """Perform actions before a row is imported."""
        venue_id = row.get('skybox_venue_id')
        if venue_id:
            try:
                venue = Venue.objects.get(skybox_venue_id=venue_id)
                row['venue'] = venue.pk
            except Venue.DoesNotExist:
                row['venue'] = None

        date_time_str = row.get('date_time')
        if date_time_str:
            try:
                date_time_parser = parser()
                parsed_date_time = date_time_parser.parse(timestr=date_time_str)
                row['date_time'] = parsed_date_time
            except ValueError:
                row['date_time'] = None

    def after_import_row(self, row, row_result, **kwargs):
        """
        Perform actions after a row has been imported.
        """
        event_instance = self._meta.model.objects.get(
            name=row.get('name'),
            date_time=row.get('date_time'),
            season=row.get('season'),
        )

        team_names = row.get('name').split(' at ')
        for team_name in team_names:
            try:
                team = Team.objects.get(name=team_name)
                TeamEvent.objects.create(event=event_instance, team=team)
            except Team.DoesNotExist:
                raise ValueError(f'Team {team_name} does not exist')

    class Meta:
        model = Event
        import_id_fields = ('id',)
        fields = (
            'id',
            'skybox_event_id',
            'name',
            'additional_info',
            'date_time',
            'season',
            'venue',
            'stubhub_event_url',
            'league',
        )
        skip_unchanged = True
        report_skipped = True
