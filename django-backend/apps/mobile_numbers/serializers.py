from apps.accounts.models import Accounts
from apps.mobile_numbers.models import MobileNumberTransaction
from apps.serializers import UserSerializer
from rest_flex_fields import FlexFieldsModelSerializer


class AccountSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Accounts
        fields = (
            'id',
            'email',
        )


class MobileNumbersSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = MobileNumberTransaction
        fields = '__all__'
        expandable_fields = {
            'email': AccountSerializer,
            'requested_by': UserSerializer,
        }
