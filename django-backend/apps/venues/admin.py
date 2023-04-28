from import_export.admin import ImportExportMixin

from django.contrib import admin

from apps.venues.models import Venues


class VenuesAdminConfig(ImportExportMixin, admin.ModelAdmin):
    save_as = True
    save_on_top = True
    list_display = (
        'id',
        'name',
        'address',
        'city',
        'state_code',
        'country_code',
        'postal_code',
    )
    readonly_fields = (
        'id',
        'created_at',
        'updated_at',
    )
    search_fields = (
        'address',
        'city',
        'state_code',
    )
    list_filter = (
        'state_code',
        'country_code',
    )


admin.site.register(Venues, VenuesAdminConfig)
