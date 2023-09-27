from django_filters.rest_framework import FilterSet

from django.contrib.admin import SimpleListFilter

from apps.stt.models import Event, Team, TeamEvent
from config.settings import BOOL_LOOKUPS, CHAR_LOOKUPS, DATE_AND_ID_LOOKUPS  # noqa


class TeamFilterSet(FilterSet):
    class Meta:
        model = Team
        fields = {
            'id': DATE_AND_ID_LOOKUPS,
            'league': CHAR_LOOKUPS,
            'city': CHAR_LOOKUPS,
            'name': CHAR_LOOKUPS,
        }


class EventFilterSet(FilterSet):
    class Meta:
        model = Event
        fields = {
            'name': CHAR_LOOKUPS,
            'date_time': DATE_AND_ID_LOOKUPS,
        }


class LeagueListFilter(SimpleListFilter):
    """
    This class provides a filter for the Events based on their associated teams' leagues.
    """

    title = 'League'
    parameter_name = 'league'

    def lookups(self, request, model_admin):
        """
        Builds a queryset for all unique leagues and prepares a tuple for each,
        returning a list of tuples, each representing a league.

        :param request: The current request.
        :param model_admin: The model admin using this filter.
        :return: A list of tuples for all unique leagues.
        """
        team_events = TeamEvent.objects.only('team__league').all()

        leagues = set([c['team__league'] for c in team_events.values('team__league')])

        return [(league, league) for league in leagues]

    def queryset(self, request, queryset):
        """
        Filters the queryset based on the selected league.

        :param request: The current request.
        :param queryset: The existing queryset for this model.
        :return: A filtered queryset.
        """
        if self.value():
            return queryset.filter(teamevent__team__league__icontains=self.value())
        else:
            return queryset
