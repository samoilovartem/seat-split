from django_filters import rest_framework as filters
from .models import Accounts

bool_lookups = ['exact']
date_and_id_lookups = ['exact', 'range', 'in']
char_lookups = ['icontains', 'exact', 'startswith']


class AccountsFilterSet(filters.FilterSet):
    class Meta:
        model = Accounts
        fields = {
            'id': date_and_id_lookups,
            'email': char_lookups,
            'first_name': char_lookups,
            'last_name': char_lookups,
            'type': char_lookups,
            'password': char_lookups,
            'recovery_email': char_lookups,
            'email_forwarding': bool_lookups,
            'auto_po_seats_scouts': bool_lookups,
            'errors_failed': char_lookups,
            'tm_created': bool_lookups,
            'tm_password': char_lookups,
            'axs_created': bool_lookups,
            'axs_password': char_lookups,
            'sg_created': bool_lookups,
            'sg_password': char_lookups,
            'tickets_com_created': bool_lookups,
            'eventbrite': bool_lookups,
            'etix': bool_lookups,
            'ticket_web': bool_lookups,
            'big_tickets': bool_lookups,
            'amazon': bool_lookups,
            'secondary_password': char_lookups,
            'seat_scouts_added': bool_lookups,
            'seat_scouts_status': bool_lookups,
            'airfrance': bool_lookups,
            'team': char_lookups,
            'specific_team': char_lookups,
            'forward_to': char_lookups,
            'forward_email_password': char_lookups,
            'disabled': bool_lookups,
            'created_by': bool_lookups,
            'edited_by': bool_lookups,
            'ld_computer_used': char_lookups,
            'created_at': date_and_id_lookups,
            'updated_at': date_and_id_lookups,
            'last_opened': date_and_id_lookups,
            'comments': char_lookups
        }
