from django.contrib import admin, messages
from django.utils.translation import ngettext

from .Resource import AccountsResource
from .models import *

from import_export.admin import ImportExportModelAdmin


class AccountsAdmin(ImportExportModelAdmin):
    resource_classes = [AccountsResource]
    save_as = True
    save_on_top = True
    list_display = ('id', 'first_name', 'last_name', 'email', 'disabled')
    list_display_links = ('first_name', 'last_name', 'email',)
    search_fields = ('id', 'first_name', 'last_name', 'email', 'team', 'created_by__username')
    list_filter = ('team', 'created_by__username', 'ld_computer_used', 'last_opened')
    # readonly_fields = ('created_at', 'updated_at', 'last_opened')
    actions = ['make_disabled', 'make_enabled']
    # inlines = [
    #     'UserInline',
    # ]

    @admin.action(description='Mark selected accounts as disabled', permissions=['change'])
    def make_disabled(self, request, queryset):
        updated = queryset.update(disabled=True)
        self.message_user(request, ngettext(
            '%d account was successfully marked as disabled.',
            '%d accounts were successfully marked as disabled.',
            updated,
        ) % updated, messages.SUCCESS)

    @admin.action(description='Mark selected accounts as enabled', permissions=['change'])
    def make_enabled(self, request, queryset):
        updated = queryset.update(disabled=False)
        self.message_user(request, ngettext(
            '%d account was successfully marked as enabled.',
            '%d accounts were successfully marked as enabled.',
            updated,
        ) % updated, messages.SUCCESS)


admin.site.register(Accounts, AccountsAdmin)
admin.site.site_header = "Lew & Dowski"
