from django.contrib import admin
from .models import *

from import_export.admin import ImportExportModelAdmin
from rest_framework.authtoken.admin import TokenAdmin

TokenAdmin.raw_id_fields = ['user']


class AccountsAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    # prepopulated_fields = {'slug': ('title',)}
    save_as = True
    save_on_top = True
    list_display = ('id', 'account_assigned', 'platform', 'type', 'parent_card',
                    'updated_at')
    list_display_links = ('id', 'account_assigned')
    search_fields = ('account_assigned', 'platform', 'parent_card', 'card_number',
                     'in_tm')
    list_filter = ('updated_at', 'parent_card', 'in_tm')
    # readonly_fields = ('views', 'created_at', 'get_photo', 'updated_at')
    # fields = ('account_assigned', 'platform',)


admin.site.register(LawnsAccounts, AccountsAdmin)
