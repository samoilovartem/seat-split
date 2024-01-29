from import_export.admin import ImportExportMixin
from simple_history.admin import SimpleHistoryAdmin

from django.contrib import admin
from django.utils.html import format_html

from apps.common_services.utils import show_changed_fields
from apps.email_domains.models import EmailDomains
from apps.email_domains.resource import EmailDomainsResource


class EmailDomainsAdminConfig(ImportExportMixin, SimpleHistoryAdmin):
    resource_classes = [EmailDomainsResource]
    save_as = True
    save_on_top = True
    list_display = (
        'id',
        'domain_name',
        'status',
        'expiration_date',
        'auto_renew',
        'type',
    )
    list_display_links = (
        'id',
        'domain_name',
    )
    search_fields = (
        'id',
        'domain_name',
        'type',
    )
    list_filter = (
        'type',
        'expiration_date',
        'status',
    )
    actions = (
        'make_disabled',
        'make_enabled',
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


admin.site.register(EmailDomains, EmailDomainsAdminConfig)
