from rest_framework import status
from rest_framework.status import HTTP_403_FORBIDDEN
from rest_framework.test import APITestCase

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import tag

from apps.cards.models import Cards
from apps.cards.tests.settings import (
    CARD_DETAIL_URL,
    CARDS_FULL_VALID_TEST_DATA,
    CARDS_LIST_URL,
)


@tag('cards', 'unauthorized')
class CardTestUnauthorized(APITestCase):
    """
    Checks if unauthorized user can get access to all CRUD methods of the Cards app.
    Expected: status code 403 Forbidden for all CRUD methods.
    """

    @classmethod
    def setUpTestData(cls):
        call_command(
            'loaddata',
            'apps/common_services/common_test_fixtures/superuser_fixture.json',
        )
        call_command(
            'loaddata',
            'apps/common_services/common_test_fixtures/test_user_fixture.json',
        )
        call_command('loaddata', 'apps/cards/tests/fixtures/cards_fixture.json')

    def setUp(self):
        self.user = get_user_model().objects.get(pk=2)

        self.client.login(
            username=self.user.username,
            password='test_user_password',
        )

    def test_fixtures_loaded(self):
        """
        Checks that the fixtures have been loaded correctly
        """
        self.assertEqual(Cards.objects.count(), 1)
        self.assertEqual(get_user_model().objects.count(), 2)

    def test_can_create_card(self):
        """
        Checks if a new card can be successfully created if user is not authorized
        Expected: False
        """
        response = self.client.post(
            path=CARDS_LIST_URL, data=CARDS_FULL_VALID_TEST_DATA
        )

        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_can_read_cards_list(self):
        """
        Checks if all cards list can be received if user is not authorized
        Expected: False
        """
        response = self.client.get(path=CARDS_LIST_URL)

        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_can_read_card_detail(self):
        """
        Checks if card detail can be received if user is not authorized
        Expected: False
        """
        response = self.client.get(path=CARD_DETAIL_URL)

        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_can_partial_update_card(self):
        """
        Checks if particular card instance can be partially updated if user is not authorized
        Expected: False
        """
        response = self.client.patch(
            path=CARD_DETAIL_URL,
            data={'account_assigned': 'PARTIALLY_UPDATED@test.com'},
        )

        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_can_update_card(self):
        """
        Checks if particular card instance can be updated if user is not authorized
        Expected: False
        """

        response = self.client.put(
            path=CARD_DETAIL_URL, data=CARDS_FULL_VALID_TEST_DATA
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_can_delete_card(self):
        """
        Checks if a card instance can be deleted if user is not authorized
        Expected: False
        """
        response = self.client.delete(path=CARD_DETAIL_URL)

        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)
