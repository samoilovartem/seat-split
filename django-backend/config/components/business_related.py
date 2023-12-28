import os

BUSINESS_TOTAL_EXPENSES = float(os.environ.get('BUSINESS_TOTAL_EXPENSES', 0.2))
EXPENSES_MULTIPLIER = 1 - BUSINESS_TOTAL_EXPENSES

GITHUB_ACCESS_TOKEN = os.environ.get('GITHUB_ACCESS_TOKEN', '')

LISTING_STATUSES = [
    ('Pending', 'Pending'),
    ('Listed', 'Listed'),
    ('Requested for delisting', 'Requested for delisting'),
    ('Sold', 'Sold'),
    ('Delisted', 'Delisted'),
]

DELIVERY_STATUSES = [
    ('Pending', 'Pending'),
    ('Complete', 'Complete'),
]

MARKETPLACES = [
    ('Event Inventory', 'Event Inventory'),
    ('StubHub', 'StubHub'),
    ('Mercury', 'Mercury'),
    ('SeatGeek', 'SeatGeek'),
    ('VividSeats', 'VividSeats'),
    ('TicketNetwork', 'TicketNetwork'),
    ('Viagogo', 'Viagogo'),
    ('Ticket Evolution', 'Ticket Evolution'),
    ('TickPick', 'TickPick'),
    ('Gametime', 'Gametime'),
]

SUPPORTED_LEAGUES = ['NFL', 'NBA', 'NHL', 'MLB', 'MLS']

STT_STAFF_GROUP_NAME = 'STT Staff'
STT_STAFF_GROUP_PERMISSIONS = [
    'view_ticketholder',
    'change_ticketholder',
    'change_ticket',
    'view_ticket',
    'view_teamevent',
    'add_purchase',
    'change_purchase',
    'view_purchase',
    'view_event',
    'change_team',
    'view_team',
    'change_ticketholderteam',
    'view_ticketholderteam',
    'add_season',
    'change_season',
    'view_season',
    'view_venue',
    'view_inquiry',
]
