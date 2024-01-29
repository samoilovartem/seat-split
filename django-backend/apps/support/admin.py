from datetime import datetime

from apps.support.models import Inquiry
from django.contrib import admin
from rangefilter.filters import DateRangeFilterBuilder
from simple_history.admin import SimpleHistoryAdmin


@admin.register(Inquiry)
class InquiryAdminConfig(SimpleHistoryAdmin):
    model = Inquiry
    save_as = True
    save_on_top = True
    list_display = (
        'first_name',
        'last_name',
        'email',
        'subject',
        'id',
    )
    readonly_fields = ('id', 'created_at')
    list_display_links = (
        'first_name',
        'last_name',
        'email',
    )
    search_fields = (
        'id',
        'first_name',
        'last_name',
        'email',
        'subject',
    )
    list_filter = (
        (
            'created_at',
            DateRangeFilterBuilder(
                title='Sent At',
                default_start=datetime.now(),
            ),
        ),
    )
    exclude = ('tickets_data',)
