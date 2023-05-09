from rest_framework.status import HTTP_403_FORBIDDEN
from rest_framework.test import APITestCase

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import tag

from apps.accounts.models import Accounts
from apps.accounts.tests.settings import (
    ACCOUNT_DETAIL_URL,
    ACCOUNTS_FULL_VALID_TEST_DATA,
    ACCOUNTS_LIST_URL,
)


@tag('accounts', 'authenticated', 'unauthorized')
class AccountTestUnauthorized(APITestCase):
    """
    Checks if unauthorized user can get access to all CRUD methods of the Accounts app.
    Expected: status code 403 Forbidden for all CRUD methods.
    """

    @classmethod
    def setUpTestData(cls):
        call_command('loaddata', 'apps/accounts/tests/fixtures/accounts_fixture.json')
        call_command(
            'loaddata',
            'apps/common_services/common_test_fixtures/test_user_fixture.json',
        )

    def setUp(self):
        self.superuser = get_user_model().objects.get(pk=2)

        self.client.login(
            username=self.superuser.username,
            password='test_user_password',
        )

        self.account = Accounts.objects.first()

    def test_fixtures_loaded(self):
        """
        Checks that the fixtures have been loaded correctly
        """
        self.assertEqual(Accounts.objects.count(), 1)
        self.assertEqual(get_user_model().objects.count(), 1)

    def test_can_create_account(self):
        """
        Checks if a new account can be successfully created if user is not authorized
        Expected: False
        """
        response = self.client.post(
            path=ACCOUNTS_LIST_URL, data=ACCOUNTS_FULL_VALID_TEST_DATA
        )
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_can_read_accounts_list(self):
        """
        Checks if all accounts list can be received if user is not authorized
        Expected: False
        """
        response = self.client.get(path=ACCOUNTS_LIST_URL)
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_can_read_account_detail(self):
        """
        Checks if account detail can be received if user is not authorized
        Expected: False
        """
        response = self.client.get(path=ACCOUNT_DETAIL_URL)
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_can_partial_update_account(self):
        """
        Checks if particular account instance can be partially updated if user is not authorized
        Expected: False
        """
        response = self.client.patch(
            path=ACCOUNT_DETAIL_URL, data={'email': 'PARTIALLY_UPDATED@test.com'}
        )
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_can_update_account(self):
        """
        Checks if particular account instance can be updated if user is not authorized
        Expected: False
        """
        response = self.client.put(
            path=ACCOUNT_DETAIL_URL, data=ACCOUNTS_FULL_VALID_TEST_DATA
        )
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_can_delete_account(self):
        """
        Checks if account instance can be deleted if user is not authorized
        Expected: False
        """
        response = self.client.delete(path=ACCOUNT_DETAIL_URL)
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)
