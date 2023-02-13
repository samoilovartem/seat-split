from django.contrib import admin
from import_export.admin import ImportExportMixin
from simple_history.admin import SimpleHistoryAdmin

from apps.mobile_numbers.models import MobileNumberTransaction


class MobileNumberAdminConfig(ImportExportMixin, SimpleHistoryAdmin):
    save_as = True
    save_on_top = True
    autocomplete_fields = ('email',)
    list_display = (
        'id',
        'phone',
        'email',
        'service_name',
        'order_id',
        'requested_by',
    )
    fields = (
        'id',
        'phone',
        'email',
        'requested_by',
        'service_name',
        'order_id',
        'service_id',
        'service_main_response',
        'account_created',
        'created_at',
        'updated_at',
    )
    readonly_fields = (
        'id',
        'created_at',
        'updated_at',
    )
    history_list_display = ('status',)


admin.site.register(MobileNumberTransaction, MobileNumberAdminConfig)
