from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import LawnsAccounts


class AccountsSerializer(serializers.ModelSerializer):

    class Meta:
        model = LawnsAccounts
        fields = '__all__'
        # validators = [
        #     UniqueTogetherValidator(
        #         queryset=Accounts.objects.all(),
        #         fields=['account_assigned', 'platform']
        #     )
        # ]
