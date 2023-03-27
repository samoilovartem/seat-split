from apps.cards.models import Cards
from django.db.models import Count


def cards_per_value(filter_name):
    result = (
        Cards.objects.values(filter_name)
        .order_by(filter_name)
        .annotate(count=Count(filter_name))
    )
    return result
