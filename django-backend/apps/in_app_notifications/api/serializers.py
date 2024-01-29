from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from notifications.models import Notification
from rest_framework.serializers import ModelSerializer

User = get_user_model()


class SimpleUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name']


class ContentTypeSerializer(ModelSerializer):
    class Meta:
        model = ContentType
        fields = ['app_label', 'model']


class NotificationSerializer(ModelSerializer):
    recipient = SimpleUserSerializer()
    actor_content_type = ContentTypeSerializer()

    class Meta:
        model = Notification
        fields = [
            'id',
            'recipient',
            'actor_content_type',
            'verb',
            'level',
            'description',
            'unread',
            'public',
            'deleted',
            'emailed',
            'timestamp',
        ]
