from django.contrib import admin

from .Resource import AccountsResource
from .models import *

from import_export.admin import ImportExportModelAdmin


class AccountsAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = AccountsResource
    save_as = True
    save_on_top = True
    list_display = ('id', 'first_name', 'last_name', 'email')
    list_display_links = ('first_name', 'last_name', 'email', )
    search_fields = ('id', 'first_name', 'last_name', 'email', 'team', 'created_by')
    list_filter = ('team', 'created_by')
    readonly_fields = ('created_at', 'last_opened')


admin.site.register(Accounts, AccountsAdmin)

