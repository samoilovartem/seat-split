from drf_yasg.utils import no_body, swagger_auto_schema
from notifications.models import Notification
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.in_app_notifications.api.serializers import NotificationSerializer


class NotificationViewSet(ListModelMixin, GenericViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    my_tags = ['notifications']

    def get_queryset(self):
        return Notification.objects.filter(recipient_id=self.request.user.id)

    @swagger_auto_schema(request_body=no_body, responses={status.HTTP_200_OK: 'OK'})
    @action(detail=False, methods=['POST'], name='Mark all as read')
    def mark_all_as_read(self, request):
        self.get_queryset().filter(unread=True).update(unread=False)
        return Response({'code': 'OK'}, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=no_body, responses={status.HTTP_200_OK: 'OK'})
    @action(detail=True, methods=['POST'], name='Mark as read')
    def mark_as_read(self, request, pk=None):
        notification = self.get_object()
        notification.unread = False
        notification.save()
        return Response({'code': 'OK'}, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=no_body, responses={status.HTTP_200_OK: 'OK'})
    @action(detail=True, methods=['POST'], name='Mark as unread')
    def mark_as_unread(self, request, pk=None):
        notification = self.get_object()
        notification.unread = True
        notification.save()
        return Response({'code': 'OK'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['DELETE'], name='Delete notification')
    def delete_notification(self, request, pk=None):
        notification = self.get_object()
        notification.delete()
        return Response({'code': 'OK'}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['GET'], name='Unread count')
    def unread_count(self, request):
        count = self.get_queryset().filter(unread=True).count()
        return Response({'unread_count': count})

    @action(detail=False, methods=['GET'], name='All count')
    def all_count(self, request):
        count = self.get_queryset().count()
        return Response({'all_count': count})
