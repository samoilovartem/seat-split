from django.contrib import admin
from .models import *

from import_export.admin import ImportExportModelAdmin


class AccountsAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    save_as = True
    save_on_top = True
    list_display = ('id', 'full_name', 'email')
    list_display_links = ('full_name', )
    search_fields = ('id', 'full_name', 'email', 'team', 'created_by')
    list_filter = ('id', 'full_name', 'email', 'team', 'created_by')
    readonly_fields = ('created_at', 'updated_at')


admin.site.register(Accounts, AccountsAdmin)

