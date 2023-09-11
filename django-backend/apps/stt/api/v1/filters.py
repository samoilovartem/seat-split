from django_filters.rest_framework import FilterSet

from apps.stt.models import Team
from config.settings import BOOL_LOOKUPS, CHAR_LOOKUPS, DATE_AND_ID_LOOKUPS  # noqa


class TeamFilterSet(FilterSet):
    class Meta:
        model = Team
        fields = {
            'id': DATE_AND_ID_LOOKUPS,
            'league': CHAR_LOOKUPS,
            'city': CHAR_LOOKUPS,
            'name': CHAR_LOOKUPS,
        }
