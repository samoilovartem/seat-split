from django_filters import rest_framework as filters
from config.settings import CHAR_LOOKUPS, BOOL_LOOKUPS, DATE_AND_ID_LOOKUPS
from accounts.models import Accounts


class AccountsFilterSet(filters.FilterSet):
    class Meta:
        model = Accounts
        fields = {
            'id': DATE_AND_ID_LOOKUPS,
            'email': CHAR_LOOKUPS,
            'first_name': CHAR_LOOKUPS,
            'last_name': CHAR_LOOKUPS,
            'type': CHAR_LOOKUPS,
            'password': CHAR_LOOKUPS,
            'recovery_email': CHAR_LOOKUPS,
            'email_forwarding': BOOL_LOOKUPS,
            'auto_po_seats_scouts': BOOL_LOOKUPS,
            'errors_failed': CHAR_LOOKUPS,
            'tm_created': BOOL_LOOKUPS,
            'tm_password': CHAR_LOOKUPS,
            'axs_created': BOOL_LOOKUPS,
            'axs_password': CHAR_LOOKUPS,
            'sg_created': BOOL_LOOKUPS,
            'sg_password': CHAR_LOOKUPS,
            'tickets_com_created': BOOL_LOOKUPS,
            'eventbrite': BOOL_LOOKUPS,
            'etix': BOOL_LOOKUPS,
            'ticket_web': BOOL_LOOKUPS,
            'big_tickets': BOOL_LOOKUPS,
            'amazon': BOOL_LOOKUPS,
            'secondary_password': CHAR_LOOKUPS,
            'seat_scouts_added': BOOL_LOOKUPS,
            'seat_scouts_status': BOOL_LOOKUPS,
            'airfrance': BOOL_LOOKUPS,
            'team': CHAR_LOOKUPS,
            'specific_team': CHAR_LOOKUPS,
            'forward_to': CHAR_LOOKUPS,
            'forward_email_password': CHAR_LOOKUPS,
            'disabled': BOOL_LOOKUPS,
            'created_by': BOOL_LOOKUPS,
            'edited_by': BOOL_LOOKUPS,
            'ld_computer_used': CHAR_LOOKUPS,
            'created_at': DATE_AND_ID_LOOKUPS,
            'updated_at': DATE_AND_ID_LOOKUPS,
            'last_opened': DATE_AND_ID_LOOKUPS,
            'comments': CHAR_LOOKUPS,
        }
