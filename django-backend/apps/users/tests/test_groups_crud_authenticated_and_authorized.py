from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from rest_framework.test import APITestCase

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management import call_command
from django.test import tag

from apps.users.models import User
from apps.users.tests.settings import GROUP_DATA, GROUP_DETAIL_URL, GROUPS_LIST_URL


@tag('groups', 'authenticated', 'authorized')
class GroupTest(APITestCase):
    """
    Group parent test class that inherits from APITestCase and has 'setUp' method
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
            'apps/users/tests/fixtures/group_fixture.json',
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
        self.assertEqual(Group.objects.count(), 1)


class CreateGroupTest(GroupTest):
    """
    Children class that contains all necessary methods to test
    if a group can be created
    """

    def setUp(self):
        super().setUp()

    def test_can_create_group(self):
        """
        Checks if a new group can be successfully created
        Expected: True
        """
        response = self.client.post(path=GROUPS_LIST_URL, data={'name': 'Test group'})

        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(Group.objects.count(), 2)

    def test_can_create_group_with_permissions(self):
        """
        Checks if a new group can be successfully created with set permissions
        Expected: True
        """
        response = self.client.post(path=GROUPS_LIST_URL, data=GROUP_DATA)

        self.assertEqual(response.status_code, HTTP_201_CREATED)


class ReadGroupTest(GroupTest):
    """
    Children class that contains all necessary methods to test
    if groups list and group detail can be read
    """

    def setUp(self):
        super().setUp()

    def test_can_read_group_list(self):
        """
        Checks if all groups list can be received
        Expected: True
        """
        response = self.client.get(path=GROUPS_LIST_URL)

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(User.objects.count(), 1)

    def test_can_read_group_detail(self):
        """
        Checks if particular group detail can be received
        Expected: True
        """
        response = self.client.get(path=GROUP_DETAIL_URL)

        self.assertEqual(response.status_code, HTTP_200_OK)


class UpdateGroupTest(GroupTest):
    """
    Children class that contains all necessary methods to test
    if group can be updated and partially updated
    """

    def setUp(self):
        super().setUp()

    def test_can_partial_update_group(self):
        """
        Checks if particular group instance can be partially updated
        Expected: True
        """
        response = self.client.patch(
            path=GROUP_DETAIL_URL, data={'name': 'PARTIALLY UPDATED'}
        )

        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_can_update_group(self):
        """
        Checks if particular group instance can be updated
        Expected: True
        """
        data_to_update = {
            'name': 'UPDATED',
            'permissions': GROUP_DATA.get('permissions'),
        }

        response = self.client.put(path=GROUP_DETAIL_URL, data=data_to_update)

        self.assertEqual(response.status_code, HTTP_200_OK)


class DeleteGroupTest(GroupTest):
    """
    Children class that contains all necessary methods to test
    if group can be deleted
    """

    def setUp(self):
        super().setUp()

    def test_can_delete_group(self):
        """
        Checks if a group can be deleted
        Expected: True
        """
        response = self.client.delete(path=GROUP_DETAIL_URL)

        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)
