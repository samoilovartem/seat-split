from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from apps.stt.api.v1.serializers import EventSerializer
from apps.stt.filters import EventFilterSet
from apps.stt.models import Event


class EventViewSet(ModelViewSet):
    queryset = Event.objects.all().prefetch_related('teamevent_set__team')
    filterset_class = EventFilterSet
    serializer_class = EventSerializer
    permission_classes = (IsAuthenticated,)
    my_tags = ['events']
