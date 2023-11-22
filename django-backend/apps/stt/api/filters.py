from django_filters import DateTimeFilter, FilterSet

from apps.stt.models import Ticket


class TicketFilter(FilterSet):
    event__date_time_gte = DateTimeFilter(
        field_name='event__date_time', lookup_expr='gte'
    )

    class Meta:
        model = Ticket
        fields = ('ticket_holder', 'event', 'listing_status', 'sold_at', 'season')
