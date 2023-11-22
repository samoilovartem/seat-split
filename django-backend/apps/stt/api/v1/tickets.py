from rest_flex_fields import is_expanded
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from django.db import IntegrityError

from apps.permissions import IsTicketHolder
from apps.stt.api.serializers import TicketSerializer
from apps.stt.models import Ticket


class TicketViewSet(ModelViewSet):
    serializer_class = TicketSerializer
    filterset_fields = ('ticket_holder', 'event', 'listing_status', 'sold_at', 'season')
    permission_classes = (IsTicketHolder,)
    search_fields = (
        'ticket_holder__first_name',
        'ticket_holder__last_name',
        'event__name',
    )

    my_tags = ['tickets']

    def get_queryset(self):
        user = self.request.user

        if user.is_staff or user.is_superuser:
            queryset = Ticket.objects.all().order_by('-created_at', 'event__date_time')

        else:
            queryset = Ticket.objects.filter(
                ticket_holder=user.ticket_holder_user
            ).order_by('-created_at', 'event__date_time')

        if is_expanded(self.request, 'event'):
            queryset = queryset.select_related('event')
        if is_expanded(self.request, 'ticket_holder'):
            queryset = queryset.select_related('ticket_holder')

        return queryset

    def create_ticket(self, data, many=False):
        serializer = self.get_serializer(data=data, many=many)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        try:
            serializer.save()
        except IntegrityError:
            return Response(
                {'error': 'Duplicate tickets cannot be created.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def create(self, request, *args, **kwargs):
        return self.create_ticket(request.data)

    @action(detail=False, methods=['post'])
    def bulk_create(self, request):
        return self.create_ticket(request.data, many=True)
