from datetime import datetime

from import_export.admin import ImportExportMixin
from rangefilter.filters import DateRangeFilterBuilder
from simple_history.admin import SimpleHistoryAdmin

from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet, Select
from django.utils.html import format_html

from apps.common_services.utils import show_changed_fields
from apps.stt.filters import FutureEventsFilter, HomeAwayFilter
from apps.stt.forms import TicketAdminForm
from apps.stt.models import (
    Event,
    Purchase,
    Season,
    Team,
    TeamEvent,
    Ticket,
    TicketHolder,
    TicketHolderTeam,
    Venue,
)
from apps.stt.resources import EventResource
from config.components.business_related import (
    DELIVERY_STATUSES,
    LISTING_STATUSES,
    MARKETPLACES,
)


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


class TicketHolderTeamInline(admin.StackedInline):
    model = TicketHolderTeam
    extra = 0
    readonly_fields = (
        'seats_quantity',
        'credentials_website_username',
        'credentials_website_password',
    )


@admin.register(Season)
class SeasonAdminConfig(BaseModelAdmin):
    model = Season
    save_as = True
    save_on_top = True
    list_display = (
        'name',
        'league',
        'start_year',
        'official_start_date',
        'official_end_date',
        'id',
    )
    readonly_fields = ('id',)
    list_display_links = ('name',)
    search_fields = ('id', 'name')
    ordering = ('name',)
    list_filter = (
        'league',
        (
            'official_start_date',
            DateRangeFilterBuilder(
                title='Official start date',
                default_start=datetime.now(),
            ),
        ),
        (
            'official_end_date',
            DateRangeFilterBuilder(
                title='Official end date',
                default_start=datetime.now(),
            ),
        ),
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
    readonly_fields = ('id', 'created_at')
    list_display_links = (
        'first_name',
        'last_name',
        'get_email',
    )
    search_fields = (
        'id',
        'first_name',
        'last_name',
        'user__email',
    )
    exclude = ('tickets_data',)
    inlines = (TicketHolderTeamInline,)
    autocomplete_fields = ('user',)

    def get_email(self, obj):
        return obj.user.email

    get_email.short_description = 'User email'


@admin.register(Ticket)
class TicketAdminConfig(BaseModelAdmin):
    model = Ticket
    form = TicketAdminForm
    save_as = True
    save_on_top = True
    ordering = ('-created_at',)
    list_display = (
        'event',
        'ticket_holder',
        'listing_status',
        'section',
        'row',
        'seat',
        'price',
        'id',
    )
    readonly_fields = ('id', 'created_at', 'sold_at')
    search_fields = (
        'id',
        'ticket_holder__id',
        'ticket_holder__user__email',
        'ticket_holder__first_name',
        'ticket_holder__last_name',
        'event__name',
    )
    list_filter = (
        'listing_status',
        (
            'created_at',
            DateRangeFilterBuilder(
                title='Created At',
                default_start=datetime.now(),
            ),
        ),
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
    search_fields = (
        'id',
        'ticket__id',
        'ticket__ticket_holder__first_name',
        'ticket__ticket_holder__last_name',
        'ticket__event__name',
    )
    readonly_fields = ('id',)
    list_filter = (
        'customer',
        'delivery_status',
        (
            'created_at',
            DateRangeFilterBuilder(
                title='Created At',
                default_start=datetime.now(),
            ),
        ),
    )
    list_display_links = ('ticket',)
    autocomplete_fields = ('ticket',)

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'delivery_status':
            kwargs['widget'] = Select(choices=DELIVERY_STATUSES)
        if db_field.name == 'customer':
            kwargs['widget'] = Select(choices=MARKETPLACES)
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
        'league',
        'date_time',
        'season',
        'id',
    )
    readonly_fields = ('id',)
    list_display_links = ('name',)
    inlines = (TeamEventInline,)
    search_fields = ('id', 'name', 'season__name')
    ordering = ('date_time',)
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

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.prefetch_related('teamevent_set__team')
        return queryset

    def associated_teams(self, obj):
        teams = [te.team.name for te in obj.teamevent_set.all()]
        if len(teams) == 2:
            return f'{teams[0]}, {teams[1]}'
        return ', '.join(teams)

    associated_teams.short_description = 'Teams'


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
    readonly_fields = ('id',)
    list_display_links = ('name',)
    search_fields = (
        'id',
        'name',
        'league',
        'city',
        'state',
    )
    list_filter = ('league',)


@admin.register(Venue)
class VenueAdminConfig(ImportExportMixin, admin.ModelAdmin):
    model = Venue
    save_as = True
    save_on_top = True
    list_display = (
        'name',
        'address',
        'city',
        'state',
        'id',
    )
    readonly_fields = ('id',)
    list_display_links = ('name',)
    search_fields = (
        'id',
        'name',
        'address',
        'city',
        'state',
    )
    list_filter = ('state',)


admin.site.site_header = 'Season Tickets Tech Admin Dashboard'
admin.site.site_url = None
