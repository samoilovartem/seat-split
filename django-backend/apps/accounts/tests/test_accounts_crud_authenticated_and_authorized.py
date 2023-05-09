from rest_framework import status
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
)
from rest_framework.test import APITestCase

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.db.models import BooleanField, CharField, DateField, EmailField
from django.test import tag

from apps.accounts.models import Accounts
from apps.accounts.tests.settings import (
    ACCOUNT_DETAIL_URL,
    ACCOUNTS_FULL_VALID_TEST_DATA,
    ACCOUNTS_LIST_URL,
)


@tag('accounts', 'authenticated', 'authorized')
class AccountsTest(APITestCase):
    """
    Account parent test class that inherits from APITestCase and has 'setUp' method
    that children classes can use without repetition
    """

    @classmethod
    def setUpTestData(cls):
        call_command('loaddata', 'apps/accounts/tests/fixtures/accounts_fixture.json')
        call_command(
            'loaddata',
            'apps/common_services/common_test_fixtures/superuser_fixture.json',
        )

    def setUp(self):
        self.superuser = get_user_model().objects.get(pk=1)

        self.client.login(
            username=self.superuser.username,
            password='super_user_password',
        )

        self.account = Accounts.objects.first()

    def test_fixtures_loaded(self):
        """
        Checks that the fixtures have been loaded correctly
        """
        self.assertEqual(Accounts.objects.count(), 1)
        self.assertEqual(get_user_model().objects.count(), 1)


class CreateAccountTest(AccountsTest):
    """
    Children class that contains all necessary methods to test if account can be CREATED
    """

    def setUp(self):
        super().setUp()

    def test_can_view_account_details(self):
        """
        Checks if particular account detail can be received by a user who has rights to see it
        Expected: True
        """
        response = self.client.get(path=ACCOUNT_DETAIL_URL)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(self.account.email, ACCOUNTS_FULL_VALID_TEST_DATA.get('email'))

    def test_required_char_fields(self):
        """
        Checks if a new account can be successfully created when required char fields are empty
        Expected: False
        """
        required_fields = [
            field.name
            for field in Accounts._meta.fields
            if isinstance(field, (CharField, EmailField)) and field.blank is False
        ]

        for field in required_fields:
            with self.subTest(field=field):
                invalid_data = ACCOUNTS_FULL_VALID_TEST_DATA.copy()
                invalid_data.update({field: ''})
                response = self.client.post(path=ACCOUNTS_LIST_URL, data=invalid_data)
                self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
                self.assertIn(
                    member='This field may not be blank.',
                    container=response.data.get(field),
                )

    def test_required_boolean_fields(self):
        """
        Checks if a new account can be successfully created when boolean fields have incorrect values
        Expected: False
        """
        boolean_fields = [
            field.name
            for field in Accounts._meta.fields
            if isinstance(field, BooleanField)
        ]

        for field in boolean_fields:
            with self.subTest(field=field):
                invalid_data = ACCOUNTS_FULL_VALID_TEST_DATA.copy()
                invalid_data.update({field: 'test'})
                response = self.client.post(path=ACCOUNTS_LIST_URL, data=invalid_data)
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
                self.assertIn(
                    member='Must be a valid boolean.',
                    container=response.data.get(field),
                )

    def test_required_date_fields(self):
        date_fields = [
            field.name
            for field in Accounts._meta.fields
            if isinstance(field, DateField)
        ]
        date_fields.remove('updated_at')

        for field in date_fields:
            # Test with an empty date field
            data_with_empty_date = ACCOUNTS_FULL_VALID_TEST_DATA.copy()
            data_with_empty_date[field] = ''
            response = self.client.post(
                path=ACCOUNTS_LIST_URL, data=data_with_empty_date
            )
            self.assertEqual(
                response.status_code,
                HTTP_400_BAD_REQUEST,
                f'Empty {field} should be invalid',
            )

            # Test with an invalid date format
            data_with_invalid_date = ACCOUNTS_FULL_VALID_TEST_DATA.copy()
            data_with_invalid_date[field] = 'invalid_date'
            response = self.client.post(
                path=ACCOUNTS_LIST_URL, data=data_with_invalid_date
            )
            self.assertEqual(
                response.status_code,
                HTTP_400_BAD_REQUEST,
                f'Invalid {field} format should be rejected',
            )

            # Test with a valid date
            data_with_valid_date = ACCOUNTS_FULL_VALID_TEST_DATA.copy()
            data_with_valid_date[field] = '2023-05-07'
            response = self.client.post(
                path=ACCOUNTS_LIST_URL, data=data_with_valid_date
            )
            self.assertEqual(
                response.status_code,
                HTTP_201_CREATED,
                f'Valid {field} should be accepted',
            )


class ReadAccountTest(AccountsTest):
    """
    Children class that contains all necessary methods to test
    if account list and account instance can be READ
    """

    def setUp(self):
        super().setUp()

    def test_can_read_accounts_list(self):
        """
        Checks if all accounts list can be received by a user who has rights to see them
        Expected: True
        """
        response = self.client.get(path=ACCOUNTS_LIST_URL)
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_can_read_account_detail(self):
        """
        Checks if particular account detail can be received by a user who has rights to see it
        Expected: True
        """
        response = self.client.get(path=ACCOUNT_DETAIL_URL)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(self.account.email, ACCOUNTS_FULL_VALID_TEST_DATA.get('email'))


class UpdateAccountTest(AccountsTest):
    """
    Children class that contains all necessary methods to test
    if account can be UPDATED and PARTIALLY UPDATED
    """

    def setUp(self):
        super().setUp()

    def test_can_partial_update_account(self):
        """
        Checks if particular account instance can be partially updated
        Expected: True
        """
        data_to_update = {'email': 'PARTIALLY_UPDATED@test.com'}
        response = self.client.patch(path=ACCOUNT_DETAIL_URL, data=data_to_update)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(Accounts.objects.get(pk=1).email, data_to_update.get('email'))

    def test_can_update_account(self):
        """
        Checks if particular account instance can be updated
        Expected: True
        """
        data_to_update = ACCOUNTS_FULL_VALID_TEST_DATA
        data_to_update.update({'email': 'UPDATED@test.com'})
        response = self.client.put(path=ACCOUNT_DETAIL_URL, data=data_to_update)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(Accounts.objects.get(pk=1).email, data_to_update.get('email'))


class DeleteAccountTest(AccountsTest):
    """
    Children class that contains all necessary methods to test
    if account can be DELETED
    """

    def setUp(self):
        super().setUp()

    def test_can_delete_account(self):
        """
        Checks if an account can be deleted
        Expected: True
        """
        response = self.client.delete(path=ACCOUNT_DETAIL_URL)
        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)
        self.assertEqual(Accounts.objects.all().count(), 0)
