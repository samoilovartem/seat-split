from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.test import APITestCase

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import tag

from apps.us_addresses.models import USAddresses
from apps.us_addresses.tests.settings import US_ADDRESSES_BASE_URL


@tag('accounts', 'authenticated', 'authorized')
class USAddressTest(APITestCase):
    """
    Account parent test class that inherits from APITestCase and has 'setUp' method
    that children classes can use without repetition
    """

    @classmethod
    def setUpTestData(cls):
        call_command(
            'loaddata', 'apps/us_addresses/tests/fixtures/us_addresses_fixture.json'
        )
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
        self.assertEqual(USAddresses.objects.count(), 5)
        self.assertEqual(get_user_model().objects.count(), 1)


class ReadUSAddressTest(USAddressTest):
    """
    Children class that contains all necessary methods to test
    if us_addresses list and us_address instance can be READ
    """

    def setUp(self):
        super().setUp()

    def test_can_get_us_addresses_list(self):
        """
        Checks if us_addresses list can be received if required params are presented
        (coordinates and distance):
        Example: /?coordinates=-85.98464644110949,33.99606697887743&distance=80000
        Expected: True
        """
        response = self.client.get(
            path=f'{US_ADDRESSES_BASE_URL}?coordinates=-85.98464644110949,33.99606697887743&distance=80000'
        )
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(response.data.get('results')), 5)

    def test_can_get_random_instance_of_us_addresses(self):
        """
        Checks if us_addresses random instance can be received if required params are presented
        (coordinates and distance) + random=true:
        Example: /?coordinates=-85.98464644110949,33.99606697887743&distance=80000&random=true
        Expected: True
        """
        response = self.client.get(
            path=f'{US_ADDRESSES_BASE_URL}?coordinates=-85.98464644110949,33.99606697887743&distance=80000&random=true'
        )
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertTrue(isinstance(response.data, dict))

    def test_can_get_us_addresses_list_without_required_params(self):
        """
        Checks if us_addresses list can be received if required params aren't presented
        (coordinates and distance):
        Example: /?coordinates=-85.98464644110949,33.99606697887743
        Expected: False
        """
        response = self.client.get(
            path=f'{US_ADDRESSES_BASE_URL}?coordinates=-85.98464644110949,33.99606697887743'
        )
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertIn(
            member='coordinates and distance are required fields',
            container=response.data.get('error'),
        )

    def test_can_get_us_addresses_list_with_wrong_required_params(self):
        """
        Checks if us_addresses list can be received if required params are wrong
        (coordinates and distance):
        Example: /?coordinates=weird_stuff&distance=80000
        Expected: False
        """
        response = self.client.get(
            path=f'{US_ADDRESSES_BASE_URL}?coordinates=weird_stuff&distance=80000'
        )
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertIn(
            member="Error parsing coordinates: could not convert string to float: 'weird_stuff'",
            container=response.data.get('error'),
        )

    def test_can_get_us_addresses_list_if_no_data_with_matched_criteria(self):
        """
        Checks if us_addresses list can be received if required params are wrong
        (coordinates and distance):
        Example: /?coordinates=-85.98464644110949,33.99606697887743&distance=10
        Expected: False
        """
        response = self.client.get(
            path=f'{US_ADDRESSES_BASE_URL}?coordinates=-85.98464644110949,33.99606697887743&distance=10'
        )
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(response.data.get('results')), 0)
