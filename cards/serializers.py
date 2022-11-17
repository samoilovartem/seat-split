from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Cards


class AccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cards
        fields = '__all__'
        # validators = [
        #     UniqueTogetherValidator(
        #         queryset=Accounts.objects.all(),
        #         fields=['account_assigned', 'platform']
        #     )
        # ]
