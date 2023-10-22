from drf_yasg.utils import swagger_auto_schema
from rest_flex_fields import FlexFieldsModelViewSet, is_expanded
from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.common_services.permissions import IsTicketHolder
from apps.stt.api.v1.serializers import (
    SimpleEventSerializer,
    TicketHolderTeamSerializer,
)
from apps.stt.models import Event, Team, Ticket, TicketHolder, TicketHolderTeam


class AvailableSeatsSerializer(serializers.Serializer):
    ticket_holder = serializers.PrimaryKeyRelatedField(
        queryset=TicketHolder.objects.all()
    )
    team = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all())


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

    @swagger_auto_schema(request_body=AvailableSeatsSerializer)
    @action(detail=False, methods=['POST'])
    def available_seats(self, request):
        serializer = AvailableSeatsSerializer(data=request.data)
        if serializer.is_valid():
            ticket_holder = serializer.validated_data['ticket_holder']
            team = serializer.validated_data['team']

            if not TicketHolderTeam.objects.filter(
                ticket_holder=ticket_holder, team=team
            ).exists():
                return Response(
                    {
                        'detail': 'The provided team does not belong to the ticket holder.'
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            try:
                th_team = TicketHolderTeam.objects.get(ticket_holder=ticket_holder)
            except TicketHolderTeam.DoesNotExist:
                return Response(
                    {'detail': 'TicketHolderTeam not found.'},
                    status=status.HTTP_404_NOT_FOUND,
                )

            general_seats = set(self.get_seats_from_range(th_team.seat))

            applicable_events = list(Event.objects.filter(name__endswith=team.name))

            # tickets = Ticket.objects.filter(
            #     ticket_holder=ticket_holder,
            #     event__in=applicable_events
            # ).values('event_id', 'seat')

            tickets = Ticket.objects.filter(
                ticket_holder=ticket_holder,
                event__in=applicable_events,
                # listing_status="sold",
                sold_at__isnull=True,
            ).values('event_id', 'seat')

            tickets_by_event = {}
            for ticket in tickets:
                if ticket['event_id'] not in tickets_by_event:
                    tickets_by_event[ticket['event_id']] = set()
                tickets_by_event[ticket['event_id']].add(ticket['seat'])

            results = []

            for event in applicable_events:
                used_seats = tickets_by_event.get(event.id, set())
                available_seats = general_seats - used_seats
                results.append(
                    {
                        'event': SimpleEventSerializer(event).data,
                        'available_seats': list(available_seats),
                    }
                )

            return Response(results)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_seats_from_range(self, seat_range):
        if '-' in seat_range:
            first_seat, last_seat = seat_range.split('-')
            return [str(i) for i in range(int(first_seat), int(last_seat) + 1)]
        else:
            return [seat_range]
