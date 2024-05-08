from django.db import IntegrityError
from rest_flex_fields import FlexFieldsModelViewSet, is_expanded
from rest_framework import status
from rest_framework.response import Response

from apps.permissions import IsTicketHolder
from apps.stt.api.serializers import TicketHolderTeamSerializer
from apps.stt.models import TicketHolderTeam


class TicketHolderTeamViewSet(
    FlexFieldsModelViewSet,
):
    serializer_class = TicketHolderTeamSerializer
    permission_classes = (IsTicketHolder,)
    permit_list_expands = ['team', 'ticket_holder']
    my_tags = ['ticket holder team']

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            queryset = TicketHolderTeam.objects.all().order_by('id')
        else:
            queryset = TicketHolderTeam.objects.filter(ticket_holder=user.ticket_holder_user).order_by('id')

        if is_expanded(self.request, 'team'):
            queryset = queryset.select_related('team')
        if is_expanded(self.request, 'ticket_holder'):
            queryset = queryset.select_related('ticket_holder')

        return queryset

    def create(self, request, *args, **kwargs):
        try:
            return super(TicketHolderTeamViewSet, self).create(request, *args, **kwargs)
        except IntegrityError:
            content = {
                'detail': 'A TicketHolderTeam with this ticket_holder and team combination already exists.'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
