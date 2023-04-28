import pandas as pd

path_to_save = 'prepared_accounts/'

# ================================= READING CSV FILE ======================================
path_to_read = '/Users/samoylovartem/Documents/Data migration/500 aged hotmail.csv'
df = pd.read_csv(path_to_read, sep=',', keep_default_na=False)


df.rename(
    columns={
        'Email': 'email',
        'Password': 'password',
        'TM password': 'tm_password',
        'Forwarding email': 'forward_to',
    },
    inplace=True,
)

keys_to_add = {
    "first_name": "NA",
    "last_name": "NA",
    "type": "TMVERIFIEDACCOUNT",
    "delta_miles": "NA",
    "flyingblue_miles": "NA",
    "delta_created": False,
    "delta_password": "NA",
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
    "recovery_email": "na@na.com",
    "email_forwarding": True,
    "auto_po_seats_scouts": False,
    "errors_failed": "NA",
    "tm_created": True,
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
    "team": "TMVERIFIED",
    "specific_team": "NA",
    "forward_email_password": "NA",
    "seat_scouts_password": "NA",
    "password_matching": False,
    "disabled": False,
    "created_by": "Muhammad Mateen",
    "edited_by": "Muhammad Mateen",
    "ld_computer_used": "NA",
    "created_at": "2023-04-27",
    "last_opened": "2023-04-27",
    "comments": "500 TM verified accounts",
    "phone": "NA",
    "tickets_com_password": "NA",
    "password_reset": True,
    "active_tickets_inside": False,
    "migrated_from": "NA",
    "migrated_to": "NA",
}

# add the missing columns with default values
df = df.assign(**keys_to_add)

# update the recovery_email column
df['recovery_email'] = df['forward_to']


df.to_csv(path_to_save + '500 accounts.csv', index=False)
