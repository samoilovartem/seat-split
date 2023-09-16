from import_export.admin import ImportExportMixin
from simple_history.admin import SimpleHistoryAdmin

from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet
from django.utils.html import format_html

from apps.common_services.utils import show_changed_fields
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


class TicketHolderAdminConfig(admin.ModelAdmin):
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

    inlines = (TicketHolderTeamInline,)

    def get_email(self, obj):
        return obj.user.email

    get_email.short_description = 'User email'


class TicketAdminConfig(admin.ModelAdmin):
    model = Ticket
    save_as = True
    save_on_top = True
    list_display = (
        'id',
        'ticket_holder',
        'event',
        'skybox_event_id',
    )
    list_display_links = ('id',)


class PurchaseAdminConfig(admin.ModelAdmin):
    model = Purchase
    save_as = True
    save_on_top = True
    list_display = (
        'id',
        'ticket',
        'invoice_number',
        'customer',
        'delivery_status',
    )
    list_display_links = ('id',)


class EventAdminConfig(ImportExportMixin, SimpleHistoryAdmin):
    model = Event
    resource_class = EventResource
    save_as = True
    save_on_top = True
    list_display = (
        'id',
        'associated_teams',
        'date_time',
        'season',
    )
    list_display_links = ('id',)
    inlines = (TeamEventInline,)
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

    def associated_teams(self, obj):
        teams = [te.team.name for te in obj.teamevent_set.all()]
        if len(teams) == 2:
            return f'{teams[0]} vs {teams[1]}'
        return ', '.join(teams)

    associated_teams.short_description = 'Teams'


class TeamAdminConfig(admin.ModelAdmin):
    model = Team
    save_as = True
    save_on_top = True
    list_display = (
        'id',
        'name',
        'league',
        'city',
        'state',
    )
    list_display_links = ('id',)
    search_fields = (
        'name',
        'league',
        'city',
        'state',
    )


admin.site.register(TicketHolder, TicketHolderAdminConfig)
admin.site.register(Ticket, TicketAdminConfig)
admin.site.register(Purchase, PurchaseAdminConfig)
admin.site.register(Event, EventAdminConfig)
admin.site.register(Team, TeamAdminConfig)
