from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from apps.stt.api.serializers import SeasonSerializer
from apps.stt.models import Season


class SeasonViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = Season.objects.all()
    serializer_class = SeasonSerializer
    permission_classes = (IsAuthenticated,)
    filterset_fields = ['league', 'name', 'start_year']
