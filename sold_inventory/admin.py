from django.contrib import admin

from .Resource import MLBSoldInventoryResource
from .models import *

from import_export.admin import ImportExportModelAdmin


class MLBSoldInventoryAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = MLBSoldInventoryResource
    save_as = True
    save_on_top = True
    list_display = ('id', 'vendor', 'event_name', 'event_date')
    # list_display_links = ('first_name', 'last_name', 'email', )
    search_fields = ('id', )
    # list_filter = ('team', 'created_by')
    # readonly_fields = ('created_at', 'last_opened')


admin.site.register(MLBSoldInventory, MLBSoldInventoryAdmin)
admin.site.site_header = "Lew & Dowski"


