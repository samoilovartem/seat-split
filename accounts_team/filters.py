import django_filters
from .models import LawnsAccounts


class AccountFilter(django_filters.FilterSet):
    query = django_filters.CharFilter(lookup_expr='icontains',
                                      method='universal_search',
                                      label="Filter")

    class Meta:
        model = LawnsAccounts
        fields = ['account_assigned']
