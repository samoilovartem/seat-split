from django.contrib import admin
from .models import *

from import_export.admin import ImportExportModelAdmin


class AccountsAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    # prepopulated_fields = {'slug': ('title',)}
    save_as = True
    save_on_top = True
    list_display = ('id', 'account_assigned', 'platform', 'type', 'parent_card',
                    'updated_at', 'in_tm', 'in_tickets_com', 'team')
    list_display_links = ('id', 'account_assigned')
    search_fields = ('account_assigned', 'platform', 'type', 'parent_card',
                     'card_number')
    list_filter = ('platform', 'type', 'updated_at', 'parent_card', 'in_tm', 'in_tickets_com',
                   'team')
    readonly_fields = ('created_at', 'updated_at')
    # fields = ('account_assigned', 'platform',)


admin.site.register(Cards, AccountsAdmin)
