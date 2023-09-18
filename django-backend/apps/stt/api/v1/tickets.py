from rest_framework.viewsets import ModelViewSet

from apps.common_services.permissions import IsTicketHolder
from apps.stt.api.v1.serializers import TicketSerializer
from apps.stt.models import Ticket


class TicketViewSet(ModelViewSet):
    serializer_class = TicketSerializer
    filterset_fields = ['ticket_holder', 'event', 'listing_status', 'sold_at']
    permission_classes = (IsTicketHolder,)

    my_tags = ['all tickets']

    def get_queryset(self):
        user = self.request.user

        if user.is_staff or user.is_superuser:
            return Ticket.objects.all()

        return Ticket.objects.filter(ticket_holder=user.ticket_holder_user)
