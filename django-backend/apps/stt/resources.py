from import_export.resources import ModelResource

from apps.stt.models import Event, Team, TeamEvent


class EventResource(ModelResource):
    def after_import_row(self, row, row_result, **kwargs):
        event = self._meta.model.objects.get(
            name=row.get('name'),
            date_time=row.get('date_time'),
            season=row.get('season'),
        )
        team_names = row.get('name').split(' vs ')

        for team_name in team_names:
            team = Team.objects.get(name=team_name)
            TeamEvent.objects.create(event=event, team=team)

    class Meta:
        model = Event
