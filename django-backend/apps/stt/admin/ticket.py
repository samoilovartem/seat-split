from datetime import datetime

from rangefilter.filters import DateRangeFilterBuilder

from django.contrib import admin
from django.forms import Select

from apps.stt.admin.base import BaseModelAdmin
from apps.stt.forms import TicketAdminForm
from apps.stt.models import Ticket
from config.components.business_related import LISTING_STATUSES


@admin.register(Ticket)
class TicketAdminConfig(BaseModelAdmin):
    model = Ticket
    form = TicketAdminForm
    save_as = True
    save_on_top = True
    ordering = ('-created_at',)
    list_display = (
        'event',
        'ticket_holder',
        'listing_status',
        'section',
        'row',
        'seat',
        'price',
        'id',
    )
    readonly_fields = ('id', 'created_at', 'sold_at')
    search_fields = (
        'id',
        'ticket_holder__id',
        'ticket_holder__user__email',
        'ticket_holder__first_name',
        'ticket_holder__last_name',
        'event__name',
    )
    list_filter = (
        'listing_status',
        (
            'created_at',
            DateRangeFilterBuilder(
                title='Created At',
                default_start=datetime.now(),
            ),
        ),
    )
    list_display_links = ('event',)
    autocomplete_fields = ('event', 'ticket_holder')

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'listing_status':
            kwargs['widget'] = Select(choices=((status, status) for status in LISTING_STATUSES))
        return super().formfield_for_dbfield(db_field, request, **kwargs)
