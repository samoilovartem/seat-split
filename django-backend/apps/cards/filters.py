from apps.cards.models import Cards
from config.settings import BOOL_LOOKUPS, CHAR_LOOKUPS, DATE_AND_ID_LOOKUPS
from django_filters import rest_framework as filters


class CardsFilterSet(filters.FilterSet):
    class Meta:
        model = Cards
        fields = {
            'id': DATE_AND_ID_LOOKUPS,
            'account_assigned': CHAR_LOOKUPS,
            'platform': CHAR_LOOKUPS,
            'type': CHAR_LOOKUPS,
            'parent_card': CHAR_LOOKUPS,
            'card_number': CHAR_LOOKUPS,
            'expiration_date': CHAR_LOOKUPS,
            'cvv_number': CHAR_LOOKUPS,
            'created_at': DATE_AND_ID_LOOKUPS,
            'updated_at': DATE_AND_ID_LOOKUPS,
            'created_by': BOOL_LOOKUPS,
            'team': CHAR_LOOKUPS,
            'address': CHAR_LOOKUPS,
            'city': CHAR_LOOKUPS,
            'state': CHAR_LOOKUPS,
            'zip_code': CHAR_LOOKUPS,
            'in_tm': BOOL_LOOKUPS,
            'in_tickets_com': BOOL_LOOKUPS,
            'is_deleted': BOOL_LOOKUPS,
        }
