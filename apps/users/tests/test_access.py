from django.test import tag
from rest_framework import status
from rest_framework.test import APITestCase

from apps.users.tests.settings import API_ROOT_URL, SWAGGER_URL


@tag('access')
class AccessTest(APITestCase):

    def test_can_access_api_root_if_unauthenticated(self):
        """
        Checks if unauthenticated user can get access to api root
        Expected: False
        """

        response = self.client.get(path=API_ROOT_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_access_swagger_if_unauthenticated(self):
        """
        Checks if unauthenticated user can get access to swagger
        Expected: False
        """

        response = self.client.get(path=SWAGGER_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)



