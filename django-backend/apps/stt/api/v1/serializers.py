from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.serializers import ShowAllSeatsMixin
from apps.stt.api.v1.validators import validate_seat_range
from apps.stt.models import (
    Event,
    Purchase,
    Team,
    TeamEvent,
    Ticket,
    TicketHolder,
    TicketHolderTeam,
    User,
)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        if not self.user.is_verified:
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


class TeamSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'


class TicketHolderTeamSerializer(ShowAllSeatsMixin, FlexFieldsModelSerializer):
    class Meta:
        model = TicketHolderTeam
        fields = '__all__'
        expandable_fields = {
            'team': 'apps.stt.api.v1.serializers.TeamSerializer',
            'ticket_holder': 'apps.stt.api.v1.serializers.TicketHolderSerializer',
        }

    @staticmethod
    def validate_seat(value):
        return validate_seat_range(value)


class TicketHolderSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = TicketHolder
        fields = '__all__'
        expandable_fields = {
            'ticket_holder_teams': (TicketHolderTeamSerializer, {'many': True}),
        }


class TicketSerializer(ShowAllSeatsMixin, FlexFieldsModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'

    def create(self, validated_data):
        return Ticket.objects.create(**validated_data)


class TeamEventSerializer(FlexFieldsModelSerializer):
    team = TeamSerializer(read_only=True)

    class Meta:
        model = TeamEvent
        fields = ['team']


class EventSerializer(FlexFieldsModelSerializer):
    teams = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = '__all__'

    @staticmethod
    def get_teams(obj):
        team_events = obj.teamevent_set.all()
        teams = [team_event.team for team_event in team_events]

        return TeamSerializer(teams, many=True).data


class PurchaseSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Purchase
        fields = '__all__'
