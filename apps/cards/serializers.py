from rest_flex_fields import FlexFieldsModelSerializer

from apps.cards.models import Cards
from apps.mobile_numbers.serializers import UserSerializer
from apps.serializers import ConvertNoneToStringSerializerMixin


class CardsSerializer(ConvertNoneToStringSerializerMixin, FlexFieldsModelSerializer):
    class Meta:
        model = Cards
        fields = '__all__'
        expandable_fields = {
            'created_by': UserSerializer,
        }
