from datetime import datetime

from rangefilter.filters import DateRangeFilterBuilder

from django.contrib import admin
from django.forms import Select

from apps.stt.admin.base import BaseModelAdmin, TeamEventInline
from apps.stt.filters import FutureEventsFilter, HomeAwayFilter
from apps.stt.models import Event
from apps.stt.resources import EventResource
from config.components.business_related import SUPPORTED_LEAGUES


@admin.register(Event)
class EventAdminConfig(BaseModelAdmin):
    model = Event
    resource_class = EventResource
    save_as = True
    save_on_top = True
    ordering = ('date_time',)
    list_display = (
        'name',
        'associated_teams',
        'additional_info',
        'league',
        'date_time',
        'season',
        'id',
    )
    readonly_fields = ('id',)
    list_display_links = ('name',)
    inlines = (TeamEventInline,)
    search_fields = ('id', 'name', 'season__name')
    list_filter = (
        (
            'date_time',
            DateRangeFilterBuilder(
                title='Event date',
                default_start=datetime.now(),
                default_end=datetime.now(),
            ),
        ),
        'season__name',
        'league',
        HomeAwayFilter,
        FutureEventsFilter,
    )
    autocomplete_fields = ('season', 'venue')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.prefetch_related('teamevent_set__team')
        return queryset

    def associated_teams(self, obj):
        teams = [te.team.name for te in obj.teamevent_set.all()]
        if len(teams) == 2:
            return f'{teams[0]}, {teams[1]}'
        return ', '.join(teams)

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'league':
            kwargs['widget'] = Select(choices=((league, league) for league in SUPPORTED_LEAGUES))
        return super().formfield_for_dbfield(db_field, request, **kwargs)

    associated_teams.short_description = 'Teams'
