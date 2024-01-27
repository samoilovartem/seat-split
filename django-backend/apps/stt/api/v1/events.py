from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.stt.api.filters import EventFilterSet
from apps.stt.api.serializers import AvailableSeatsSerializer, EventSerializer
from apps.stt.models import Event, TicketHolderTeam
from apps.stt.services.available_seats_calculator import AvailableSeatsCalculator


class EventViewSet(ModelViewSet):
    queryset = Event.objects.all().prefetch_related('teamevent_set__team').order_by('id')
    search_fields = ('name', 'date_time')
    filterset_class = EventFilterSet
    serializer_class = EventSerializer
    permission_classes = (IsAuthenticated,)
    my_tags = ['events']

    @swagger_auto_schema(request_body=AvailableSeatsSerializer)
    @action(detail=False, methods=['POST'])
    def available_seats(self, request):
        """
        Calculate and return available seats for a given ticket holder and team.

        This endpoint accepts a ticket holder and a team as input and computes
        the available seats for upcoming events of the team for the ticket holder.
        It uses the AvailableSeatsCalculator to determine the seats that have
        not been occupied by the ticket holder for each event.

        :param request: The request object containing ticket holder and team data.
        :return: A list of available seats for each applicable event for the ticket holder.
        """
        serializer = AvailableSeatsSerializer(data=request.data)
        if serializer.is_valid():
            ticket_holder = serializer.validated_data['ticket_holder']
            team = serializer.validated_data['team']

            if not TicketHolderTeam.objects.filter(ticket_holder=ticket_holder, team=team).exists():
                return Response(
                    {'detail': 'The provided team does not belong to the ticket holder.'},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            context = {'request': request}

            calculator = AvailableSeatsCalculator(ticket_holder, team)
            return Response(calculator.calculate(context=context))

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
