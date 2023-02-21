from django.contrib import admin, messages
from django.utils.html import format_html
from django.utils.translation import ngettext
from import_export.admin import ImportExportMixin
from simple_history.admin import SimpleHistoryAdmin

from apps.accounts.models import Accounts
from apps.accounts.resource import AccountsResource
from apps.utils import show_changed_fields


class AccountsAdminConfig(ImportExportMixin, SimpleHistoryAdmin):
    resource_classes = [AccountsResource]
    save_as = True
    save_on_top = True
    list_display = (
        'id',
        'first_name',
        'last_name',
        'disabled',
        'email',
        'password',
        'recovery_email',
        'ld_computer_used',
        'last_opened',
        'team',
        'specific_team',
        'updated_at',
        'created_at',
    )
    list_display_links = (
        'id',
        'first_name',
        'last_name',
    )
    search_fields = (
        'id',
        'first_name',
        'last_name',
        'email',
        'team',
        'created_by',
    )
    list_filter = (
        'team',
        'specific_team',
        'disabled',
        'created_by',
        'ld_computer_used',
        'last_opened',
        'updated_at',
        'created_at',
    )
    actions = (
        'make_disabled',
        'make_enabled',
    )
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

    @admin.action(
        description='Mark selected accounts as disabled', permissions=['change']
    )
    def make_disabled(self, request, queryset):
        updated = queryset.update(disabled=True)
        self.message_user(
            request,
            ngettext(
                '%d account was successfully marked as disabled.',
                '%d accounts were successfully marked as disabled.',
                updated,
            )
            % updated,
            messages.SUCCESS,
        )

    @admin.action(
        description='Mark selected accounts as enabled', permissions=['change']
    )
    def make_enabled(self, request, queryset):
        updated = queryset.update(disabled=False)
        self.message_user(
            request,
            ngettext(
                '%d account was successfully marked as enabled.',
                '%d accounts were successfully marked as enabled.',
                updated,
            )
            % updated,
            messages.SUCCESS,
        )


admin.site.register(Accounts, AccountsAdminConfig)
admin.site.site_header = "Lew & Dowski"
