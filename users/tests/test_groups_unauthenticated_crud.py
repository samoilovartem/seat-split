from rest_framework import status
from rest_framework.test import APITestCase
from django.test import tag

from django.contrib.auth.models import Group

from users.tests.settings import GROUP_DATA, GROUPS_LIST_URL, GROUP_DETAIL_URL


@tag('groups', 'unauthenticated')
class GroupTestUnauthenticated(APITestCase):
    """
    Checks if unauthenticated user can get access to all CRUD methods of the API.
    Expected: status code 401 unauthorized.
    """

    def setUp(self):

        # Creating a test group
        self.group = Group.objects.create(name=GROUP_DATA.get('name'))

    def test_can_create_group(self):
        """
        Checks if new group can be successfully created if user is not authenticated
        Expected: False
        """

        response = self.client.post(path=GROUPS_LIST_URL, data={'name': 'test_group'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_read_groups_list(self):
        """
        Checks if all groups list can be received if user is not authenticated
        Expected: False
        """

        response = self.client.get(path=GROUPS_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_read_group_detail(self):
        """
        Checks if a group detail can be received if user is not authenticated
        Expected: False
        """

        response = self.client.get(path=GROUP_DETAIL_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_partial_update_group(self):
        """
        Checks if particular group instance can be partially updated if user is not authenticated
        Expected: False
        """

        response = self.client.patch(path=GROUP_DETAIL_URL, data={'name': 'PARTIALLY UPDATED'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_update_group(self):
        """
        Checks if particular group instance can be updated if user is not authenticated
        Expected: False
        """

        data_to_update = {'name': 'UPDATED',
                          'permissions': GROUP_DATA.get('permissions')}
        response = self.client.put(path=GROUP_DETAIL_URL,
                                   data=data_to_update)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_delete_group(self):
        """
        Checks if a group can be deleted if user is not authenticated
        Expected: False
        """

        response = self.client.delete(path=GROUP_DETAIL_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
