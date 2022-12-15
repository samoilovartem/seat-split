from django.contrib import admin, messages
from django.utils.translation import ngettext

from import_export.admin import ImportExportModelAdmin

from .models import *


class CardsAdminConfig(ImportExportModelAdmin, admin.ModelAdmin):
    save_as = True
    save_on_top = True
    list_display = ('id', 'account_assigned', 'platform', 'type',
                    'parent_card', 'card_number', 'expiration_date', 'cvv_number', 'updated_at',
                    'in_tm', 'in_tickets_com', 'is_deleted', 'team', 'specific_team')
    list_display_links = ('id', 'account_assigned')
    search_fields = ('account_assigned', 'platform', 'type', 'parent_card',
                     'card_number')
    list_filter = ('platform', 'type', 'updated_at', 'parent_card', 'in_tm', 'in_tickets_com',
                   'team', 'specific_team', 'is_deleted')
    readonly_fields = ('created_at', 'updated_at',)
    actions = ['mark_deleted', 'mark_not_deleted']

    @admin.action(description='Mark selected cards as deleted', permissions=['change'])
    def mark_deleted(self, request, queryset):
        updated = queryset.update(is_deleted=True)
        self.message_user(request, ngettext(
            '%d card was successfully marked as deleted.',
            '%d cards were successfully marked as deleted.',
            updated,
        ) % updated, messages.SUCCESS)

    @admin.action(description='Mark selected cards as not deleted', permissions=['change'])
    def mark_not_deleted(self, request, queryset):
        updated = queryset.update(is_deleted=False)
        self.message_user(request, ngettext(
            '%d card was successfully marked as NOT deleted.',
            '%d cards were successfully marked as NOT deleted.',
            updated,
        ) % updated, messages.SUCCESS)


admin.site.register(Cards, CardsAdminConfig)
