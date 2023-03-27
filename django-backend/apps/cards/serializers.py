from apps.cards.models import Cards
from apps.serializers import ConvertNoneToStringSerializerMixin, UserSerializer
from rest_flex_fields import FlexFieldsModelSerializer


class CardsSerializer(ConvertNoneToStringSerializerMixin, FlexFieldsModelSerializer):
    class Meta:
        model = Cards
        fields = '__all__'
        expandable_fields = {
            'created_by': UserSerializer,
        }
