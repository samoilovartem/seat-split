from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
)
from rest_framework.test import APITestCase

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import tag

from apps.users.models import User
from apps.users.serializers import UserCreateSerializer
from apps.users.tests.settings import (
    FULL_USER_DATA,
    REQUIRED_USER_DATA,
    USER_DETAIL_URL,
    USERS_LIST_URL,
)


@tag('users', 'authenticated', 'authorized')
class UserTest(APITestCase):
    """
    User parent test class that inherits from APITestCase and has 'setUp' method
    that children classes can use without repetition
    """

    @classmethod
    def setUpTestData(cls):
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

    def test_fixtures_loaded(self):
        """
        Checks that the fixtures have been loaded correctly
        """
        self.assertEqual(get_user_model().objects.count(), 1)


class CreateUserTest(UserTest):
    """
    Children class that contains all necessary methods to test if user can be created
    """

    def setUp(self):
        super().setUp()

    def test_can_create_user(self):
        """
        Checks if a new user can be successfully created
        Expected: True
        """
        response = self.client.post(path=USERS_LIST_URL, data=REQUIRED_USER_DATA)

        self.expected_output = UserCreateSerializer(User.objects.get(pk=2)).data

        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(response.data, self.expected_output)

    def test_can_create_user_with_all_fields(self):
        """
        Checks if a new user can be successfully created with all fields (not only required) filled
        Expected: True
        """
        response = self.client.post(path=USERS_LIST_URL, data=FULL_USER_DATA)

        self.expected_output = UserCreateSerializer(User.objects.get(pk=3)).data

        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(response.data, self.expected_output)

    def test_can_create_user_without_required_fields(self):
        """
        Checks if a new user can be successfully created without required fields:
        - username, first_name, last_name, password
        Expected: False
        """
        incomplete_data = {
            'username': REQUIRED_USER_DATA.get('username'),
            'password': REQUIRED_USER_DATA.get('password'),
        }

        response = self.client.post(path=USERS_LIST_URL, data=incomplete_data)

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)


class ReadUserTest(UserTest):
    """
    Children class that contains all necessary methods to test
    if user list and user detail can be read
    """

    def setUp(self):
        super().setUp()

    def test_can_read_user_list(self):
        """
        Checks if all users list can be received
        Expected: True
        """
        response = self.client.get(path=USERS_LIST_URL)

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(User.objects.count(), 1)

    def test_can_read_user_detail(self):
        """
        Checks if particular user detail can be received
        Expected: True
        """
        response = self.client.get(path=USER_DETAIL_URL)

        self.assertEqual(response.status_code, HTTP_200_OK)


class UpdateUserTest(UserTest):
    """
    Children class that contains all necessary methods to test
    if user can be updated and partially updated
    """

    def setUp(self):
        super().setUp()

    def test_can_partial_update_user(self):
        """
        Checks if particular user instance can be partially updated
        Expected: True
        """
        response = self.client.patch(
            path=USER_DETAIL_URL, data={'first_name': 'PARTIALLY UPDATED'}
        )

        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_can_update_all_user_fields(self):
        """
        Checks if particular user instance can be completely updated
        with almost all available fields
        Expected: True
        """
        data_to_update = FULL_USER_DATA
        data_to_update.pop('password', None)

        response = self.client.put(path=USER_DETAIL_URL, data=data_to_update)

        self.assertEqual(response.status_code, HTTP_200_OK)


class DeleteUserTest(UserTest):
    """
    Children class that contains all necessary methods to test
    if user can be deleted
    """

    def setUp(self):
        super().setUp()

    def test_can_delete_user(self):
        """
        Checks if a user can be deleted
        Expected: True
        """
        response = self.client.delete(path=USER_DETAIL_URL)

        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)
