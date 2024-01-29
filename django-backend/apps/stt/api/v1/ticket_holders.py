from rest_flex_fields import is_expanded
from rest_framework.mixins import (
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from apps.stt.api.serializers import TicketHolderSerializer
from apps.stt.models import TicketHolder


class TicketHolderViewSet(
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    GenericViewSet,
):
    serializer_class = TicketHolderSerializer
    permission_classes = [IsAuthenticated]
    permit_list_expands = ['ticket_holder_teams']
    my_tags = ['ticket holder']

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            queryset = TicketHolder.objects.all().order_by('id')
        else:
            queryset = TicketHolder.objects.filter(user=user).order_by('id')

        if is_expanded(self.request, 'ticket_holder_teams'):
            queryset = queryset.prefetch_related('ticket_holder_teams')

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
