from datetime import datetime
from typing import Any

from apps.stt.api.serializers import SimpleEventSerializer
from apps.stt.models import Event, Ticket, TicketHolderTeam


class AvailableSeatsCalculator:
    def __init__(self, ticket_holder: int, team: str) -> None:
        """
        Initializes the calculator.

        :param ticket_holder: ID of the ticket holder.
        :param team: Team name associated with the ticket holder.
        """
        self.ticket_holder = ticket_holder
        self.team = team
        self.th_team = TicketHolderTeam.objects.get(
            ticket_holder=ticket_holder, team=self.team
        )
        self.general_seats = self._get_seats_from_range(self.th_team.seat)
        self.applicable_events = self._get_future_home_events_for_team()
        self.tickets = self._get_tickets_for_events()

    def _get_seats_from_range(self, seat_range: str) -> set[str]:  # noqa
        """
        Convert a seat range (e.g., '1-5') to a set of seat numbers.

        :param seat_range: Range of seats in string format.
        :return: Set of seat numbers.
        """
        if '-' in seat_range:
            first_seat, last_seat = seat_range.split('-')
            return set(str(i) for i in range(int(first_seat), int(last_seat) + 1))
        else:
            return {seat_range}

    def _get_future_home_events_for_team(self) -> list[Event]:
        """
        Get all future home events for the specified team.

        :return: List of upcoming events.
        """
        return list(
            Event.objects.filter(
                name__endswith=self.team.name, date_time__gte=datetime.now()
            )
        )

    def _get_tickets_for_events(self) -> list[dict[str, Any]]:
        """
        Retrieve tickets associated with the ticket holder for upcoming events.

        :return: List of ticket data.
        """
        return Ticket.objects.filter(
            ticket_holder=self.ticket_holder,
            event__in=self.applicable_events,
            season__in=[event.season for event in self.applicable_events],
        ).values('event_id', 'seat')

    def calculate(self) -> list[dict[str, Any]]:
        """
        Calculate the available seats for the ticket holder for each upcoming event.

        :return: List of available seats data with the associated event.
        """
        tickets_by_event = {}
        for ticket in self.tickets:
            if ticket['event_id'] not in tickets_by_event:
                tickets_by_event[ticket['event_id']] = set()
            tickets_by_event[ticket['event_id']].add(ticket['seat'])

        results = []
        for event in self.applicable_events:
            used_seats = tickets_by_event.get(event.id, set())
            available_seats = self.general_seats - used_seats
            if available_seats:
                results.append(
                    {
                        'event': SimpleEventSerializer(event).data,
                        'available_seats': sorted(list(available_seats), key=int),
                    }
                )

        return results
