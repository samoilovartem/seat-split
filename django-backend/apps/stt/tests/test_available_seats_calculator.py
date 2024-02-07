from uuid import UUID

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase

from apps.stt.models import Event, Team, TicketHolder, TicketHolderTeam
from apps.stt.services.available_seats_calculator import AvailableSeatsCalculator

User = get_user_model()


class TestAvailableSeatsCalculator(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command('loaddata', 'apps/stt/tests/fixtures/test_user.json')
        call_command('loaddata', 'apps/stt/tests/fixtures/test_teams.json')
        call_command('loaddata', 'apps/stt/tests/fixtures/test_ticket_holder_team.json')
        call_command('loaddata', 'apps/stt/tests/fixtures/test_events.json')
        call_command('loaddata', 'apps/stt/tests/fixtures/test_ticket.json')

    def setUp(self):
        self.user = User.objects.first()
        self.ticket_holder = TicketHolder.objects.first()
        self.teams = Team.objects.all()
        self.ticket_holder_team = TicketHolderTeam.objects.first()
        self.available_seats_calculator = AvailableSeatsCalculator(self.ticket_holder, self.teams[0])

    def test_count_initialized_objects(self):
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(TicketHolder.objects.count(), 1)
        self.assertEqual(Team.objects.count(), 2)
        self.assertEqual(TicketHolderTeam.objects.count(), 1)
        self.assertEqual(Event.objects.count(), 3)

    def test_initialization(self):
        self.assertEqual(self.available_seats_calculator.ticket_holder_team, self.ticket_holder_team)
        self.assertEqual(self.available_seats_calculator.ticket_holder, self.ticket_holder)
        self.assertEqual(self.available_seats_calculator.team, self.teams[0])

    def test_get_seats_from_range(self):
        self.assertEqual(self.available_seats_calculator._get_seats_from_range('1-2'), {'1', '2'})
        self.assertEqual(self.available_seats_calculator._get_seats_from_range('1'), {'1'})

    def test_get_future_home_events_for_team(self):
        self.assertEqual(len(self.available_seats_calculator.applicable_events), 3)

    def test_get_tickets_for_events(self):
        self.assertEqual(len(self.available_seats_calculator.tickets), 1)
        self.assertEqual(
            self.available_seats_calculator.tickets[0]['event_id'],
            UUID('250dc054-0934-406a-bd0b-6e821afb5818'),
        )

    #
    def test_get_general_ticket_data(self):
        expected_data = {'section': '1', 'row': '1', 'seat': '1-2'}
        self.assertEqual(self.available_seats_calculator._get_general_ticket_data(), expected_data)

    def test_calculate(self):
        """
        Test the calculate method of the available_seats_calculator.

        This method verifies that the calculate method returns the expected result.
        It checks that the result is a list, with a length of 3 (because 3 objects were loaded from fixtures),
        and that the first element of the result contains the key 'available_seats' with the value ['2'],
        since ticket holder already has one ticket with seat ['1'] that has been already created during fixture loading.
        """
        result = self.available_seats_calculator.calculate()

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0]['available_seats'], ['2'])
