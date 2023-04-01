from django.test import tag
from rest_framework import status
from rest_framework.test import APITestCase

from apps.cards.models import Cards
from apps.cards.tests.settings import (
    CARD_DETAIL_URL,
    CARDS_FULL_VALID_REAL_DATA,
    CARDS_FULL_VALID_TEST_DATA,
    CARDS_FULL_VALID_TEST_DATA_COPY,
    CARDS_LIST_URL,
    REQUIRED_SUPERUSER_DATA,
)
from apps.users.models import User


@tag('cards', 'authenticated')
class CardsTest(APITestCase):
    """
    Card parent test class that inherits from APITestCase and has 'setUp' method
    that children classes can use without repetition
    """

    def setUp(self):
        # creating test superuser, hashing its password and checking if raw password matches hashed one
        self.superuser = User.objects.create_superuser(**REQUIRED_SUPERUSER_DATA)
        self.superuser.set_password(REQUIRED_SUPERUSER_DATA.get("password"))
        self.superuser.save()
        self.assertTrue(
            self.superuser.check_password(REQUIRED_SUPERUSER_DATA.get('password'))
        )

        # logging in
        self.client.login(
            username=REQUIRED_SUPERUSER_DATA.get('username'),
            password=REQUIRED_SUPERUSER_DATA.get('password'),
        )

        # creating one real card for next tests
        self.card = Cards.objects.create(**CARDS_FULL_VALID_REAL_DATA)


class CreateCardTest(CardsTest):
    """
    Children class that contains all necessary methods to test if a card can be CREATED
    """

    def setUp(self):
        super().setUp()

    def test_can_create_card(self):
        """
        Checks if a new card can be successfully created
        Expected: True
        """

        response = self.client.post(
            path=CARDS_LIST_URL, data=CARDS_FULL_VALID_TEST_DATA
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Cards.objects.count(), 2)
        self.assertEqual(
            response.data.get('account_assigned'),
            CARDS_FULL_VALID_TEST_DATA.get('account_assigned'),
        )

    def test_can_create_card_with_existing_email_and_platform(self):
        """
        Checks if a new card can be successfully created
        if unique together fields (account_assigned and platform) already exist in DB
        Expected: False
        """

        response = self.client.post(
            path=CARDS_LIST_URL, data=CARDS_FULL_VALID_REAL_DATA
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            member='The fields account_assigned, platform must make a unique set.',
            container=response.data.get('non_field_errors'),
        )

    def test_can_create_card_with_incorrect_email(self):
        """
        Checks if a new card can be successfully created with an incorrect email
        Expected: False
        """

        CARDS_FULL_VALID_TEST_DATA.update({'account_assigned': 'test'})
        response = self.client.post(
            path=CARDS_LIST_URL, data=CARDS_FULL_VALID_TEST_DATA
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            member='Enter a valid email address.',
            container=response.data.get('account_assigned'),
        )

    def test_can_create_card_with_empty_email(self):
        """
        Checks if a new card can be successfully created with an empty email
        Expected: False
        """

        CARDS_FULL_VALID_TEST_DATA.update({'account_assigned': ''})
        response = self.client.post(
            path=CARDS_LIST_URL, data=CARDS_FULL_VALID_TEST_DATA
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            member='This field may not be blank.',
            container=response.data.get('account_assigned'),
        )

    def test_can_create_card_with_empty_platform(self):
        """
        Checks if a new card can be successfully created with an empty platform
        Expected: False
        """

        CARDS_FULL_VALID_TEST_DATA.update({'platform': ''})
        response = self.client.post(
            path=CARDS_LIST_URL, data=CARDS_FULL_VALID_TEST_DATA
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            member='This field may not be blank.',
            container=response.data.get('platform'),
        )

    def test_can_create_card_with_empty_type(self):
        """
        Checks if a new card can be successfully created with an empty type
        Expected: False
        """

        CARDS_FULL_VALID_TEST_DATA.update({'type': ''})
        response = self.client.post(
            path=CARDS_LIST_URL, data=CARDS_FULL_VALID_TEST_DATA
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            member='This field may not be blank.', container=response.data.get('type')
        )

    def test_can_create_card_with_empty_parent_card(self):
        """
        Checks if a new card can be successfully created with an empty parent_card
        Expected: False
        """

        CARDS_FULL_VALID_TEST_DATA.update({'parent_card': ''})
        response = self.client.post(
            path=CARDS_LIST_URL, data=CARDS_FULL_VALID_TEST_DATA
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            member='This field may not be blank.',
            container=response.data.get('parent_card'),
        )

    def test_can_create_card_with_incorrect_card_number(self):
        """
        Checks if a new card can be successfully created with an incorrect card_number
        Expected: False
        """

        CARDS_FULL_VALID_TEST_DATA.update({'card_number': '12345678876543'})
        response = self.client.post(
            path=CARDS_LIST_URL, data=CARDS_FULL_VALID_TEST_DATA
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            member='Card number must have 15 or 16 digits!',
            container=response.data.get('card_number'),
        )

        CARDS_FULL_VALID_TEST_DATA.update({'card_number': '12345678876543210'})
        response = self.client.post(
            path=CARDS_LIST_URL, data=CARDS_FULL_VALID_TEST_DATA
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            member='Ensure this field has no more than 16 characters.',
            container=response.data.get('card_number'),
        )

    def test_can_create_card_with_empty_card_number(self):
        """
        Checks if a new card can be successfully created with an empty card_number
        Expected: False
        """

        CARDS_FULL_VALID_TEST_DATA.update({'card_number': ''})
        response = self.client.post(
            path=CARDS_LIST_URL, data=CARDS_FULL_VALID_TEST_DATA
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            member='This field may not be blank.',
            container=response.data.get('card_number'),
        )

    def test_can_create_card_with_incorrect_expiration_date(self):
        """
        Checks if a new card can be successfully created with an incorrect expiration_date
        Expected: False
        """

        CARDS_FULL_VALID_TEST_DATA.update({'expiration_date': '1/23'})
        response = self.client.post(
            path=CARDS_LIST_URL, data=CARDS_FULL_VALID_TEST_DATA
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            member='Expiration date must be in format MM/YY',
            container=response.data.get('expiration_date'),
        )

        CARDS_FULL_VALID_TEST_DATA.update({'expiration_date': '10/230'})
        response = self.client.post(
            path=CARDS_LIST_URL, data=CARDS_FULL_VALID_TEST_DATA
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            member='Ensure this field has no more than 5 characters.',
            container=response.data.get('expiration_date'),
        )

    def test_can_create_card_with_empty_expiration_date(self):
        """
        Checks if a new card can be successfully created with an empty expiration_date
        Expected: False
        """

        CARDS_FULL_VALID_TEST_DATA.update({'expiration_date': ''})
        response = self.client.post(
            path=CARDS_LIST_URL, data=CARDS_FULL_VALID_TEST_DATA
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            member='This field may not be blank.',
            container=response.data.get('expiration_date'),
        )

    def test_can_create_card_with_incorrect_cvv_number(self):
        """
        Checks if a new card can be successfully created with an incorrect cvv_number
        Expected: False
        """

        CARDS_FULL_VALID_TEST_DATA.update({'cvv_number': '12'})
        response = self.client.post(
            path=CARDS_LIST_URL, data=CARDS_FULL_VALID_TEST_DATA
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            member='CVV number must have 3 or 4 digits!',
            container=response.data.get('cvv_number'),
        )

        CARDS_FULL_VALID_TEST_DATA.update({'cvv_number': '12000'})
        response = self.client.post(
            path=CARDS_LIST_URL, data=CARDS_FULL_VALID_TEST_DATA
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            member='Ensure this field has no more than 4 characters.',
            container=response.data.get('cvv_number'),
        )

    def test_can_create_card_with_empty_cvv_number(self):
        """
        Checks if a new card can be successfully created with an empty cvv_number
        Expected: False
        """

        CARDS_FULL_VALID_TEST_DATA.update({'cvv_number': ''})
        response = self.client.post(
            path=CARDS_LIST_URL, data=CARDS_FULL_VALID_TEST_DATA
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            member='This field may not be blank.',
            container=response.data.get('cvv_number'),
        )

    def test_can_create_card_with_empty_team(self):
        """
        Checks if a new card can be successfully created with an empty team
        Expected: False
        """

        CARDS_FULL_VALID_TEST_DATA.update({'team': ''})
        response = self.client.post(
            path=CARDS_LIST_URL, data=CARDS_FULL_VALID_TEST_DATA
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            member='This field may not be blank.', container=response.data.get('team')
        )

    def test_can_create_card_with_empty_specific_team(self):
        """
        Checks if a new card can be successfully created with an empty specific_team
        Expected: False
        """

        CARDS_FULL_VALID_TEST_DATA.update({'specific_team': ''})
        response = self.client.post(
            path=CARDS_LIST_URL, data=CARDS_FULL_VALID_TEST_DATA
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            member='This field may not be blank.',
            container=response.data.get('specific_team'),
        )

    def test_can_create_card_with_empty_address(self):
        """
        Checks if a new card can be successfully created with an empty address
        Expected: False
        """

        CARDS_FULL_VALID_TEST_DATA.update({'address': ''})
        response = self.client.post(
            path=CARDS_LIST_URL, data=CARDS_FULL_VALID_TEST_DATA
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            member='This field may not be blank.',
            container=response.data.get('address'),
        )

    def test_can_create_card_with_empty_city(self):
        """
        Checks if a new card can be successfully created with an empty city
        Expected: False
        """

        CARDS_FULL_VALID_TEST_DATA.update({"city": ""})
        response = self.client.post(
            path=CARDS_LIST_URL, data=CARDS_FULL_VALID_TEST_DATA
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            member='This field may not be blank.', container=response.data.get('city')
        )

    def test_can_create_card_with_incorrect_state(self):
        """
        Checks if a new card can be successfully created with an incorrect state
        Expected: False
        """

        CARDS_FULL_VALID_TEST_DATA.update({'state': 'f'})
        response = self.client.post(
            path=CARDS_LIST_URL, data=CARDS_FULL_VALID_TEST_DATA
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            member='State must have 2 letters only and be in the following format: XX!',
            container=response.data.get('state'),
        )

        CARDS_FULL_VALID_TEST_DATA.update({'state': 'gggg'})
        response = self.client.post(
            path=CARDS_LIST_URL, data=CARDS_FULL_VALID_TEST_DATA
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            member='Ensure this field has no more than 2 characters.',
            container=response.data.get('state'),
        )

    def test_can_create_card_with_empty_state(self):
        """
        Checks if a new card can be successfully created with an empty state
        Expected: False
        """

        CARDS_FULL_VALID_TEST_DATA.update({'state': ''})
        response = self.client.post(
            path=CARDS_LIST_URL, data=CARDS_FULL_VALID_TEST_DATA
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            member='This field may not be blank.', container=response.data.get('state')
        )

    def test_can_create_card_with_incorrect_zip_code(self):
        """
        Checks if a new card can be successfully created with an incorrect zip_code
        Expected: False
        """

        CARDS_FULL_VALID_TEST_DATA.update({'zip_code': '3323'})
        response = self.client.post(
            path=CARDS_LIST_URL, data=CARDS_FULL_VALID_TEST_DATA
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            member='ZIP code must have 5 digits!',
            container=response.data.get('zip_code'),
        )

        CARDS_FULL_VALID_TEST_DATA.update({'zip_code': 'fssdfd'})
        response = self.client.post(
            path=CARDS_LIST_URL, data=CARDS_FULL_VALID_TEST_DATA
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            member='Ensure this field has no more than 5 characters.',
            container=response.data.get('zip_code'),
        )

    def test_can_create_card_with_empty_zip_code(self):
        """
        Checks if a new card can be successfully created with an empty zip_code
        Expected: False
        """

        CARDS_FULL_VALID_TEST_DATA.update({'zip_code': ''})
        response = self.client.post(
            path=CARDS_LIST_URL, data=CARDS_FULL_VALID_TEST_DATA
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            member='This field may not be blank.',
            container=response.data.get('zip_code'),
        )

    def test_can_create_card_with_incorrect_in_tm(self):
        """
        Checks if a new card can be successfully created with an incorrect in_tm
        Expected: False
        """

        CARDS_FULL_VALID_TEST_DATA.update({'in_tm': 'test'})
        response = self.client.post(
            path=CARDS_LIST_URL, data=CARDS_FULL_VALID_TEST_DATA
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            member='Must be a valid boolean.', container=response.data.get('in_tm')
        )

    def test_can_create_card_with_incorrect_in_tickets_com(self):
        """
        Checks if a new card can be successfully created with an incorrect in_tickets_com
        Expected: False
        """

        CARDS_FULL_VALID_TEST_DATA.update({'in_tickets_com': 'test'})
        response = self.client.post(
            path=CARDS_LIST_URL, data=CARDS_FULL_VALID_TEST_DATA
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            member='Must be a valid boolean.',
            container=response.data.get('in_tickets_com'),
        )

    def test_can_create_card_with_incorrect_is_deleted(self):
        """
        Checks if a new card can be successfully created with an incorrect is_deleted
        Expected: False
        """

        CARDS_FULL_VALID_TEST_DATA.update({'is_deleted': 'test'})
        response = self.client.post(
            path=CARDS_LIST_URL, data=CARDS_FULL_VALID_TEST_DATA
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            member='Must be a valid boolean.', container=response.data.get('is_deleted')
        )

    def test_can_create_card_with_incorrect_created_by(self):
        """
        Checks if a new card can be successfully created with an incorrect created_by
        Expected: False
        """

        CARDS_FULL_VALID_TEST_DATA.update({'created_by': 'test'})
        response = self.client.post(
            path=CARDS_LIST_URL, data=CARDS_FULL_VALID_TEST_DATA
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            member='Incorrect type. Expected pk value, received str.',
            container=response.data.get('created_by'),
        )

        CARDS_FULL_VALID_TEST_DATA.update({'created_by': 12344})
        response = self.client.post(
            path=CARDS_LIST_URL, data=CARDS_FULL_VALID_TEST_DATA
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            member='Invalid pk "12344" - object does not exist.',
            container=response.data.get('created_by'),
        )

    def test_can_create_card_with_not_existing_fields_passed(self):
        """
        A card can be created if we pass fields that aren't defined in Cards model,
        but that incorrect data will not be considered upon creating a card.
        Only valid data will be considered upon creation.
        Expected: True
        """

        CARDS_FULL_VALID_TEST_DATA_COPY.update({'test_field': 'test'})
        response = self.client.post(
            path=CARDS_LIST_URL, data=CARDS_FULL_VALID_TEST_DATA_COPY
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertFalse(response.data.get('test_field', False))


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
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_read_card_detail(self):
        """
        Checks if particular card detail can be received by a user who has rights to see it
        Expected: True
        """

        response = self.client.get(path=CARD_DETAIL_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            Cards.objects.get(pk=1).account_assigned,
            CARDS_FULL_VALID_REAL_DATA.get('account_assigned'),
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
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            Cards.objects.get(pk=1).account_assigned,
            data_to_update.get('account_assigned'),
        )

    def test_can_update_card(self):
        """
        Checks if particular card instance can be updated
        Expected: True
        """

        data_to_update = CARDS_FULL_VALID_REAL_DATA
        data_to_update.update({'account_assigned': 'UPDATED@test.com'})
        response = self.client.put(path=CARD_DETAIL_URL, data=data_to_update)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            Cards.objects.get(pk=1).account_assigned,
            data_to_update.get('account_assigned'),
        )

    def test_can_update_all_card_fields(self):
        """
        Checks if particular card instance can be completely updated
        with almost all available fields
        Expected: True
        """

        response = self.client.put(
            path=CARD_DETAIL_URL, data=CARDS_FULL_VALID_TEST_DATA_COPY
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            Cards.objects.get(pk=1).account_assigned,
            CARDS_FULL_VALID_TEST_DATA_COPY.get('account_assigned'),
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
