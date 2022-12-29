from django.urls import reverse

CARDS_LIST_URL = reverse('all-cards-list')
CARD_DETAIL_URL = reverse('all-cards-detail', kwargs={'pk': 1})

REQUIRED_SUPERUSER_DATA = {
    "username": "superuser",
    "first_name": "Super",
    "last_name": "User",
    "password": "super_user_password"
}

REQUIRED_USER_DATA = {
    "username": "mike",
    "first_name": "Mike",
    "last_name": "Tyson",
    "password": "mike_tyson_password"
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
}


CARDS_FULL_VALID_TEST_DATA = {
    "account_assigned": "test_card_account@test.com",
    "platform": "Test platform",
    "type": "Test type",
    "parent_card": "Test parent card",
    "card_number": "1234567887654321",
    "expiration_date": "12/24",
    "cvv_number": "123",
    "team": "Test team",
    "specific_team": "Test specific team",
    "address": "Test address",
    "city": "Test city",
    "state": "TS",
    "zip_code": "67456",
    "in_tm": True,
    "in_tickets_com": False,
    "is_deleted": False,
}

CARDS_FULL_VALID_TEST_DATA_COPY = {
    "account_assigned": "test_card_account@test.com",
    "platform": "Test platform",
    "type": "Test type",
    "parent_card": "Test parent card",
    "card_number": "1234567887654321",
    "expiration_date": "12/24",
    "cvv_number": "123",
    "team": "Test team",
    "specific_team": "Test specific team",
    "address": "Test address",
    "city": "Test city",
    "state": "TS",
    "zip_code": "67456",
    "in_tm": True,
    "in_tickets_com": False,
    "is_deleted": False,
    "created_by": 1
}

CARDS_FULL_VALID_REAL_DATA = {
    "account_assigned": "Lawrence@phantasydraft.com",
    "platform": "DIVVY",
    "type": "VISA",
    "parent_card": "NA",
    "card_number": "4482130155618527",
    "expiration_date": "10/30",
    "cvv_number": "583",
    "team": "lawns",
    "specific_team": "NA",
    "address": "2120 Southside Lane",
    "city": "Los Angeles",
    "state": "CA",
    "zip_code": "90017",
    "in_tm": True,
    "in_tickets_com": False,
    "is_deleted": False,
}
