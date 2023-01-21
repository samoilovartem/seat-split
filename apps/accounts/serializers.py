from drf_queryfields import QueryFieldsMixin
from rest_framework import serializers

from apps.accounts.models import Accounts
from apps.serializers import ConvertNoneToStringSerializerMixin


class AccountsSerializer(
    ConvertNoneToStringSerializerMixin, QueryFieldsMixin, serializers.ModelSerializer
):
    class Meta:
        model = Accounts
        exclude = ('updated_at',)
        none_to_str_fields = ('created_by', 'edited_by', 'created_at', 'last_opened')
