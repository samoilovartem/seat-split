from rest_framework import status
from rest_framework.test import APITestCase
from django.test import tag

from cards.models import Cards
from cards.tests.settings import FULL_USER_DATA, CARDS_LIST_URL, CARDS_FULL_VALID_REAL_DATA, CARD_DETAIL_URL, \
    CARDS_FULL_VALID_TEST_DATA
from users.models import User


@tag('cards', 'unauthorized')
class CardTestUnauthorized(APITestCase):
    """
    Checks if unauthorized user can get access to all CRUD methods of the Cards app.
    Expected: status code 403 Forbidden for all CRUD methods.
    """

    def setUp(self):

        # creating test user, hashing its password and checking if raw password matches hashed one
        self.user = User.objects.create(**FULL_USER_DATA)
        self.user.set_password(FULL_USER_DATA.get('password'))
        self.user.save()
        self.assertTrue(self.user.check_password(FULL_USER_DATA.get('password')))

        # logging in a test user
        self.client.login(username=FULL_USER_DATA.get('username'),
                          password=FULL_USER_DATA.get('password'))

        # creating one real card for next tests
        self.card = Cards.objects.create(**CARDS_FULL_VALID_REAL_DATA)

    def test_can_create_card(self):
        """
        Checks if a new card can be successfully created if user is not authorized
        Expected: False
        """

        response = self.client.post(path=CARDS_LIST_URL, data=CARDS_FULL_VALID_REAL_DATA)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_can_read_cards_list(self):
        """
        Checks if all cards list can be received if user is not authorized
        Expected: False
        """

        response = self.client.get(path=CARDS_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_can_read_card_detail(self):
        """
        Checks if card detail can be received if user is not authorized
        Expected: False
        """

        response = self.client.get(path=CARD_DETAIL_URL)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_can_partial_update_card(self):
        """
        Checks if particular card instance can be partially updated if user is not authorized
        Expected: False
        """

        response = self.client.patch(path=CARD_DETAIL_URL,
                                     data={'account_assigned': 'PARTIALLY_UPDATED@test.com'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_can_update_card(self):
        """
        Checks if particular card instance can be updated if user is not authorized
        Expected: False
        """

        response = self.client.put(path=CARD_DETAIL_URL,
                                   data=CARDS_FULL_VALID_TEST_DATA)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_can_delete_card(self):
        """
        Checks if a card instance can be deleted if user is not authorized
        Expected: False
        """

        response = self.client.delete(path=CARD_DETAIL_URL)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
