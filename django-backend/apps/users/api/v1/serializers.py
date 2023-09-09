from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework.exceptions import ValidationError

from django.contrib.auth.models import Group, Permission

from apps.stt.models import TicketHolder
from apps.users.models import User


class PermissionsSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Permission
        fields = (
            'id',
            'name',
        )


class UserGroupSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Group
        fields = (
            'id',
            'name',
        )


class GroupSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'
        expandable_fields = {
            'permissions': (PermissionsSerializer, {'many': True}),
        }


class TicketHolderUserSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = TicketHolder
        exclude = ('date_created', 'user')


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

        return super().update(instance, validated_data)

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
