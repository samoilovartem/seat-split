from apps.users.models import User
from rest_flex_fields import FlexFieldsModelSerializer


class ShowAllSeatsMixin:
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if '-' in representation['seat']:
            first_seat, last_seat = representation['seat'].split('-')
            representation['seat'] = [str(i) for i in range(int(first_seat), int(last_seat) + 1)]
        else:
            representation['seat'] = [representation['seat']]
        return representation


class ConvertNoneToStringSerializerMixin:
    def get_none_to_str_fields(self):
        meta = getattr(self, 'Meta', None)
        return getattr(meta, 'none_to_str_fields', [])

    def to_representation(self, instance):
        fields = self.get_none_to_str_fields()
        data = super().to_representation(instance)

        if not fields or not isinstance(data, dict):
            return data

        for field in fields:
            if field in data and data[field] is None:
                data[field] = ''
        return data


class UserSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
        )
