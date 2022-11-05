import django_filters
from .models import Accounts


class AccountFilter(django_filters.FilterSet):
    query = django_filters.CharFilter(lookup_expr='icontains',
                                      method='universal_search',
                                      label="Filter")

    class Meta:
        model = Accounts
        fields = ['account_assigned']
