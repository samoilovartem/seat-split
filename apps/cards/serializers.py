from drf_queryfields import QueryFieldsMixin
from rest_framework import serializers

from apps.accounts.serializers import ConvertNoneToStringSerializerMixin
from apps.cards.models import Cards


class CardsSerializer(ConvertNoneToStringSerializerMixin, QueryFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = Cards
        fields = '__all__'
        # none_to_str_fields = ('created_by',)
