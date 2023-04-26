from import_export.admin import ImportExportMixin

from django.contrib import admin

from apps.us_addresses.models import USAddresses


class USAddressesAdminConfig(ImportExportMixin, admin.ModelAdmin):
    save_as = True
    save_on_top = True
    list_display = (
        'id',
        'line',
        'city',
        'state',
        'country',
        'postal_code',
    )
    readonly_fields = (
        'id',
        'created_at',
        'updated_at',
    )
    search_fields = (
        'line',
        'city',
        'state',
    )
    list_filter = ('state',)


admin.site.register(USAddresses, USAddressesAdminConfig)
