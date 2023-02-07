from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework import serializers

from apps.accounts.models import Accounts
from apps.mobile_numbers.models import MobileNumberTransaction
from apps.users.models import User


class AccountSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Accounts
        fields = (
            'id',
            'email',
        )


class UserSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
        )


class MobileNumbersSerializer(FlexFieldsModelSerializer):
    email = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=Accounts.objects.all()
    )
    requested_by = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=User.objects.all()
    )

    class Meta:
        model = MobileNumberTransaction
        fields = '__all__'
        expandable_fields = {
            'email': AccountSerializer,
            'requested_by': UserSerializer,
        }
