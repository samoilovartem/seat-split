from django.contrib import admin
from django.utils.html import format_html
from import_export.admin import ImportExportMixin
from simple_history.admin import SimpleHistoryAdmin

from apps.mobile_numbers.models import MobileNumberTransaction
from apps.utils import show_changed_fields


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
    readonly_fields = (
        'id',
        'created_at',
        'updated_at',
    )
    history_list_display = ('changed_fields', 'list_changes', 'status')

    def changed_fields(self, obj):
        if obj.prev_record:
            delta = obj.diff_against(obj.prev_record)
            return delta.changed_fields
        return None

    def list_changes(self, obj):
        fields = ''
        if obj.prev_record:
            fields = show_changed_fields(obj, fields)
            return format_html(fields)
        return None


admin.site.register(MobileNumberTransaction, MobileNumberAdminConfig)
