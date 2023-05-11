from rest_framework.status import HTTP_200_OK
from rest_framework.test import APITestCase

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import tag

from apps.accounts.models import Accounts
from apps.accounts.tests.settings import ACCOUNTS_LIST_URL


@tag('accounts', 'authenticated', 'authorized', 'filters')
class AccountsTest(APITestCase):
    """
    Account parent test class that inherits from APITestCase and has 'setUp' method
    that children classes can use without repetition
    """

    @classmethod
    def setUpTestData(cls):
        call_command(
            'loaddata', 'apps/accounts/tests/fixtures/fake_accounts_fixture.json'
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
        self.assertEqual(Accounts.objects.count(), 21)
        self.assertEqual(get_user_model().objects.count(), 1)


class SearchAccountTest(AccountsTest):
    """
    Children class that contains all necessary methods to test
    if account search lookup is working correctly
    """

    def setUp(self):
        super().setUp()

    def test_can_read_accounts_list(self):
        """
        Checks if all accounts list can be received by a user who has rights to see them
        Expected: True
        """
        response = self.client.get(path=ACCOUNTS_LIST_URL)

        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_can_search_accounts(self):
        """
        Checks if accounts can be searched by a user who has rights to do so
        Example: %VALUE%
        Expected: HTTP_200_OK
        """
        response = self.client.get(path=f'{ACCOUNTS_LIST_URL}?search=ichardharve')

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertTrue('ichardharve' in str(response.data))

    def test_search_accounts_not_found(self):
        """
        Checks if searching for non-existent accounts returns an empty result
        Expected: HTTP_200_OK and empty result
        """
        response = self.client.get(
            path=f'{ACCOUNTS_LIST_URL}?search=non_existent_account'
        )

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(response.data.get('results')), 0)


class FilterAccountTest(AccountsTest):
    """
    Children class that contains all necessary methods to test
    if account filters lookups are working correctly
    """

    def setUp(self):
        super().setUp()

    def test_can_filter_accounts_by_first_name_exact(self):
        """
        Checks if accounts can be filtered by first_name exact lookup
        Example: first_name=<FIRST_NAME>
        Expected: HTTP_200_OK
        """
        response = self.client.get(path=f'{ACCOUNTS_LIST_URL}?first_name=Carolyn')

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertTrue('Carolyn' in str(response.data))

    def test_can_filter_accounts_by_last_name_exact(self):
        """
        Checks if accounts can be filtered by last_name exact lookup
        Example: last_name=<LAST_NAME>
        Expected: HTTP_200_OK
        """
        response = self.client.get(path=f'{ACCOUNTS_LIST_URL}?last_name=Nichols')

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertTrue('Nichols' in str(response.data))

    def test_can_filter_accounts_by_email_icontains(self):
        """
        Checks if accounts can be filtered by email icontains lookup
        Example: email__icontains=<EMAIL>
        Expected: HTTP_200_OK
        """
        response = self.client.get(
            path=f'{ACCOUNTS_LIST_URL}?email__icontains=ichardharve'
        )

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertTrue('ichardharve' in str(response.data))

    def test_can_filter_accounts_by_type_exact(self):
        """
        Checks if accounts can be filtered by type exact lookup
        Example: type=<TYPE>
        Expected: HTTP_200_OK
        """
        response = self.client.get(path=f'{ACCOUNTS_LIST_URL}?type=test')

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertTrue('test' in str(response.data))

    def test_can_filter_accounts_by_password_exact(self):
        """
        Checks if accounts can be filtered by password exact lookup
        Example: password=<PASSWORD>
        Expected: HTTP_200_OK
        """
        response = self.client.get(path=f'{ACCOUNTS_LIST_URL}?password=password123')

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertTrue('password123' in str(response.data))

    def test_can_filter_accounts_by_recovery_email_icontains(self):
        """
        Checks if accounts can be filtered by recovery_email icontains lookup
        Example: recovery_email__icontains=<RECOVERY_EMAIL>
        Expected: HTTP_200_OK
        """
        response = self.client.get(
            path=f'{ACCOUNTS_LIST_URL}?recovery_email__icontains=esswend'
        )

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertTrue('esswend' in str(response.data))

    def test_can_filter_accounts_by_email_forwarding_exact(self):
        """
        Checks if accounts can be filtered by email_forwarding exact lookup
        Example: email_forwarding=<TRUE/FALSE>
        Expected: HTTP_200_OK, but only 1 result if email_forwarding=true
        """
        response = self.client.get(path=f'{ACCOUNTS_LIST_URL}?email_forwarding=true')

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(response.data.get('results')), 1)

    def test_can_filter_accounts_by_auto_po_seats_scouts_exact(self):
        """
        Checks if accounts can be filtered by auto_po_seats_scouts exact lookup
        Example: auto_po_seats_scouts=<TRUE/FALSE>
        Expected: HTTP_200_OK, but only 1 result if auto_po_seats_scouts=true
        """
        response = self.client.get(
            path=f'{ACCOUNTS_LIST_URL}?auto_po_seats_scouts=true'
        )

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(response.data.get('results')), 1)

    def test_can_filter_accounts_by_errors_failed_icontains(self):
        """
        Checks if accounts can be filtered by errors_failed icontains lookup
        Example: errors_failed__icontains=<ERRORS_FAILED>
        Expected: HTTP_200_OK
        """
        response = self.client.get(
            path=f'{ACCOUNTS_LIST_URL}?errors_failed__icontains=TEST ERROR'
        )

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(response.data.get('results')), 1)
        self.assertTrue('TEST ERROR' in str(response.data))

    def test_can_filter_accounts_by_seat_scouts_added_exact(self):
        """
        Checks if accounts can be filtered by seat_scouts_added exact lookup
        Example: seat_scouts_added=<TRUE/FALSE>
        Expected: HTTP_200_OK, but only 1 result if seat_scouts_added=true
        """
        response = self.client.get(path=f'{ACCOUNTS_LIST_URL}?seat_scouts_added=true')

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(response.data.get('results')), 1)

    def test_can_filter_accounts_by_seat_scouts_status_exact(self):
        """
        Checks if accounts can be filtered by seat_scouts_status exact lookup
        Example: seat_scouts_status=<TRUE/FALSE>
        Expected: HTTP_200_OK, but only 1 result if seat_scouts_status=true
        """
        response = self.client.get(path=f'{ACCOUNTS_LIST_URL}?seat_scouts_status=true')

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(response.data.get('results')), 1)

    def test_can_filter_accounts_by_team_exact(self):
        """
        Checks if accounts can be filtered by team exact lookup
        Example: team=<TEAM>
        Expected: HTTP_200_OK
        """
        response = self.client.get(path=f'{ACCOUNTS_LIST_URL}?team=TEST_TEAM')

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(response.data.get('results')), 1)
        self.assertTrue('TEST_TEAM' in str(response.data))

    def test_can_filter_accounts_by_specific_team_icontains(self):
        """
        Checks if accounts can be filtered by specific_team icontains lookup
        Example: specific_team__icontains=<SPECIFIC_TEAM>
        Expected: HTTP_200_OK
        """
        response = self.client.get(
            path=f'{ACCOUNTS_LIST_URL}?specific_team__icontains=TEST_SPECIFIC_TEAM'
        )

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(response.data.get('results')), 1)
        self.assertTrue('TEST_SPECIFIC_TEAM' in str(response.data))

    def test_can_filter_accounts_by_forward_to_icontains(self):
        """
        Checks if accounts can be filtered by forward_to icontains lookup
        Example: forward_to__icontains=<FORWARD_TO_EMAIL>
        Expected: HTTP_200_OK
        """
        response = self.client.get(
            path=f'{ACCOUNTS_LIST_URL}?forward_to__icontains=TEST_FORWARD_TO_EMAIL'
        )

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(response.data.get('results')), 1)
        self.assertTrue('TEST_FORWARD_TO_EMAIL' in str(response.data))

    def test_can_filter_accounts_by_forward_email_password_exact(self):
        """
        Checks if accounts can be filtered by forward_email_password exact lookup
        Example: forward_email_password=<FORWARD_EMAIL_PASSWORD>
        Expected: HTTP_200_OK
        """
        response = self.client.get(
            path=f'{ACCOUNTS_LIST_URL}?forward_email_password=FORWARD_EMAIL_PASSWORD'
        )

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(response.data.get('results')), 1)
        self.assertTrue('FORWARD_EMAIL_PASSWORD' in str(response.data))

    def test_can_filter_accounts_by_disabled_exact(self):
        """
        Checks if accounts can be filtered by disabled exact lookup
        Example: disabled=<TRUE/FALSE>
        Expected: HTTP_200_OK, but only 1 result if disabled=true
        """
        response = self.client.get(path=f'{ACCOUNTS_LIST_URL}?disabled=true')

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(response.data.get('results')), 1)

    def test_can_filter_accounts_by_ld_computer_used_exact(self):
        """
        Checks if accounts can be filtered by ld_computer_used exact lookup
        Example: ld_computer_used=<LD_COMPUTER_USED>
        Expected: HTTP_200_OK
        """
        response = self.client.get(
            path=f'{ACCOUNTS_LIST_URL}?ld_computer_used=LD_COMPUTER_USED'
        )

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(response.data.get('results')), 1)
        self.assertTrue('LD_COMPUTER_USED' in str(response.data))

    def test_can_filter_accounts_by_last_opened_exact(self):
        """
        Checks if accounts can be filtered by last_opened exact lookup
        Example: last_opened=<YYYY-MM-DD>
        Expected: HTTP_200_OK
        """
        response = self.client.get(path=f'{ACCOUNTS_LIST_URL}?last_opened=2023-05-11')

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(response.data.get('results')), 1)
        self.assertTrue('2023-05-11' in str(response.data))

    def test_can_filter_accounts_by_comments_icontains(self):
        """
        Checks if accounts can be filtered by comments icontains lookup
        Example: comments__icontains=<COMMENT>
        Expected: HTTP_200_OK
        """
        response = self.client.get(
            path=f'{ACCOUNTS_LIST_URL}?comments__icontains=EST_COMMEN'
        )

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(response.data.get('results')), 1)
        self.assertTrue('EST_COMMEN' in str(response.data))

    def test_can_filter_accounts_by_tm_created_exact(self):
        """
        Checks if accounts can be filtered by tm_created exact lookup
        Example: tm_created=<TRUE/FALSE>
        Expected: HTTP_200_OK, but only 1 result if tm_created=true
        """
        response = self.client.get(path=f'{ACCOUNTS_LIST_URL}?tm_created=true')

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(response.data.get('results')), 1)

    def test_can_filter_accounts_by_axs_created_exact(self):
        """
        Checks if accounts can be filtered by axs_created exact lookup
        Example: axs_created=<TRUE/FALSE>
        Expected: HTTP_200_OK, but only 1 result if axs_created=true
        """
        response = self.client.get(path=f'{ACCOUNTS_LIST_URL}?axs_created=true')

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(response.data.get('results')), 1)

    def test_can_filter_accounts_by_eventbrite_exact(self):
        """
        Checks if accounts can be filtered by eventbrite exact lookup
        Example: eventbrite=<TRUE/FALSE>
        Expected: HTTP_200_OK, but only 1 result if eventbrite=true
        """
        response = self.client.get(path=f'{ACCOUNTS_LIST_URL}?eventbrite=true')

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(response.data.get('results')), 1)

    def test_can_filter_accounts_by_etix_exact(self):
        """
        Checks if accounts can be filtered by etix exact lookup
        Example: etix=<TRUE/FALSE>
        Expected: HTTP_200_OK, but only 1 result if etix=true
        """
        response = self.client.get(path=f'{ACCOUNTS_LIST_URL}?etix=true')

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(response.data.get('results')), 1)

    def test_can_filter_accounts_by_ticket_web_exact(self):
        """
        Checks if accounts can be filtered by ticket_web exact lookup
        Example: ticket_web=<TRUE/FALSE>
        Expected: HTTP_200_OK, but only 1 result if ticket_web=true
        """
        response = self.client.get(path=f'{ACCOUNTS_LIST_URL}?ticket_web=true')

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(response.data.get('results')), 1)

    def test_can_filter_accounts_by_big_tickets_exact(self):
        """
        Checks if accounts can be filtered by big_tickets exact lookup
        Example: big_tickets=<TRUE/FALSE>
        Expected: HTTP_200_OK, but only 1 result if big_tickets=true
        """
        response = self.client.get(path=f'{ACCOUNTS_LIST_URL}?big_tickets=true')

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(response.data.get('results')), 1)

    def test_can_filter_accounts_by_amazon_exact(self):
        """
        Checks if accounts can be filtered by amazon exact lookup
        Example: amazon=<TRUE/FALSE>
        Expected: HTTP_200_OK, but only 1 result if amazon=true
        """
        response = self.client.get(path=f'{ACCOUNTS_LIST_URL}?amazon=true')

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(response.data.get('results')), 1)

    def test_can_filter_accounts_by_delta_created_exact(self):
        """
        Checks if accounts can be filtered by delta_created exact lookup
        Example: delta_created=<TRUE/FALSE>
        Expected: HTTP_200_OK, but only 1 result if delta_created=true
        """
        response = self.client.get(path=f'{ACCOUNTS_LIST_URL}?delta_created=true')

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(response.data.get('results')), 1)

    def test_can_filter_accounts_by_air_france_created_exact(self):
        """
        Checks if accounts can be filtered by air_france_created exact lookup
        Example: air_france_created=<TRUE/FALSE>
        Expected: HTTP_200_OK, but only 1 result if air_france_created=true
        """
        response = self.client.get(path=f'{ACCOUNTS_LIST_URL}?air_france_created=true')

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(response.data.get('results')), 1)

    def test_can_filter_accounts_by_aeromexico_created_exact(self):
        """
        Checks if accounts can be filtered by aeromexico_created exact lookup
        Example: aeromexico_created=<TRUE/FALSE>
        Expected: HTTP_200_OK, but only 1 result if aeromexico_created=true
        """
        response = self.client.get(path=f'{ACCOUNTS_LIST_URL}?aeromexico_created=true')

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(response.data.get('results')), 1)

    def test_can_filter_accounts_by_avianca_created_exact(self):
        """
        Checks if accounts can be filtered by avianca_created exact lookup
        Example: avianca_created=<TRUE/FALSE>
        Expected: HTTP_200_OK, but only 1 result if avianca_created=true
        """
        response = self.client.get(path=f'{ACCOUNTS_LIST_URL}?avianca_created=true')

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(response.data.get('results')), 1)

    def test_can_filter_accounts_by_korean_air_created_exact(self):
        """
        Checks if accounts can be filtered by korean_air_created exact lookup
        Example: korean_air_created=<TRUE/FALSE>
        Expected: HTTP_200_OK, but only 1 result if korean_air_created=true
        """
        response = self.client.get(path=f'{ACCOUNTS_LIST_URL}?korean_air_created=true')

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(response.data.get('results')), 1)

    def test_can_filter_accounts_by_china_airlines_created_exact(self):
        """
        Checks if accounts can be filtered by china_airlines_created exact lookup
        Example: china_airlines_created=<TRUE/FALSE>
        Expected: HTTP_200_OK, but only 1 result if china_airlines_created=true
        """
        response = self.client.get(
            path=f'{ACCOUNTS_LIST_URL}?china_airlines_created=true'
        )

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(response.data.get('results')), 1)
