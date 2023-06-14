from django.urls import reverse

CARDS_LIST_URL = reverse('all-cards-list')
CARD_DETAIL_URL = reverse('all-cards-detail', kwargs={'pk': 1})

CARDS_FULL_VALID_TEST_DATA = {
    'account_assigned': 'john.doe@example.com',
    'platform': 'Test Platform',
    'type': 'Test Type',
    'parent_card': 'Test Parent Card',
    'card_number': '1234567890123456',
    'expiration_date': '12/22',
    'cvv_number': '123',
    'created_at': '2022-05-01',
    'updated_at': '2022-05-02',
    'created_by': 1,
    'team': 'Test Team',
    'specific_team': 'Test Specific Team',
    'address': 'Test Address',
    'city': 'Test City',
    'state': 'NY',
    'zip_code': '12345',
    'in_tm': False,
    'in_tickets_com': True,
    'is_deleted': False,
}
