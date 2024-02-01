from import_export.admin import ImportExportMixin

from django.contrib import admin

from apps.stt.models import Venue


@admin.register(Venue)
class VenueAdminConfig(ImportExportMixin, admin.ModelAdmin):
    model = Venue
    save_as = True
    save_on_top = True
    ordering = ('-created_at',)
    list_display = (
        'name',
        'address',
        'city',
        'state',
        'id',
    )
    readonly_fields = ('id',)
    list_display_links = ('name',)
    search_fields = (
        'id',
        'skybox_venue_id',
        'name',
        'address',
        'city',
        'state',
    )
    list_filter = ('state',)
