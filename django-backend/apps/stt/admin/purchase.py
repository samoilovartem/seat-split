from datetime import datetime

from rangefilter.filters import DateRangeFilterBuilder

from django.contrib import admin
from django.forms import Select

from apps.stt.models import Purchase
from config.components.business_related import DELIVERY_STATUSES, MARKETPLACES


@admin.register(Purchase)
class PurchaseAdminConfig(admin.ModelAdmin):
    model = Purchase
    save_as = True
    save_on_top = True
    ordering = ('-created_at',)
    list_display = (
        'ticket',
        'invoice_number',
        'customer',
        'delivery_status',
        'id',
    )
    search_fields = (
        'id',
        'ticket__id',
        'ticket__ticket_holder__first_name',
        'ticket__ticket_holder__last_name',
        'ticket__event__name',
    )
    readonly_fields = ('id',)
    list_filter = (
        'customer',
        'delivery_status',
        (
            'created_at',
            DateRangeFilterBuilder(
                title='Created At',
                default_start=datetime.now(),
            ),
        ),
    )
    list_display_links = ('ticket',)
    autocomplete_fields = ('ticket',)

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'delivery_status':
            kwargs['widget'] = Select(choices=((status, status) for status in DELIVERY_STATUSES))
        if db_field.name == 'customer':
            kwargs['widget'] = Select(choices=((customer, customer) for customer in MARKETPLACES))
        return super().formfield_for_dbfield(db_field, request, **kwargs)
