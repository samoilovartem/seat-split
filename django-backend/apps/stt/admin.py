from import_export.admin import ImportExportMixin
from simple_history.admin import SimpleHistoryAdmin

from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet, Select
from django.utils.html import format_html

from apps.common_services.utils import show_changed_fields
from apps.stt.filters import LeagueListFilter
from apps.stt.models import (
    Event,
    Purchase,
    Team,
    TeamEvent,
    Ticket,
    TicketHolder,
    TicketHolderTeam,
)
from apps.stt.resources import EventResource
from config.settings import DELIVERY_STATUSES, LISTING_STATUSES


class BaseModelAdmin(SimpleHistoryAdmin):
    history_list_display = ('changed_fields', 'list_changes', 'status')

    @staticmethod
    def changed_fields(obj):
        if obj.prev_record:
            delta = obj.diff_against(obj.prev_record)
            return delta.changed_fields
        return None

    @staticmethod
    def list_changes(obj):
        fields = ''
        if obj.prev_record:
            fields = show_changed_fields(obj, fields)
            return format_html(fields)
        return None


class TeamEventFormset(BaseInlineFormSet):
    def clean(self):
        super(TeamEventFormset, self).clean()

        count = sum(1 for form in self.forms if not form.cleaned_data.get('DELETE'))

        if count > 2:
            raise ValidationError(
                'You can associate a maximum of 2 teams with an event.'
            )


class TeamEventInline(admin.TabularInline):
    model = TeamEvent
    extra = 0
    autocomplete_fields = ('team',)
    formset = TeamEventFormset


class TicketHolderTeamInline(admin.TabularInline):
    model = TicketHolderTeam
    extra = 0
    readonly_fields = (
        'credentials_website_username',
        'credentials_website_password',
    )


@admin.register(TicketHolder)
class TicketHolderAdminConfig(BaseModelAdmin):
    model = TicketHolder
    save_as = True
    save_on_top = True
    list_display = (
        'first_name',
        'last_name',
        'get_email',
        'id',
    )
    list_display_links = (
        'first_name',
        'last_name',
        'get_email',
    )
    search_fields = (
        'first_name',
        'last_name',
        'user__email',
    )
    inlines = (TicketHolderTeamInline,)
    autocomplete_fields = ('user',)

    def get_email(self, obj):
        return obj.user.email

    get_email.short_description = 'User email'


@admin.register(Ticket)
class TicketAdminConfig(BaseModelAdmin):
    model = Ticket
    save_as = True
    save_on_top = True
    list_display = (
        'event',
        'ticket_holder',
        'skybox_event_id',
        'id',
    )
    search_fields = (
        'ticket_holder__first_name',
        'ticket_holder__last_name',
        'event__name',
    )
    list_display_links = ('event',)
    autocomplete_fields = ('event', 'ticket_holder')

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'listing_status':
            kwargs['widget'] = Select(choices=LISTING_STATUSES)
        return super().formfield_for_dbfield(db_field, request, **kwargs)


@admin.register(Purchase)
class PurchaseAdminConfig(admin.ModelAdmin):
    model = Purchase
    save_as = True
    save_on_top = True
    list_display = (
        'ticket',
        'invoice_number',
        'customer',
        'delivery_status',
        'id',
    )
    list_display_links = ('ticket',)
    autocomplete_fields = ('ticket',)

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'delivery_status':
            kwargs['widget'] = Select(choices=DELIVERY_STATUSES)
        return super().formfield_for_dbfield(db_field, request, **kwargs)


@admin.register(Event)
class EventAdminConfig(ImportExportMixin, BaseModelAdmin):
    model = Event
    resource_class = EventResource
    save_as = True
    save_on_top = True
    list_display = (
        'name',
        'associated_teams',
        'event_league',
        'date_time',
        'season',
        'id',
    )
    list_display_links = ('name',)
    inlines = (TeamEventInline,)
    search_fields = ('name', 'season')
    ordering = ('date_time',)
    list_filter = ('season', LeagueListFilter)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.prefetch_related('teamevent_set__team')
        return queryset

    def associated_teams(self, obj):
        teams = [te.team.name for te in obj.teamevent_set.all()]
        if len(teams) == 2:
            return f'{teams[0]}, {teams[1]}'
        return ', '.join(teams)

    def event_league(self, obj):
        teams_leagues = [te.team.league for te in obj.teamevent_set.all()]
        if teams_leagues[0] == teams_leagues[1]:
            return teams_leagues[0]
        return ', '.join(teams_leagues)

    associated_teams.short_description = 'Teams'
    event_league.short_description = 'League'


@admin.register(Team)
class TeamAdminConfig(ImportExportMixin, admin.ModelAdmin):
    model = Team
    save_as = True
    save_on_top = True
    list_display = (
        'name',
        'league',
        'city',
        'state',
        'id',
    )
    list_display_links = ('name',)
    search_fields = (
        'name',
        'league',
        'city',
        'state',
    )
    list_filter = ('league',)


admin.site.site_header = 'Season Tickets Tech Admin Dashboard'
admin.site.site_url = None
