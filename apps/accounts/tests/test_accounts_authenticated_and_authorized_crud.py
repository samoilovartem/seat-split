from rest_framework import status
from rest_framework.test import APITestCase
from django.test import tag

from apps.accounts.tests.settings import FULL_USER_DATA, ACCOUNTS_LIST_URL, ACCOUNT_DETAIL_URL, \
    ACCOUNTS_FULL_VALID_REAL_DATA, ACCOUNTS_FULL_VALID_TEST_DATA, ACCOUNTS_FULL_VALID_TEST_DATA_COPY
from apps.users.models import User
from apps.accounts.models import Accounts


@tag('accounts', 'authenticated', 'authorized')
class AccountsTest(APITestCase):
    """
    Account parent test class that inherits from APITestCase and has 'setUp' method
    that children classes can use without repetition
    """

    def setUp(self):
        # Creating test user, hashing its password and checking if raw password matches hashed one
        self.user = User.objects.create(**FULL_USER_DATA)
        self.user.set_password(FULL_USER_DATA.get('password'))
        self.user.user_permissions.add(47, 48, 49, 50)
        self.user.save()
        self.assertTrue(self.user.check_password(FULL_USER_DATA.get('password')))

        # logging in a test user
        self.client.login(username=FULL_USER_DATA.get('username'),
                          password=FULL_USER_DATA.get('password'))

        # creating one real card for next tests
        self.account = Accounts.objects.create(**ACCOUNTS_FULL_VALID_REAL_DATA)


class CreateAccountTest(AccountsTest):
    """
    Children class that contains all necessary methods to test if account can be CREATED
    """

    def setUp(self):
        super().setUp()

    def test_can_create_account(self):
        """
        Checks if a new account can be successfully created
        Expected: True
        """

        response = self.client.post(path=ACCOUNTS_LIST_URL, data=ACCOUNTS_FULL_VALID_TEST_DATA)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Accounts.objects.count(), 2)
        self.assertEqual(response.data.get('email'),
                         ACCOUNTS_FULL_VALID_TEST_DATA.get('email'))

    def test_can_create_account_with_empty_first_name(self):
        """
        Checks if a new account can be successfully created with an empty first_name
        Expected: False
        """

        ACCOUNTS_FULL_VALID_TEST_DATA.update({'first_name': ''})
        response = self.client.post(path=ACCOUNTS_LIST_URL, data=ACCOUNTS_FULL_VALID_TEST_DATA)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(member='This field may not be blank.',
                      container=response.data.get('first_name'))

    def test_can_create_account_with_empty_last_name(self):
        """
        Checks if a new account can be successfully created with an empty last_name
        Expected: False
        """

        ACCOUNTS_FULL_VALID_TEST_DATA.update({'last_name': ''})
        response = self.client.post(path=ACCOUNTS_LIST_URL, data=ACCOUNTS_FULL_VALID_TEST_DATA)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(member='This field may not be blank.',
                      container=response.data.get('last_name'))

    def test_can_create_account_with_incorrect_email(self):
        """
        Checks if a new account can be successfully created with an incorrect email
        Expected: False
        """

        ACCOUNTS_FULL_VALID_TEST_DATA.update({'email': 'test'})
        response = self.client.post(path=ACCOUNTS_LIST_URL, data=ACCOUNTS_FULL_VALID_TEST_DATA)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(member='Enter a valid email address.',
                      container=response.data.get('email'))

    def test_can_create_account_with_empty_email(self):
        """
        Checks if a new account can be successfully created with an empty email
        Expected: False
        """

        ACCOUNTS_FULL_VALID_TEST_DATA.update({'email': ''})
        response = self.client.post(path=ACCOUNTS_LIST_URL, data=ACCOUNTS_FULL_VALID_TEST_DATA)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(member='This field may not be blank.',
                      container=response.data.get('email'))

    def test_can_create_account_with_empty_type(self):
        """
        Checks if a new account can be successfully created with an empty type
        Expected: False
        """

        ACCOUNTS_FULL_VALID_TEST_DATA.update({'type': ''})
        response = self.client.post(path=ACCOUNTS_LIST_URL, data=ACCOUNTS_FULL_VALID_TEST_DATA)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(member='This field may not be blank.',
                      container=response.data.get('type'))

    def test_can_create_account_with_empty_password(self):
        """
        Checks if a new account can be successfully created with an empty password
        Expected: False
        """

        ACCOUNTS_FULL_VALID_TEST_DATA.update({'password': ''})
        response = self.client.post(path=ACCOUNTS_LIST_URL, data=ACCOUNTS_FULL_VALID_TEST_DATA)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(member='This field may not be blank.',
                      container=response.data.get('password'))

    def test_can_create_account_with_empty_recovery_email(self):
        """
        Checks if a new account can be successfully created with an empty recovery_email
        Expected: False
        """

        ACCOUNTS_FULL_VALID_TEST_DATA.update({'recovery_email': ''})
        response = self.client.post(path=ACCOUNTS_LIST_URL, data=ACCOUNTS_FULL_VALID_TEST_DATA)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(member='This field may not be blank.',
                      container=response.data.get('recovery_email'))

    def test_can_create_account_with_incorrect_email_forwarding(self):
        """
        Checks if a new account can be successfully created with an incorrect email_forwarding
        Expected: False
        """

        ACCOUNTS_FULL_VALID_TEST_DATA.update({'email_forwarding': 'test'})
        response = self.client.post(path=ACCOUNTS_LIST_URL, data=ACCOUNTS_FULL_VALID_TEST_DATA)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(member='Must be a valid boolean.',
                      container=response.data.get('email_forwarding'))

    def test_can_create_account_with_incorrect_auto_po_seats_scouts(self):
        """
        Checks if a new account can be successfully created with an incorrect auto_po_seats_scouts
        Expected: False
        """

        ACCOUNTS_FULL_VALID_TEST_DATA.update({'auto_po_seats_scouts': 'test'})
        response = self.client.post(path=ACCOUNTS_LIST_URL, data=ACCOUNTS_FULL_VALID_TEST_DATA)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(member='Must be a valid boolean.',
                      container=response.data.get('auto_po_seats_scouts'))

    def test_can_create_account_with_empty_errors_failed(self):
        """
        Checks if a new account can be successfully created with an empty errors_failed
        Expected: False
        """

        ACCOUNTS_FULL_VALID_TEST_DATA.update({'errors_failed': ''})
        response = self.client.post(path=ACCOUNTS_LIST_URL, data=ACCOUNTS_FULL_VALID_TEST_DATA)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(member='This field may not be blank.',
                      container=response.data.get('errors_failed'))

    def test_can_create_account_with_incorrect_tm_created(self):
        """
        Checks if a new account can be successfully created with an incorrect tm_created
        Expected: False
        """

        ACCOUNTS_FULL_VALID_TEST_DATA.update({'tm_created': 'test'})
        response = self.client.post(path=ACCOUNTS_LIST_URL, data=ACCOUNTS_FULL_VALID_TEST_DATA)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(member='Must be a valid boolean.',
                      container=response.data.get('tm_created'))

    def test_can_create_account_with_empty_tm_password(self):
        """
        Checks if a new account can be successfully created with an empty tm_password
        Expected: False
        """

        ACCOUNTS_FULL_VALID_TEST_DATA.update({'tm_password': ''})
        response = self.client.post(path=ACCOUNTS_LIST_URL, data=ACCOUNTS_FULL_VALID_TEST_DATA)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(member='This field may not be blank.',
                      container=response.data.get('tm_password'))

    def test_can_create_account_with_incorrect_axs_created(self):
        """
        Checks if a new account can be successfully created with an incorrect axs_created
        Expected: False
        """

        ACCOUNTS_FULL_VALID_TEST_DATA.update({'axs_created': 'test'})
        response = self.client.post(path=ACCOUNTS_LIST_URL, data=ACCOUNTS_FULL_VALID_TEST_DATA)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(member='Must be a valid boolean.',
                      container=response.data.get('axs_created'))

    def test_can_create_account_with_empty_axs_password(self):
        """
        Checks if a new account can be successfully created with an empty axs_password
        Expected: False
        """

        ACCOUNTS_FULL_VALID_TEST_DATA.update({'axs_password': ''})
        response = self.client.post(path=ACCOUNTS_LIST_URL, data=ACCOUNTS_FULL_VALID_TEST_DATA)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(member='This field may not be blank.',
                      container=response.data.get('axs_password'))

    def test_can_create_account_with_incorrect_sg_created(self):
        """
        Checks if a new account can be successfully created with an incorrect sg_created
        Expected: False
        """

        ACCOUNTS_FULL_VALID_TEST_DATA.update({'sg_created': 'test'})
        response = self.client.post(path=ACCOUNTS_LIST_URL, data=ACCOUNTS_FULL_VALID_TEST_DATA)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(member='Must be a valid boolean.',
                      container=response.data.get('sg_created'))

    def test_can_create_account_with_empty_sg_password(self):
        """
        Checks if a new account can be successfully created with an empty sg_password
        Expected: False
        """

        ACCOUNTS_FULL_VALID_TEST_DATA.update({'sg_password': ''})
        response = self.client.post(path=ACCOUNTS_LIST_URL, data=ACCOUNTS_FULL_VALID_TEST_DATA)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(member='This field may not be blank.',
                      container=response.data.get('sg_password'))

    def test_can_create_account_with_incorrect_tickets_com_created(self):
        """
        Checks if a new account can be successfully created with an incorrect tickets_com_created
        Expected: False
        """

        ACCOUNTS_FULL_VALID_TEST_DATA.update({'tickets_com_created': 'test'})
        response = self.client.post(path=ACCOUNTS_LIST_URL, data=ACCOUNTS_FULL_VALID_TEST_DATA)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(member='Must be a valid boolean.',
                      container=response.data.get('tickets_com_created'))

    def test_can_create_account_with_incorrect_eventbrite(self):
        """
        Checks if a new account can be successfully created with an incorrect eventbrite
        Expected: False
        """

        ACCOUNTS_FULL_VALID_TEST_DATA.update({'eventbrite': 'test'})
        response = self.client.post(path=ACCOUNTS_LIST_URL, data=ACCOUNTS_FULL_VALID_TEST_DATA)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(member='Must be a valid boolean.',
                      container=response.data.get('eventbrite'))

    def test_can_create_account_with_incorrect_etix(self):
        """
        Checks if a new account can be successfully created with an incorrect etix
        Expected: False
        """

        ACCOUNTS_FULL_VALID_TEST_DATA.update({'etix': 'test'})
        response = self.client.post(path=ACCOUNTS_LIST_URL, data=ACCOUNTS_FULL_VALID_TEST_DATA)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(member='Must be a valid boolean.',
                      container=response.data.get('etix'))

    def test_can_create_account_with_incorrect_ticket_web(self):
        """
        Checks if a new account can be successfully created with an incorrect ticket_web
        Expected: False
        """

        ACCOUNTS_FULL_VALID_TEST_DATA.update({'ticket_web': 'test'})
        response = self.client.post(path=ACCOUNTS_LIST_URL, data=ACCOUNTS_FULL_VALID_TEST_DATA)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(member='Must be a valid boolean.',
                      container=response.data.get('ticket_web'))

    def test_can_create_account_with_incorrect_big_tickets(self):
        """
        Checks if a new account can be successfully created with an incorrect big_tickets
        Expected: False
        """

        ACCOUNTS_FULL_VALID_TEST_DATA.update({'big_tickets': 'test'})
        response = self.client.post(path=ACCOUNTS_LIST_URL, data=ACCOUNTS_FULL_VALID_TEST_DATA)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(member='Must be a valid boolean.',
                      container=response.data.get('big_tickets'))

    def test_can_create_account_with_incorrect_amazon(self):
        """
        Checks if a new account can be successfully created with an incorrect amazon
        Expected: False
        """

        ACCOUNTS_FULL_VALID_TEST_DATA.update({'amazon': 'test'})
        response = self.client.post(path=ACCOUNTS_LIST_URL, data=ACCOUNTS_FULL_VALID_TEST_DATA)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(member='Must be a valid boolean.',
                      container=response.data.get('amazon'))

    def test_can_create_account_with_empty_secondary_password(self):
        """
        Checks if a new account can be successfully created with an empty secondary_password
        Expected: False
        """

        ACCOUNTS_FULL_VALID_TEST_DATA.update({'secondary_password': ''})
        response = self.client.post(path=ACCOUNTS_LIST_URL, data=ACCOUNTS_FULL_VALID_TEST_DATA)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(member='This field may not be blank.',
                      container=response.data.get('secondary_password'))

    def test_can_create_account_with_incorrect_seat_scouts_added(self):
        """
        Checks if a new account can be successfully created with an incorrect seat_scouts_added
        Expected: False
        """

        ACCOUNTS_FULL_VALID_TEST_DATA.update({'seat_scouts_added': 'test'})
        response = self.client.post(path=ACCOUNTS_LIST_URL, data=ACCOUNTS_FULL_VALID_TEST_DATA)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(member='Must be a valid boolean.',
                      container=response.data.get('seat_scouts_added'))

    def test_can_create_account_with_incorrect_seat_scouts_status(self):
        """
        Checks if a new account can be successfully created with an incorrect seat_scouts_status
        Expected: False
        """

        ACCOUNTS_FULL_VALID_TEST_DATA.update({'seat_scouts_status': 'test'})
        response = self.client.post(path=ACCOUNTS_LIST_URL, data=ACCOUNTS_FULL_VALID_TEST_DATA)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(member='Must be a valid boolean.',
                      container=response.data.get('seat_scouts_status'))

    def test_can_create_account_with_incorrect_airfrance(self):
        """
        Checks if a new account can be successfully created with an incorrect airfrance
        Expected: False
        """

        ACCOUNTS_FULL_VALID_TEST_DATA.update({'airfrance': 'test'})
        response = self.client.post(path=ACCOUNTS_LIST_URL, data=ACCOUNTS_FULL_VALID_TEST_DATA)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(member='Must be a valid boolean.',
                      container=response.data.get('airfrance'))

    def test_can_create_account_with_empty_team(self):
        """
        Checks if a new account can be successfully created with an empty team
        Expected: False
        """

        ACCOUNTS_FULL_VALID_TEST_DATA.update({'team': ''})
        response = self.client.post(path=ACCOUNTS_LIST_URL, data=ACCOUNTS_FULL_VALID_TEST_DATA)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(member='This field may not be blank.',
                      container=response.data.get('team'))

    def test_can_create_account_with_empty_specific_team(self):
        """
        Checks if a new account can be successfully created with an empty specific_team
        Expected: False
        """

        ACCOUNTS_FULL_VALID_TEST_DATA.update({'specific_team': ''})
        response = self.client.post(path=ACCOUNTS_LIST_URL, data=ACCOUNTS_FULL_VALID_TEST_DATA)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(member='This field may not be blank.',
                      container=response.data.get('specific_team'))

    def test_can_create_account_with_empty_forward_to(self):
        """
        Checks if a new account can be successfully created with an empty forward_to
        Expected: False
        """

        ACCOUNTS_FULL_VALID_TEST_DATA.update({'forward_to': ''})
        response = self.client.post(path=ACCOUNTS_LIST_URL, data=ACCOUNTS_FULL_VALID_TEST_DATA)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(member='This field may not be blank.',
                      container=response.data.get('forward_to'))

    def test_can_create_account_with_empty_forward_email_password(self):
        """
        Checks if a new account can be successfully created with an empty forward_email_password
        Expected: False
        """

        ACCOUNTS_FULL_VALID_TEST_DATA.update({'forward_email_password': ''})
        response = self.client.post(path=ACCOUNTS_LIST_URL, data=ACCOUNTS_FULL_VALID_TEST_DATA)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(member='This field may not be blank.',
                      container=response.data.get('forward_email_password'))

    def test_can_create_account_with_incorrect_disabled(self):
        """
        Checks if a new account can be successfully created with an incorrect disabled
        Expected: False
        """

        ACCOUNTS_FULL_VALID_TEST_DATA.update({'disabled': 'test'})
        response = self.client.post(path=ACCOUNTS_LIST_URL, data=ACCOUNTS_FULL_VALID_TEST_DATA)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(member='Must be a valid boolean.',
                      container=response.data.get('disabled'))

    def test_can_create_account_with_empty_ld_computer_used(self):
        """
        Checks if a new account can be successfully created with an empty ld_computer_used
        Expected: False
        """

        ACCOUNTS_FULL_VALID_TEST_DATA.update({'ld_computer_used': ''})
        response = self.client.post(path=ACCOUNTS_LIST_URL, data=ACCOUNTS_FULL_VALID_TEST_DATA)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(member='This field may not be blank.',
                      container=response.data.get('ld_computer_used'))

    def test_can_create_account_with_incorrect_created_at(self):
        """
        Checks if a new account can be successfully created with an incorrect created_at
        Expected: False
        """

        ACCOUNTS_FULL_VALID_TEST_DATA.update({'created_at': 'test'})
        response = self.client.post(path=ACCOUNTS_LIST_URL, data=ACCOUNTS_FULL_VALID_TEST_DATA)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(member='Date has wrong format. Use one of these formats instead: YYYY-MM-DD.',
                      container=response.data.get('created_at'))

    def test_can_create_account_with_incorrect_last_opened(self):
        """
        Checks if a new account can be successfully created with an incorrect last_opened
        Expected: False
        """

        ACCOUNTS_FULL_VALID_TEST_DATA.update({'last_opened': 'test'})
        response = self.client.post(path=ACCOUNTS_LIST_URL, data=ACCOUNTS_FULL_VALID_TEST_DATA)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(member='Date has wrong format. Use one of these formats instead: YYYY-MM-DD.',
                      container=response.data.get('last_opened'))

    def test_can_create_account_with_empty_comments(self):
        """
        Checks if a new account can be successfully created with an empty comments
        Expected: False
        """

        ACCOUNTS_FULL_VALID_TEST_DATA.update({'comments': ''})
        response = self.client.post(path=ACCOUNTS_LIST_URL, data=ACCOUNTS_FULL_VALID_TEST_DATA)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(member='This field may not be blank.',
                      container=response.data.get('comments'))

    def test_can_create_account_with_incorrect_created_by(self):
        """
        Checks if a new account can be successfully created with an incorrect created_by
        Expected: False
        """

        ACCOUNTS_FULL_VALID_TEST_DATA.update({'created_by': 'test'})
        response = self.client.post(path=ACCOUNTS_LIST_URL, data=ACCOUNTS_FULL_VALID_TEST_DATA)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(member='Incorrect type. Expected pk value, received str.',
                      container=response.data.get('created_by'))

        ACCOUNTS_FULL_VALID_TEST_DATA.update({'created_by': 12344})
        response = self.client.post(path=ACCOUNTS_LIST_URL, data=ACCOUNTS_FULL_VALID_TEST_DATA)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(member='Invalid pk "12344" - object does not exist.',
                      container=response.data.get('created_by'))

    def test_can_create_account_with_empty_created_by(self):
        """
        Checks if a new account can be successfully created with an empty created_by
        Expected: True
        """

        ACCOUNTS_FULL_VALID_TEST_DATA_COPY.update({'created_by': ''})
        response = self.client.post(path=ACCOUNTS_LIST_URL, data=ACCOUNTS_FULL_VALID_TEST_DATA_COPY)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_can_create_account_with_incorrect_edited_by(self):
        """
        Checks if a new account can be successfully created with an incorrect edited_by
        Expected: False
        """

        ACCOUNTS_FULL_VALID_TEST_DATA.update({'edited_by': 'test'})
        response = self.client.post(path=ACCOUNTS_LIST_URL, data=ACCOUNTS_FULL_VALID_TEST_DATA)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(member='Incorrect type. Expected pk value, received str.',
                      container=response.data.get('edited_by'))

        ACCOUNTS_FULL_VALID_TEST_DATA.update({'edited_by': 12344})
        response = self.client.post(path=ACCOUNTS_LIST_URL, data=ACCOUNTS_FULL_VALID_TEST_DATA)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(member='Invalid pk "12344" - object does not exist.',
                      container=response.data.get('edited_by'))

    def test_can_create_account_with_empty_edited_by(self):
        """
        Checks if a new account can be successfully created with an empty edited_by
        Expected: True
        """

        ACCOUNTS_FULL_VALID_TEST_DATA_COPY.update({'edited_by': ''})
        response = self.client.post(path=ACCOUNTS_LIST_URL, data=ACCOUNTS_FULL_VALID_TEST_DATA_COPY)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_can_create_account_with_empty_phone(self):
        """
        Checks if a new account can be successfully created with an empty phone
        Expected: False
        """

        ACCOUNTS_FULL_VALID_TEST_DATA.update({'phone': ''})
        response = self.client.post(path=ACCOUNTS_LIST_URL, data=ACCOUNTS_FULL_VALID_TEST_DATA)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(member='This field may not be blank.',
                      container=response.data.get('phone'))

    def test_can_create_account_with_empty_tickets_com_password(self):
        """
        Checks if a new account can be successfully created with an empty tickets_com_password
        Expected: False
        """

        ACCOUNTS_FULL_VALID_TEST_DATA.update({'tickets_com_password': ''})
        response = self.client.post(path=ACCOUNTS_LIST_URL, data=ACCOUNTS_FULL_VALID_TEST_DATA)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(member='This field may not be blank.',
                      container=response.data.get('tickets_com_password'))

    def test_can_create_account_with_incorrect_password_reset(self):
        """
        Checks if a new account can be successfully created with an incorrect password_reset
        Expected: False
        """

        ACCOUNTS_FULL_VALID_TEST_DATA.update({'password_reset': 'test'})
        response = self.client.post(path=ACCOUNTS_LIST_URL, data=ACCOUNTS_FULL_VALID_TEST_DATA)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(member='Must be a valid boolean.',
                      container=response.data.get('password_reset'))

    def test_can_create_account_with_incorrect_active_tickets_inside(self):
        """
        Checks if a new account can be successfully created with an incorrect active_tickets_inside
        Expected: False
        """

        ACCOUNTS_FULL_VALID_TEST_DATA.update({'active_tickets_inside': 'test'})
        response = self.client.post(path=ACCOUNTS_LIST_URL, data=ACCOUNTS_FULL_VALID_TEST_DATA)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(member='Must be a valid boolean.',
                      container=response.data.get('active_tickets_inside'))

    def test_can_create_account_with_empty_migrated_from(self):
        """
        Checks if a new account can be successfully created with an empty migrated_from
        Expected: False
        """

        ACCOUNTS_FULL_VALID_TEST_DATA.update({'migrated_from': ''})
        response = self.client.post(path=ACCOUNTS_LIST_URL, data=ACCOUNTS_FULL_VALID_TEST_DATA)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(member='This field may not be blank.',
                      container=response.data.get('migrated_from'))

    def test_can_create_account_with_empty_migrated_to(self):
        """
        Checks if a new account can be successfully created with an empty migrated_to
        Expected: False
        """

        ACCOUNTS_FULL_VALID_TEST_DATA.update({'migrated_to': ''})
        response = self.client.post(path=ACCOUNTS_LIST_URL, data=ACCOUNTS_FULL_VALID_TEST_DATA)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(member='This field may not be blank.',
                      container=response.data.get('migrated_to'))

    def test_can_create_account_with_not_existing_fields_passed(self):
        """
        An account can be created if we pass fields that aren't defined in Accounts model,
        but that incorrect data will not be considered upon creating an account.
        Only valid data will be considered upon creation.
        Expected: True
        """

        ACCOUNTS_FULL_VALID_TEST_DATA_COPY.update({'test_field': 'test'})
        response = self.client.post(path=ACCOUNTS_LIST_URL, data=ACCOUNTS_FULL_VALID_TEST_DATA_COPY)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertFalse(response.data.get('test_field', False))


class ReadAccountTest(AccountsTest):
    """
    Children class that contains all necessary methods to test
    if account list and account instance can be READ
    """

    def setUp(self):
        super().setUp()

    def test_can_read_accounts_list(self):
        """
        Checks if all accounts list can be received by a user who has rights to see them
        Expected: True
        """

        response = self.client.get(path=ACCOUNTS_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_read_account_detail(self):
        """
        Checks if particular account detail can be received by a user who has rights to see it
        Expected: True
        """

        response = self.client.get(path=ACCOUNT_DETAIL_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Accounts.objects.get(pk=1).email,
                         ACCOUNTS_FULL_VALID_REAL_DATA.get('email'))


class UpdateAccountTest(AccountsTest):
    """
    Children class that contains all necessary methods to test
    if account can be UPDATED and PARTIALLY UPDATED
    """

    def setUp(self):
        super().setUp()

    def test_can_partial_update_account(self):
        """
        Checks if particular account instance can be partially updated
        Expected: True
        """

        data_to_update = {'email': 'PARTIALLY_UPDATED@test.com'}
        response = self.client.patch(path=ACCOUNT_DETAIL_URL, data=data_to_update)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Accounts.objects.get(pk=1).email,
                         data_to_update.get('email'))

    def test_can_update_account(self):
        """
        Checks if particular account instance can be updated
        Expected: True
        """

        data_to_update = ACCOUNTS_FULL_VALID_REAL_DATA
        data_to_update.update({'email': 'UPDATED@test.com'})
        response = self.client.put(path=ACCOUNT_DETAIL_URL, data=data_to_update)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Accounts.objects.get(pk=1).email,
                         data_to_update.get('email'))

    def test_can_update_all_account_fields(self):
        """
        Checks if particular account instance can be completely updated
        with almost all available fields
        Expected: True
        """

        response = self.client.put(path=ACCOUNT_DETAIL_URL, data=ACCOUNTS_FULL_VALID_TEST_DATA_COPY)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Accounts.objects.get(pk=1).email,
                         ACCOUNTS_FULL_VALID_TEST_DATA_COPY.get('email'))


class DeleteAccountTest(AccountsTest):
    """
    Children class that contains all necessary methods to test
    if account can be DELETED
    """

    def setUp(self):
        super().setUp()

    def test_can_delete_account(self):
        """
        Checks if an account can be deleted
        Expected: True
        """

        response = self.client.delete(path=ACCOUNT_DETAIL_URL)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Accounts.objects.all().count(), 0)
