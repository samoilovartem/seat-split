from drf_queryfields import QueryFieldsMixin
from rest_framework import serializers

from apps.accounts.models import Accounts


class ConvertNoneToStringSerializerMixin:

    def get_none_to_str_fields(self):
        meta = getattr(self, 'Meta', None)
        return getattr(meta, 'none_to_str_fields', [])

    def to_representation(self, instance):
        fields = self.get_none_to_str_fields()
        data = super().to_representation(instance)

        if not fields or not isinstance(data, dict):
            return data

        for field in fields:
            if field in data and data[field] is None:
                data[field] = 'NA'
        return data


class AccountsSerializer(ConvertNoneToStringSerializerMixin, QueryFieldsMixin, serializers.ModelSerializer):

    class Meta:
        model = Accounts
        # fields = '__all__'
        exclude = ('updated_at',)
        none_to_str_fields = ('created_by', 'edited_by', 'created_at', 'last_opened')
