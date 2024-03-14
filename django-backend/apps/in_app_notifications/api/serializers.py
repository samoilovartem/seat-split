from notifications.models import Notification
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType

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
    recipient = SimpleUserSerializer(read_only=True)
    actor_content_type = ContentTypeSerializer(read_only=True)

    recipient_email = serializers.EmailField(write_only=True, required=True)
    actor_object_id = serializers.UUIDField(write_only=True, required=True)
    actor_content_type_app_label = serializers.CharField(write_only=True, required=True)
    actor_content_type_model = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Notification
        fields = [
            'id',
            'recipient',
            'actor_content_type',
            'actor_object_id',
            'verb',
            'level',
            'description',
            'unread',
            'public',
            'deleted',
            'emailed',
            'timestamp',
            'recipient_email',
            'actor_content_type_app_label',
            'actor_content_type_model',
        ]

    def create(self, validated_data):
        recipient_email = validated_data.pop('recipient_email', None)
        app_label = validated_data.pop('actor_content_type_app_label', None)
        model = validated_data.pop('actor_content_type_model', None)

        if recipient_email:
            recipient = User.objects.get(email=recipient_email)
            validated_data['recipient'] = recipient
        if app_label and model:
            actor_content_type = ContentType.objects.get(app_label=app_label, model=model)
            validated_data['actor_content_type'] = actor_content_type

        return super().create(validated_data)
