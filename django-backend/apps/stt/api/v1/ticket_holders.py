from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import (
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.stt.api.v1.serializers import (
    TicketHolderSerializer,
    TicketHolderTeamSerializer,
)
from apps.stt.models import TicketHolder


class TicketHolderViewSet(
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    GenericViewSet,
):
    queryset = TicketHolder.objects.all()
    serializer_class = TicketHolderSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @swagger_auto_schema(request_body=TicketHolderTeamSerializer)
    @action(detail=True, methods=['POST'])
    def add_ticket_holder_team(self, request, pk=None):
        ticket_holder = self.get_object()
        team_serializer = TicketHolderTeamSerializer(data=request.data)

        if team_serializer.is_valid():
            team_serializer.save(ticket_holder=ticket_holder)
            return Response(team_serializer.data)
        return Response(team_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
