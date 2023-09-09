from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.stt.models import Team, TicketHolder, User


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        if not self.user.ticket_holder_user.is_verified:
            raise AuthenticationFailed('User is not verified.')

        return data


class UserSerializer(ModelSerializer[User]):
    @staticmethod
    def validate_email(value):
        if User.objects.filter(email=value).exists():
            raise ValidationError()
        return value

    class Meta:
        ref_name = 'UserSerializer'
        model = User
        fields = [
            'id',
        ]


class RegisterSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    phone = serializers.CharField(required=True)
    address = serializers.CharField(required=True)
    is_season_ticket_interest = serializers.BooleanField(required=True)
    is_card_interest = serializers.BooleanField(required=True)

    class Meta:
        model = User
        fields = (
            'email',
            'password',
            'first_name',
            'last_name',
            'phone',
            'address',
            'is_season_ticket_interest',
            'is_card_interest',
        )
        extra_kwargs = {'password': {'write_only': True}}


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'


class TicketHolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketHolder
        fields = '__all__'
