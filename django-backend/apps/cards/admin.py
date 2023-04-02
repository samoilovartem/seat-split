from import_export.admin import ImportExportMixin
from simple_history.admin import SimpleHistoryAdmin

from django.contrib import admin, messages
from django.utils.html import format_html
from django.utils.translation import ngettext

from apps.cards.models import Cards
from apps.utils import show_changed_fields


class CardsAdminConfig(ImportExportMixin, SimpleHistoryAdmin):
    save_as = True
    save_on_top = True
    list_display = (
        'id',
        'account_assigned',
        'platform',
        'type',
        'parent_card',
        'card_number',
        'expiration_date',
        'cvv_number',
        'updated_at',
        'in_tm',
        'in_tickets_com',
        'is_deleted',
        'team',
        'specific_team',
    )
    list_display_links = ('id', 'account_assigned')
    search_fields = (
        'account_assigned',
        'platform',
        'type',
        'parent_card',
        'card_number',
    )
    list_filter = (
        'platform',
        'type',
        'updated_at',
        'parent_card',
        'in_tm',
        'in_tickets_com',
        'team',
        'specific_team',
        'is_deleted',
    )
    readonly_fields = (
        'created_at',
        'updated_at',
    )
    actions = ['mark_deleted', 'mark_not_deleted']
    history_list_display = ('changed_fields', 'list_changes', 'status')

    def changed_fields(self, obj):
        if obj.prev_record:
            delta = obj.diff_against(obj.prev_record)
            return delta.changed_fields
        return None

    def list_changes(self, obj):
        fields = ''
        if obj.prev_record:
            fields = show_changed_fields(obj, fields)
            return format_html(fields)
        return None

    @admin.action(description='Mark selected cards as deleted', permissions=['change'])
    def mark_deleted(self, request, queryset):
        updated = queryset.update(is_deleted=True)
        self.message_user(
            request,
            ngettext(
                '%d card was successfully marked as deleted.',
                '%d cards were successfully marked as deleted.',
                updated,
            )
            % updated,
            messages.SUCCESS,
        )

    @admin.action(
        description='Mark selected cards as not deleted', permissions=['change']
    )
    def mark_not_deleted(self, request, queryset):
        updated = queryset.update(is_deleted=False)
        self.message_user(
            request,
            ngettext(
                '%d card was successfully marked as NOT deleted.',
                '%d cards were successfully marked as NOT deleted.',
                updated,
            )
            % updated,
            messages.SUCCESS,
        )


admin.site.register(Cards, CardsAdminConfig)
