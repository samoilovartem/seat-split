from rest_framework.viewsets import ModelViewSet

from apps.permissions import IsTicketHolder
from apps.stt.api.serializers import PurchaseSerializer
from apps.stt.filters import PurchaseFilterSet
from apps.stt.models import Purchase


class PurchaseViewSet(ModelViewSet):
    serializer_class = PurchaseSerializer
    filterset_class = PurchaseFilterSet
    permission_classes = (IsTicketHolder,)
    my_tags = ['purchases']

    def get_queryset(self):
        user = self.request.user

        if user.is_staff or user.is_superuser:
            return Purchase.objects.all().order_by('id')

        return Purchase.objects.filter(
            ticket__ticket_holder=user.ticket_holder_user
        ).order_by('id')
