from rest_framework import status
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.test import APITestCase

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.db.models import BooleanField, CharField, DateField, EmailField
from django.test import tag

from apps.cards.models import Cards
from apps.cards.tests.settings import (
    CARD_DETAIL_URL,
    CARDS_FULL_VALID_TEST_DATA,
    CARDS_LIST_URL,
)


@tag('cards', 'authenticated')
class CardsTest(APITestCase):
    """
    Card parent test class that inherits from APITestCase and has 'setUp' method
    that children classes can use without repetition
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
        self.superuser = get_user_model().objects.get(pk=1)

        self.client.login(
            username=self.superuser.username,
            password='super_user_password',
        )

        self.card = Cards.objects.first()

    def test_fixtures_loaded(self):
        """
        Checks that the fixtures have been loaded correctly
        """
        self.assertEqual(Cards.objects.count(), 1)
        self.assertEqual(get_user_model().objects.count(), 2)


class CreateCardTest(CardsTest):
    """
    Children class that contains all necessary methods to test if a card can be CREATED
    """

    def setUp(self):
        super().setUp()

    def test_can_view_card_details(self):
        """
        Checks if particular card detail can be received by a user who has rights to see it
        Expected: True
        """
        response = self.client.get(path=CARD_DETAIL_URL)

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(
            self.card.card_number,
            CARDS_FULL_VALID_TEST_DATA.get('card_number'),
        )

    def test_can_create_card(self):
        """
        Checks if a new card can be successfully created
        Expected: True
        """

        card_data = CARDS_FULL_VALID_TEST_DATA.copy()
        card_data.update({'account_assigned': 'john.doe2@example.com'})

        response = self.client.post(path=CARDS_LIST_URL, data=card_data)

        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(Cards.objects.count(), 2)
        self.assertEqual(
            response.data.get('account_assigned'),
            card_data.get('account_assigned'),
        )

    def test_required_char_fields(self):
        """
        Checks if a new card can be successfully created when required char fields are empty
        Expected: False
        """
        required_fields = [
            field.name
            for field in Cards._meta.fields
            if isinstance(field, (CharField, EmailField)) and field.blank is False
        ]

        for field in required_fields:
            with self.subTest(field=field):
                invalid_data = CARDS_FULL_VALID_TEST_DATA.copy()
                invalid_data.update({field: ''})

                response = self.client.post(path=CARDS_LIST_URL, data=invalid_data)

                self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
                self.assertIn(
                    member='This field may not be blank.',
                    container=response.data.get(field),
                )

    def test_required_boolean_fields(self):
        """
        Checks if a new card can be successfully created when boolean fields have incorrect values
        Expected: False
        """
        boolean_fields = [
            field.name
            for field in Cards._meta.fields
            if isinstance(field, BooleanField)
        ]

        for field in boolean_fields:
            with self.subTest(field=field):
                invalid_data = CARDS_FULL_VALID_TEST_DATA.copy()
                invalid_data.update({field: 'test'})

                response = self.client.post(path=CARDS_LIST_URL, data=invalid_data)

                self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
                self.assertIn(
                    member='Must be a valid boolean.',
                    container=response.data.get(field),
                )

    def test_required_date_fields(self):
        """
        Checks if a new card can be successfully created when required date fields have incorrect values
        Expected: False
        """
        required_date_fields = [
            field.name
            for field in Cards._meta.fields
            if isinstance(field, DateField) and field.blank is False
        ]

        for field in required_date_fields:
            with self.subTest(field=field):
                invalid_data = CARDS_FULL_VALID_TEST_DATA.copy()
                invalid_data.update({field: 'invalid format'})

                response = self.client.post(path=CARDS_LIST_URL, data=invalid_data)

                self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
                self.assertIn(
                    member='Date has wrong format. Use one of these formats instead: YYYY-MM-DD.',
                    container=response.data.get(field),
                )


class ReadCardTest(CardsTest):
    """
    Children class that contains all necessary methods to test
    if cards list and card instance can be READ
    """

    def setUp(self):
        super().setUp()

    def test_can_read_cards_list(self):
        """
        Checks if all cards list can be received by a user who has rights to see them
        Expected: True
        """
        response = self.client.get(path=CARDS_LIST_URL)

        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_can_read_card_detail(self):
        """
        Checks if particular card detail can be received by a user who has rights to see it
        Expected: True
        """
        response = self.client.get(path=CARD_DETAIL_URL)

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(
            Cards.objects.get(pk=1).account_assigned,
            CARDS_FULL_VALID_TEST_DATA.get('account_assigned'),
        )


class UpdateCardTest(CardsTest):
    """
    Children class that contains all necessary methods to test
    if card can be UPDATED and PARTIALLY UPDATED
    """

    def setUp(self):
        super().setUp()

    def test_can_partial_update_card(self):
        """
        Checks if particular card instance can be partially updated
        Expected: True
        """
        data_to_update = {'account_assigned': 'PARTIALLY_UPDATED@test.com'}

        response = self.client.patch(path=CARD_DETAIL_URL, data=data_to_update)

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(
            Cards.objects.get(pk=1).account_assigned,
            data_to_update.get('account_assigned'),
        )

    def test_can_update_card(self):
        """
        Checks if particular card instance can be updated
        Expected: True
        """
        data_to_update = CARDS_FULL_VALID_TEST_DATA
        data_to_update.update({'account_assigned': 'UPDATED@test.com'})

        response = self.client.put(path=CARD_DETAIL_URL, data=data_to_update)

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(
            Cards.objects.get(pk=1).account_assigned,
            data_to_update.get('account_assigned'),
        )


class DeleteCardTest(CardsTest):
    """
    Children class that contains all necessary methods to test
    if card can be DELETED
    """

    def setUp(self):
        super().setUp()

    def test_can_delete_card(self):
        """
        Checks if a card can be deleted
        Expected: True
        """
        response = self.client.delete(path=CARD_DETAIL_URL)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Cards.objects.all().count(), 0)
