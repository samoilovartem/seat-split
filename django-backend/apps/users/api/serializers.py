from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from django.contrib.auth import authenticate, password_validation

from apps.serializers import ShowAllSeatsMixin
from apps.stt.models import Team, TicketHolder, TicketHolderTeam
from apps.users.models import User


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        password_validation.validate_password(value, self.context['request'].user)
        return value

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Old password is not correct')
        return value


class EmailChangeSerializer(serializers.Serializer):
    new_email = serializers.EmailField(required=True)
    current_password = serializers.CharField(required=True, write_only=True)

    def validate_current_password(self, value):
        user = self.context['request'].user
        if not authenticate(username=user.username, password=value):
            raise serializers.ValidationError('Current password is incorrect.')
        return value

    def validate_new_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email is already in use.')
        return value


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class SimpleTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('id', 'name', 'league', 'logo')


class SimpleTicketHolderTeamSerializer(ShowAllSeatsMixin, serializers.ModelSerializer):
    team = SimpleTeamSerializer()

    class Meta:
        model = TicketHolderTeam
        fields = '__all__'


class TicketHolderUserSerializer(FlexFieldsModelSerializer):
    ticket_holder_teams = SimpleTicketHolderTeamSerializer(many=True, read_only=True)

    class Meta:
        model = TicketHolder
        exclude = ('created_at', 'user')


class UserSerializer(FlexFieldsModelSerializer):
    ticket_holder_data = TicketHolderUserSerializer(source='ticket_holder_user')

    class Meta:
        model = User
        exclude = (
            'password',
            'username',
            'user_permissions',
            'groups',
            'date_joined',
            'last_login',
        )
        ref_name = 'UserSerializer'

    def update(self, instance, validated_data):
        ticket_holder_data = validated_data.pop('ticket_holder_user', None)
        self.update_ticket_holder(instance, ticket_holder_data)

        instance = super().update(instance, validated_data)
        instance.refresh_from_db()
        return instance

    def update_ticket_holder(self, user, ticket_holder_data):  # noqa
        if ticket_holder_data is not None:
            ticket_holder = TicketHolder.objects.filter(user=user).first()
            if not ticket_holder:
                raise ValidationError(
                    {'ticket_holder_data': 'No associated Ticket Holder to update.'}
                )
            for key, value in ticket_holder_data.items():
                setattr(ticket_holder, key, value)
            ticket_holder.save()

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if ret['ticket_holder_data'] is None:
            ret['ticket_holder_data'] = {}
        return ret
