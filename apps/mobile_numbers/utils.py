from django.db.models import Count

from apps.mobile_numbers.models import MobileNumberTransaction


def mobile_numbers_per_value(filter_name):
    result = (
        MobileNumberTransaction.objects.values(filter_name)
        .order_by(filter_name)
        .annotate(count=Count(filter_name))
    )
    return result
