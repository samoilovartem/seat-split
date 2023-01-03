from rest_framework import status
from rest_framework.test import APITestCase
from django.test import tag

from apps.users.models import User
from apps.users.serializers import GeneralUserSerializer, UserDetailSerializer, UserCreateSerializer
from apps.users.tests.settings import REQUIRED_SUPERUSER_DATA, USERS_LIST_URL, REQUIRED_USER_DATA, \
    USER_DETAIL_URL, FULL_USER_DATA


@tag('users', 'authenticated', 'authorized')
class UserTest(APITestCase):
    """
    User parent test class that inherits from APITestCase and has 'setUp' method
    that children classes can use without repetition
    """

    def setUp(self):

        # creating test superuser, hashing its password and checking if raw password matches hashed one
        self.superuser = User.objects.create_superuser(**REQUIRED_SUPERUSER_DATA)
        self.superuser.set_password(REQUIRED_SUPERUSER_DATA.get('password'))
        self.superuser.save()
        self.assertTrue(self.superuser.check_password(REQUIRED_SUPERUSER_DATA.get('password')))

        # creating test superuser, hashing its password and checking if raw password matches hashed one
        self.client.login(username=REQUIRED_SUPERUSER_DATA.get('username'),
                          password=REQUIRED_SUPERUSER_DATA.get('password'))


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
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(response.data, self.expected_output)

    def test_can_create_user_with_all_fields(self):
        """
        Checks if a new user can be successfully created with all fields (not only required) filled
        Expected: True
        """

        response = self.client.post(path=USERS_LIST_URL, data=FULL_USER_DATA)
        self.expected_output = UserCreateSerializer(User.objects.get(pk=2)).data
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(response.data, self.expected_output)

    def test_can_create_user_without_required_fields(self):
        """
        Checks if a new user can be successfully created without required fields:
        - username, first_name, last_name, password
        Expected: False
        """

        incomplete_data = {'username': REQUIRED_USER_DATA.get('username'),
                           'password': REQUIRED_USER_DATA.get('password')}
        response = self.client.post(path=USERS_LIST_URL, data=incomplete_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ReadUserTest(UserTest):
    """
    Children class that contains all necessary methods to test
    if user list and user detail can be read
    """

    def setUp(self):
        super().setUp()

        # Creating test user, hashing its password and checking if raw password matches hashed one
        self.user = User.objects.create(**REQUIRED_USER_DATA)
        self.user.set_password(REQUIRED_USER_DATA.get('password'))
        self.user.save()
        self.assertTrue(self.user.check_password(REQUIRED_USER_DATA.get('password')))

        # Getting expected output to compare with response
        self.expected_output = UserDetailSerializer(self.user).data

    def test_can_read_user_list(self):
        """
        Checks if all users list can be received
        Expected: True
        """

        response = self.client.get(path=USERS_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(User.objects.get(pk=1).first_name, REQUIRED_SUPERUSER_DATA.get('first_name'))
        self.assertEqual(User.objects.get(pk=2).first_name, REQUIRED_USER_DATA.get('first_name'))

    def test_can_read_user_detail(self):
        """
        Checks if particular user detail can be received
        Expected: True
        """

        response = self.client.get(path=USER_DETAIL_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.expected_output)


class UpdateUserTest(UserTest):
    """
    Children class that contains all necessary methods to test
    if user can be updated and partially updated
    """

    def setUp(self):
        super().setUp()

        # Creating test user, hashing its password and checking if raw password matches hashed one
        self.user = User.objects.create(**REQUIRED_USER_DATA)
        self.user.set_password(REQUIRED_USER_DATA.get('password'))
        self.user.save()
        self.assertTrue(self.user.check_password(REQUIRED_USER_DATA.get('password')))

        # Getting expected output to compare with response
        self.data = GeneralUserSerializer(self.user).data
        self.data['first_name'] = 'PARTIALLY UPDATED'
        self.expected_output = self.data

    def test_can_partial_update_user(self):
        """
        Checks if particular user instance can be partially updated
        Expected: True
        """

        response = self.client.patch(path=USER_DETAIL_URL, data={'first_name': 'PARTIALLY UPDATED'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.expected_output)

    def test_can_update_user(self):
        """
        Checks if particular user instance can be updated
        Expected: True
        """

        data_to_update = {'first_name': 'UPDATED',
                          'last_name': 'UPDATED',
                          'username': REQUIRED_USER_DATA.get('username')}
        response = self.client.put(path=USER_DETAIL_URL,
                                   data=data_to_update)
        self.expected_output.update(data_to_update)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.expected_output)

    def test_can_update_all_user_fields(self):
        """
        Checks if particular user instance can be completely updated
        with almost all available fields
        Expected: True
        """

        data_to_update = FULL_USER_DATA
        data_to_update.pop('password', None)
        response = self.client.put(path=USER_DETAIL_URL,
                                   data=data_to_update)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class DeleteUserTest(UserTest):
    """
    Children class that contains all necessary methods to test
    if user can be deleted
    """

    def setUp(self):
        super().setUp()

        # Creating test user, hashing its password and checking if raw password matches hashed one
        self.user = User.objects.create(**REQUIRED_USER_DATA)
        self.user.set_password(REQUIRED_USER_DATA.get('password'))
        self.user.save()
        self.assertTrue(self.user.check_password(REQUIRED_USER_DATA.get('password')))

    def test_can_delete_user(self):
        """
        Checks if a user can be deleted
        Expected: True
        """

        response = self.client.delete(path=USER_DETAIL_URL)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


