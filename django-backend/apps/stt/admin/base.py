from simple_history.admin import SimpleHistoryAdmin

from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet
from django.utils.html import format_html

from apps.common_services.utils import show_changed_fields
from apps.stt.models import TeamEvent, TicketHolderTeam


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
            raise ValidationError('You can associate a maximum of 2 teams with an event.')


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


admin.site.site_header = 'Season Tickets Tech Admin Dashboard'
admin.site.site_url = None
