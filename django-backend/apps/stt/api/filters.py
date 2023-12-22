from django_filters import DateTimeFilter, FilterSet

from apps.stt.models import Event, Purchase, Team, Ticket
from config.components.django_filters import (
    BOOL_OR_EXACT_LOOKUPS,
    CHAR_LOOKUPS,
    DATE_AND_ID_LOOKUPS,
)


class TicketFilter(FilterSet):
    event__date_time_gte = DateTimeFilter(
        field_name='event__date_time', lookup_expr='gte'
    )

    class Meta:
        model = Ticket
        fields = (
            'ticket_holder',
            'event',
            'listing_status',
            'sold_at',
            'event__season__name',
        )


class TeamFilterSet(FilterSet):
    class Meta:
        model = Team
        fields = {
            'id': DATE_AND_ID_LOOKUPS,
            'league': CHAR_LOOKUPS,
            'city': CHAR_LOOKUPS,
            'name': CHAR_LOOKUPS,
        }


class EventFilterSet(FilterSet):
    class Meta:
        model = Event
        fields = {
            'name': CHAR_LOOKUPS,
            'date_time': DATE_AND_ID_LOOKUPS,
        }


class PurchaseFilterSet(FilterSet):
    class Meta:
        model = Purchase
        fields = {
            'ticket': BOOL_OR_EXACT_LOOKUPS,
            'invoice_number': BOOL_OR_EXACT_LOOKUPS,
            'customer': CHAR_LOOKUPS,
            'purchased_at': DATE_AND_ID_LOOKUPS,
            'delivery_status': CHAR_LOOKUPS,
        }
