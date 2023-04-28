from rest_flex_fields import FlexFieldsModelSerializer

from apps.serializers import ConvertNoneToStringSerializerMixin
from apps.venues.models import Venues


class VenuesSerializer(ConvertNoneToStringSerializerMixin, FlexFieldsModelSerializer):
    class Meta:
        model = Venues
        exclude = (
            'updated_at',
            'created_at',
        )
        none_to_str_fields = (
            'latitude',
            'longitude',
        )
