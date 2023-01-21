from django.urls import reverse

USERS_LIST_URL = reverse("all-users-list")
USER_DETAIL_URL = reverse("all-users-detail", kwargs={"pk": 2})
GROUPS_LIST_URL = reverse("all-groups-list")
GROUP_DETAIL_URL = reverse("all-groups-detail", kwargs={"pk": 1})

API_ROOT_URL = reverse("api-root")
SWAGGER_URL = reverse("schema-swagger-ui")
# USER_BASE_AUTH_LOGIN_URL = reverse('login')
# USER_BASE_AUTH_LOGOUT_URL = reverse('logout')

REQUIRED_SUPERUSER_DATA = {
    "username": "superuser",
    "first_name": "Super",
    "last_name": "User",
    "password": "super_user_password",
}

REQUIRED_USER_DATA = {
    "username": "mike",
    "first_name": "Mike",
    "last_name": "Tyson",
    "password": "mike_tyson_password",
}

FULL_USER_DATA = {
    "is_superuser": False,
    "username": "eric_johnson",
    "email": "eric_johnson@test.com",
    "is_staff": True,
    "is_active": True,
    "first_name": "Eric",
    "last_name": "Johnson",
    "password": "eric_johnson_password",
    "role": "Manager",
    "groups": [],
    "user_permissions": [41, 42, 44],
}

GROUP_DATA = {"name": "Managers", "permissions": [41, 42, 44]}
