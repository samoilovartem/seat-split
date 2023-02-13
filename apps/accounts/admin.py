from django.contrib import admin, messages
from django.utils.translation import ngettext
from import_export.admin import ImportExportMixin
from simple_history.admin import SimpleHistoryAdmin

from apps.accounts.models import Accounts
from apps.accounts.resource import AccountsResource


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
    )
    list_display_links = (
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
    )
    actions = (
        'make_disabled',
        'make_enabled',
    )
    history_list_display = ('status',)

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
