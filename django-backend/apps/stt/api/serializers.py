from pytz import timezone
from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from django.contrib.auth import get_user_model
from django.utils.timezone import localtime

from apps.serializers import ShowAllSeatsMixin
from apps.stt.api.validators import validate_seat_range
from apps.stt.models import (
    Event,
    Purchase,
    Season,
    Team,
    TeamEvent,
    Ticket,
    TicketHolder,
    TicketHolderTeam,
    Venue,
)
from apps.stt.utils import calculate_price_with_expenses

User = get_user_model()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        if not self.user.is_verified:
            raise AuthenticationFailed('User is not verified.')

        return data


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


class SimpleTicketHolderSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = TicketHolder
        fields = '__all__'


class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = (
            'id',
            'name',
            'address',
            'city',
            'state',
            'postal_code',
            'country',
            'timezone',
            'phone',
        )


class SimpleEventSerializer(FlexFieldsModelSerializer):
    venue = VenueSerializer(read_only=True)
    season = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = '__all__'

    def get_season(self, obj):
        return obj.season.name if obj.season else None

    def to_representation(self, instance):
        """
        Convert `date_time` to the timezone specified in the TicketHolder's profile
        before serializing the object.
        """
        representation = super().to_representation(instance)
        request = self.context.get('request')

        if request and hasattr(request.user, 'ticket_holder_user'):
            user_timezone = request.user.ticket_holder_user.timezone
            tz = timezone(user_timezone)
            date_time = instance.date_time.astimezone(tz)
        else:
            date_time = localtime(instance.date_time)

        representation['name'] = instance.get_formatted_name()
        representation['date_time'] = date_time.strftime('%Y-%m-%d %H:%M')
        return representation


class TicketSerializer(ShowAllSeatsMixin, FlexFieldsModelSerializer):
    season = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = '__all__'
        expandable_fields = {
            'ticket_holder': SimpleTicketHolderSerializer,
            'event': SimpleEventSerializer,
        }

    def get_season(self, obj):
        return obj.event.season.name if obj.event else None

    def create(self, validated_data):
        return Ticket.objects.create(**validated_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['price'] = calculate_price_with_expenses(instance.price)
        return representation


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

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['name'] = instance.get_formatted_name()
        return representation


class PurchaseSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Purchase
        fields = '__all__'


class AvailableSeatsSerializer(serializers.Serializer):
    ticket_holder = serializers.PrimaryKeyRelatedField(queryset=TicketHolder.objects.all(), required=False)
    team = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all())


class SeasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Season
        fields = '__all__'
