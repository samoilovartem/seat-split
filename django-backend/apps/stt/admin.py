from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from apps.stt.models import Event, Purchase, Team, TeamEvent, Ticket, TicketHolder


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


class TicketHolderAdminConfig(admin.ModelAdmin):
    model = TicketHolder
    save_as = True
    save_on_top = True
    list_display = (
        'id',
        'first_name',
        'last_name',
        'phone',
    )
    list_display_links = (
        'first_name',
        'last_name',
    )


class TicketAdminConfig(admin.ModelAdmin):
    model = Ticket
    save_as = True
    save_on_top = True
    list_display = (
        'id',
        'user',
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


class EventAdminConfig(admin.ModelAdmin):
    model = Event
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
