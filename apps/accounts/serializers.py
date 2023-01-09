from drf_queryfields import QueryFieldsMixin
from rest_framework import serializers

from apps.accounts.models import Accounts


class AccountsSerializer(QueryFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = Accounts
        # fields = '__all__'
        exclude = ('updated_at',)
