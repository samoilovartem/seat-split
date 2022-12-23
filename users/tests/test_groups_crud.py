from rest_framework import status
from rest_framework.test import APITestCase
from django.test import tag

from users.models import User
from django.contrib.auth.models import Group

from users.serializers import GroupSerializer
from users.tests.settings import REQUIRED_SUPERUSER_DATA, GROUPS_LIST_URL, GROUP_DATA, GROUP_DETAIL_URL


@tag('groups')
class GroupTest(APITestCase):
    """
    Group parent test class that inherits from APITestCase and has 'setUp' method
    that children classes can use without repetition
    """

    def setUp(self):
        # creating test superuser, hashing its password and checking if raw password matches hashed one
        self.superuser = User.objects.create_superuser(**REQUIRED_SUPERUSER_DATA)
        self.superuser.set_password(REQUIRED_SUPERUSER_DATA.get('password'))
        self.superuser.save()
        self.assertTrue(self.superuser.check_password(REQUIRED_SUPERUSER_DATA.get('password')))

        # logging in
        self.client.login(username=REQUIRED_SUPERUSER_DATA.get('username'),
                          password=REQUIRED_SUPERUSER_DATA.get('password'))


class CreateGroupTest(GroupTest):
    def setUp(self):
        super().setUp()

    @tag('positive')
    def test_can_create_group(self):
        """
        Checks if new group can be successfully created
        """

        response = self.client.post(path=GROUPS_LIST_URL, data={'name': 'Managers'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @tag('positive')
    def test_can_create_group_with_permissions(self):
        """
        Checks if new group can be successfully created
        """

        response = self.client.post(path=GROUPS_LIST_URL, data=GROUP_DATA)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ReadGroupTest(GroupTest):
    """
    Children class that contains all necessary methods to test
    if groups list and group detail can be read
    """

    def setUp(self):
        super().setUp()

        # Creating test group
        self.group = Group.objects.create(name=GROUP_DATA.get('name'))

        # Getting expected output to compare with response
        self.expected_output = GroupSerializer(self.group).data
        self.expected_output.update({'id': 1})

    @tag('positive')
    def test_can_read_group_list(self):
        """
        Checks if all groups list can be received
        """

        response = self.client.get(path=GROUPS_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Group.objects.get(pk=1).name, GROUP_DATA.get('name'))

    @tag('positive')
    def test_can_read_group_detail(self):
        """
        Checks if particular group detail can be received
        """

        response = self.client.get(path=GROUP_DETAIL_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.expected_output)


class UpdateGroupTest(GroupTest):
    """
    Children class that contains all necessary methods to test
    if group can be updated and partial updated
    """
    def setUp(self):
        super().setUp()

        # Creating test group
        self.group = Group.objects.create(name=GROUP_DATA.get('name'))

        # Getting expected output to compare with response
        self.expected_output = GroupSerializer(self.group).data
        self.expected_output.update({'id': 1, 'name': 'PARTIALLY UPDATED'})

    @tag('positive')
    def test_can_partial_update_group(self):
        """
        Checks if particular group instance can be partially updated
        """

        response = self.client.patch(path=GROUP_DETAIL_URL, data={'name': 'PARTIALLY UPDATED'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.expected_output)

    @tag('positive')
    def test_can_update_group(self):
        """
        Checks if particular group instance can be updated
        """

        data_to_update = {'name': 'UPDATED',
                          'permissions': GROUP_DATA.get('permissions')}
        response = self.client.put(path=GROUP_DETAIL_URL,
                                   data=data_to_update)
        self.expected_output.update(data_to_update)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.expected_output)


class DeleteGroupTest(GroupTest):
    """
    Children class that contains all necessary methods to test
    if group can be deleted
    """
    def setUp(self):
        super().setUp()

        # Creating test group
        self.group = Group.objects.create(name=GROUP_DATA.get('name'))

    @tag('positive')
    def test_can_delete_group(self):
        """
        Checks if a group can be deleted
        """
        response = self.client.delete(path=GROUP_DETAIL_URL)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


@tag('groups', 'unauthenticated')
class CreateGroupTestNotAuthenticated(APITestCase):
    """
    Group parent test class that inherits from APITestCase and has 'setUp' method
    that children classes can use without repetition
    """

    def setUp(self):
        self.group = Group.objects.create(name=GROUP_DATA.get('name'))

    @tag('positive')
    def test_can_create_group(self):
        """
        Checks if new group can be successfully created if user is not authenticated
        """

        response = self.client.post(path=GROUPS_LIST_URL, data={'name': 'test_group'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @tag('positive')
    def test_can_read_groups_list(self):
        """
        Checks if all groups list can be received if user is not authenticated
        """

        response = self.client.get(path=GROUPS_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @tag('positive')
    def test_can_read_group_detail(self):
        """
        Checks if group detail can be received if user is not authenticated
        """

        response = self.client.get(path=GROUP_DETAIL_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @tag('positive')
    def test_can_partial_update_group(self):
        """
        Checks if particular group instance can be partially updated if user is not authenticated
        """

        response = self.client.patch(path=GROUP_DETAIL_URL, data={'name': 'PARTIALLY UPDATED'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @tag('positive')
    def test_can_update_group(self):
        """
        Checks if particular group instance can be updated if user is not authenticated
        """

        data_to_update = {'name': 'UPDATED',
                          'permissions': GROUP_DATA.get('permissions')}
        response = self.client.put(path=GROUP_DETAIL_URL,
                                   data=data_to_update)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @tag('positive')
    def test_can_delete_group(self):
        """
        Checks if a group can be deleted if user is not authenticated
        """
        response = self.client.delete(path=GROUP_DETAIL_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)



