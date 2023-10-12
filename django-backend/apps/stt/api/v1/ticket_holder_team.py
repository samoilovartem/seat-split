from rest_flex_fields import FlexFieldsModelViewSet, is_expanded

from apps.common_services.permissions import IsTicketHolder
from apps.stt.api.v1.serializers import TicketHolderTeamSerializer
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
            queryset = TicketHolderTeam.objects.filter(
                ticket_holder=user.ticket_holder_user
            ).order_by('id')

        if is_expanded(self.request, 'team'):
            queryset = queryset.select_related('team')
        if is_expanded(self.request, 'ticket_holder'):
            queryset = queryset.select_related('ticket_holder')

        return queryset
