from rest_framework import status, serializers
from rest_framework.test import APITestCase
from django.urls import reverse

from .models import User
from users.serializers import GeneralUserSerializer

USERS_LIST_URL = reverse('all-users-list')
USERS_DETAIL_URL = reverse('all-users-detail', kwargs={'pk': 1})

SUPERUSER_DATA = {
    'username': 'superuser',
    'first_name': 'Super',
    'last_name': 'User',
    'password': 'super_user_password',
}

USER_DATA = {
    'username': 'mike',
    'first_name': 'Mike',
    'last_name': 'Tyson',
    'password': 'mike_tyson_password'
}


class CreateUserTest(APITestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(**SUPERUSER_DATA)
        self.client.login(username=SUPERUSER_DATA.get('username'),
                          password=SUPERUSER_DATA.get('password'))
        self.data = USER_DATA

    def test_can_create_user(self):
        response = self.client.post(path=USERS_LIST_URL, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ReadUserTest(APITestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(**SUPERUSER_DATA)
        self.client.login(username=SUPERUSER_DATA.get('username'),
                          password=SUPERUSER_DATA.get('password'))
        self.user = User.objects.create(**USER_DATA)

    def test_can_read_user_list(self):
        response = self.client.get(path=USERS_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_read_user_detail(self):
        response = self.client.get(path=USERS_DETAIL_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(
            [self.user.username, self.user.first_name,
             self.user.last_name, self.user.password],
            [USER_DATA.get('username'), USER_DATA.get('first_name'),
             USER_DATA.get('last_name'), USER_DATA.get('password')]
        )


# class UpdateUserTest(APITestCase):
#     def setUp(self):
#         self.superuser = User.objects.create_superuser(**SUPERUSER_DATA)
#         self.client.login(username=SUPERUSER_DATA.get('username'),
#                           password=SUPERUSER_DATA.get('password'))
#         self.user = User.objects.create(**USER_DATA)
#         self.data = GeneralUserSerializer(self.user).data
#         self.data.update({'first_name': 'Changed'})
#
#     def test_can_update_user(self):
#         response = self.client.put(path=USERS_DETAIL_URL, data=self.data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(self.user.first_name, 'Changed')


class DeleteUserTest(APITestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(**SUPERUSER_DATA)
        self.client.login(username=SUPERUSER_DATA.get('username'),
                          password=SUPERUSER_DATA.get('password'))
        self.user = User.objects.create(**USER_DATA)

    def test_can_delete_user(self):
        response = self.client.delete(path=USERS_DETAIL_URL)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
