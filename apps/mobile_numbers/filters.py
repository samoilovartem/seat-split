from django_filters import rest_framework as filters

from apps.mobile_numbers.models import MobileNumberTransaction
from config.settings import BOOL_LOOKUPS, CHAR_LOOKUPS, DATE_AND_ID_LOOKUPS


class MobileNumbersFilterSet(filters.FilterSet):
    class Meta:
        model = MobileNumberTransaction
        fields = {
            'id': CHAR_LOOKUPS,
            'email': BOOL_LOOKUPS,
            'phone': CHAR_LOOKUPS,
            'service_name': CHAR_LOOKUPS,
            'order_id': CHAR_LOOKUPS,
            'service_id': CHAR_LOOKUPS,
            'account_created': BOOL_LOOKUPS,
        }
