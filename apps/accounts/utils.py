from django.db.models import Count

from apps.accounts.models import Accounts


def accounts_per_value(filter_name):
    result = Accounts.objects.values(filter_name) \
        .order_by(filter_name) \
        .annotate(count=Count(filter_name))
    return result
