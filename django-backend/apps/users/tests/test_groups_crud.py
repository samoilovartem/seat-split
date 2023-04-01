from django.contrib.auth.models import Group
from django.test import tag
from rest_framework import status
from rest_framework.test import APITestCase

from apps.users.models import User
from apps.users.serializers import GroupSerializer
from apps.users.tests.settings import (
    GROUP_DATA,
    GROUP_DETAIL_URL,
    GROUPS_LIST_URL,
    REQUIRED_SUPERUSER_DATA,
)


@tag("groups", "authenticated", "authorized")
class GroupTest(APITestCase):
    """
    Group parent test class that inherits from APITestCase and has 'setUp' method
    that children classes can use without repetition
    """

    def setUp(self):
        # creating test superuser, hashing its password and checking if raw password matches hashed one
        self.superuser = User.objects.create_superuser(**REQUIRED_SUPERUSER_DATA)
        self.superuser.set_password(REQUIRED_SUPERUSER_DATA.get("password"))
        self.superuser.save()
        self.assertTrue(
            self.superuser.check_password(REQUIRED_SUPERUSER_DATA.get("password"))
        )

        # logging in
        self.client.login(
            username=REQUIRED_SUPERUSER_DATA.get("username"),
            password=REQUIRED_SUPERUSER_DATA.get("password"),
        )


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

        response = self.client.post(path=GROUPS_LIST_URL, data={"name": "Managers"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_can_create_group_with_permissions(self):
        """
        Checks if a new group can be successfully created with set permissions
        Expected: True
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
        self.group = Group.objects.create(name=GROUP_DATA.get("name"))

        # Getting expected output to compare with response
        self.expected_output = GroupSerializer(self.group).data
        self.expected_output.update({"id": 1})

    def test_can_read_group_list(self):
        """
        Checks if all groups list can be received
        Expected: True
        """

        response = self.client.get(path=GROUPS_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Group.objects.get(pk=1).name, GROUP_DATA.get("name"))

    def test_can_read_group_detail(self):
        """
        Checks if particular group detail can be received
        Expected: True
        """

        response = self.client.get(path=GROUP_DETAIL_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.expected_output)


class UpdateGroupTest(GroupTest):
    """
    Children class that contains all necessary methods to test
    if group can be updated and partially updated
    """

    def setUp(self):
        super().setUp()

        # Creating test group
        self.group = Group.objects.create(name=GROUP_DATA.get("name"))

        # Getting expected output to compare with response
        self.expected_output = GroupSerializer(self.group).data
        self.expected_output.update({"id": 1, "name": "PARTIALLY UPDATED"})

    def test_can_partial_update_group(self):
        """
        Checks if particular group instance can be partially updated
        Expected: True
        """

        response = self.client.patch(
            path=GROUP_DETAIL_URL, data={"name": "PARTIALLY UPDATED"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.expected_output)

    def test_can_update_group(self):
        """
        Checks if particular group instance can be updated
        Expected: True
        """

        data_to_update = {
            "name": "UPDATED",
            "permissions": GROUP_DATA.get("permissions"),
        }
        response = self.client.put(path=GROUP_DETAIL_URL, data=data_to_update)
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
        self.group = Group.objects.create(name=GROUP_DATA.get("name"))

    def test_can_delete_group(self):
        """
        Checks if a group can be deleted
        Expected: True
        """

        response = self.client.delete(path=GROUP_DETAIL_URL)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
