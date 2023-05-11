import json

from faker import Faker

fake = Faker()

path_to_save = 'apps/accounts/tests/fixtures/'

accounts = []

for i in range(1, 22):
    account = {
        "model": "accounts.accounts",
        "pk": i,
        "fields": {
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": fake.email(),
            "type": "test",
            "password": "password123",
            "delta_created": False,
            "delta_password": "NA",
            "delta_miles": "NA",
            "flyingblue_miles": "NA",
            "air_france_created": False,
            "air_france_password": "NA",
            "aeromexico_created": False,
            "aeromexico_password": "NA",
            "avianca_created": False,
            "avianca_password": "NA",
            "korean_air_created": False,
            "korean_air_password": "NA",
            "china_airlines_created": False,
            "china_airlines_password": "NA",
            "recovery_email": fake.email(),
            "email_forwarding": False,
            "auto_po_seats_scouts": False,
            "errors_failed": "NA",
            "tm_created": False,
            "tm_password": "NA",
            "tm_address": "NA",
            "axs_created": False,
            "axs_password": "NA",
            "sg_created": False,
            "sg_password": "NA",
            "tickets_com_created": False,
            "facebook_created": False,
            "twitter_created": False,
            "eventbrite": False,
            "etix": False,
            "ticket_web": False,
            "big_tickets": False,
            "amazon": False,
            "secondary_password": "NA",
            "seat_scouts_added": False,
            "seat_scouts_status": False,
            "team": "NA",
            "specific_team": "NA",
            "forward_to": "NA",
            "forward_email_password": "NA",
            "seat_scouts_password": "NA",
            "password_matching": False,
            "disabled": False,
            "created_by": "MATEEN",
            "edited_by": "NA",
            "ld_computer_used": "NA",
            "created_at": "2023-05-07",
            "updated_at": "2023-05-07T00:00:00Z",
            "last_opened": "2023-05-07",
            "comments": "NA",
            "phone": "NA",
            "tickets_com_password": "NA",
            "password_reset": False,
            "active_tickets_inside": False,
            "migrated_from": "NA",
            "migrated_to": "NA",
        },
    }

    accounts.append(account)

with open('fake_accounts_fixture.json', 'w') as f:
    json.dump(accounts, f, indent=4)
