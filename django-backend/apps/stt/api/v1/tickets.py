from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from django.db import IntegrityError

from apps.common_services.permissions import IsTicketHolder
from apps.stt.api.v1.serializers import TicketSerializer
from apps.stt.models import Ticket


class TicketViewSet(ModelViewSet):
    serializer_class = TicketSerializer
    filterset_fields = ['ticket_holder', 'event', 'listing_status', 'sold_at']
    permission_classes = (IsTicketHolder,)

    my_tags = ['tickets']

    def get_queryset(self):
        user = self.request.user

        if user.is_staff or user.is_superuser:
            return Ticket.objects.all()

        return Ticket.objects.filter(ticket_holder=user.ticket_holder_user)

    @action(detail=False, methods=['post'])
    def bulk_create(self, request):
        serializer = self.get_serializer(data=request.data, many=True)

        if serializer.is_valid():
            try:
                serializer.save()
            except IntegrityError:
                return Response(
                    {'error': 'Duplicate tickets cannot be created.'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            else:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
