from django.contrib import admin
from .models import *

from import_export.admin import ImportExportModelAdmin


class AccountsAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    # prepopulated_fields = {'slug': ('title',)}
    save_as = True
    save_on_top = True
    list_display = ('id', 'account_assigned', 'platform', 'type', 'parent_card',
                    'created_by', 'team', 'updated_at')
    list_display_links = ('id', 'account_assigned')
    search_fields = ('account_assigned', 'platform', 'card_number', 'created_by',
                     'team', 'in_tm', 'in_tickets_com')
    list_filter = ('created_by',
                   'team', 'in_tm', 'in_tickets_com')
    # readonly_fields = ('views', 'created_at', 'get_photo', 'updated_at')
    # fields = ('account_assigned', 'platform',)


admin.site.register(Accounts, AccountsAdmin)
