from django.test import tag
from rest_framework import status
from rest_framework.test import APITestCase

from apps.accounts.models import Accounts
from apps.accounts.tests.settings import (
    ACCOUNT_DETAIL_URL,
    ACCOUNTS_FULL_VALID_REAL_DATA,
    ACCOUNTS_FULL_VALID_TEST_DATA,
    ACCOUNTS_LIST_URL,
    FULL_USER_DATA,
)
from apps.users.models import User


@tag('accounts', 'authenticated', 'unauthorized')
class AccountTestUnauthorized(APITestCase):
    """
    Checks if unauthorized user can get access to all CRUD methods of the Accounts app.
    Expected: status code 403 Forbidden for all CRUD methods.
    """

    def setUp(self):

        # creating test user, hashing its password and checking if raw password matches hashed one
        self.user = User.objects.create(**FULL_USER_DATA)
        self.user.set_password(FULL_USER_DATA.get('password'))
        self.user.save()
        self.assertTrue(self.user.check_password(FULL_USER_DATA.get('password')))

        # logging in a test user
        self.client.login(
            username=FULL_USER_DATA.get('username'),
            password=FULL_USER_DATA.get('password'),
        )

        # creating one real card for next tests
        self.card = Accounts.objects.create(**ACCOUNTS_FULL_VALID_REAL_DATA)

    def test_can_create_account(self):
        """
        Checks if a new account can be successfully created if user is not authorized
        Expected: False
        """

        response = self.client.post(
            path=ACCOUNTS_LIST_URL, data=ACCOUNTS_FULL_VALID_TEST_DATA
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_can_read_accounts_list(self):
        """
        Checks if all accounts list can be received if user is not authorized
        Expected: False
        """

        response = self.client.get(path=ACCOUNTS_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_can_read_account_detail(self):
        """
        Checks if account detail can be received if user is not authorized
        Expected: False
        """

        response = self.client.get(path=ACCOUNT_DETAIL_URL)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_can_partial_update_account(self):
        """
        Checks if particular account instance can be partially updated if user is not authorized
        Expected: False
        """

        response = self.client.patch(
            path=ACCOUNT_DETAIL_URL, data={'email': 'PARTIALLY_UPDATED@test.com'}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_can_update_account(self):
        """
        Checks if particular account instance can be updated if user is not authorized
        Expected: False
        """

        response = self.client.put(
            path=ACCOUNT_DETAIL_URL, data=ACCOUNTS_FULL_VALID_TEST_DATA
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_can_delete_account(self):
        """
        Checks if account instance can be deleted if user is not authorized
        Expected: False
        """

        response = self.client.delete(path=ACCOUNT_DETAIL_URL)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
