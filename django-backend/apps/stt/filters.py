from django_filters.rest_framework import FilterSet

from django.contrib.admin import SimpleListFilter
from django.utils import timezone

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
            return queryset.filter(
                teamevent__team__league__icontains=self.value()
            ).distinct()
        else:
            return queryset


class HomeAwayFilter(SimpleListFilter):
    """
    Custom filter for Django admin that filters events based on whether they're 'home' or 'away' games
    for the team searched for in the search bar.
    """

    title = 'home / away'
    parameter_name = 'home_away'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each tuple is the coded value
        for the option that will appear in the URL query. The second element is the
        human-readable name for the option that will appear in the right sidebar.
        """
        return [
            ('home', 'Home'),
            ('away', 'Away'),
        ]

    def queryset(self, request, queryset):
        """
        Returns a queryset of events filtered based on whether they're 'home' or 'away'
        games for the team searched for in the search bar. If no valid 'home' or 'away'
        value is provided or no team name is searched, the unaltered queryset is returned.
        """
        if not self.value():
            return queryset

        team_name = request.GET.get('q', '')

        if not team_name:
            return queryset

        search_string = team_name.strip()

        if self.value() == 'home':
            return queryset.filter(name__icontains=f' at {search_string}')
        elif self.value() == 'away':
            return queryset.filter(name__icontains=f'{search_string} at')

        return queryset


class FutureEventsFilter(SimpleListFilter):
    """
    This class provides a filter for the Events based on their date. By default, only future events
    (i.e., events with a 'date_time' field value greater than or equal to the current time) are displayed.
    An option is provided to display all events, including those in the past.
    """

    title = 'Future events'
    parameter_name = 'future_events'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples to be displayed in the filter sidebar. Each tuple represents
        a filter option and contains a URL query parameter and its human-readable counterpart.
        """
        return (('all events (including past)', 'All events (including past)'),)

    def queryset(self, request, queryset):
        """
        Filters the queryset based on the chosen filter option.

        If 'all events (including past)' is chosen, all instances of the model will be returned.
        By default, or if no choice is selected, only instances representing future events
        will be returned.
        """
        if self.value() == 'all events (including past)':
            return queryset
        return queryset.filter(date_time__gte=timezone.now())
