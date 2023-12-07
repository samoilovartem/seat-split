import csv
import json

JSON_FILE_PATH = 'json_source_files/NHL2023-2024.json'
CSV_OUTPUT_FILENAME = 'NHL20232024.csv'

with open(JSON_FILE_PATH, 'r') as json_file:
    data = json.load(json_file)

rows = data['rows']


fieldnames = [
    'id',
    'name',
    'date',
    'venue_id',
    'venue_name',
    'venue_address',
    'venue_city',
    'venue_state',
    'venue_country',
    'venue_postalCode',
    'venue_phone',
    'venue_timeZone',
    'performerId',
    'performer',
    'keywords',
    'chartUrl',
    'stubhubEventId',
    'stubhubEventUrl',
    'tags',
    'notes',
    'eiEventId',
    'optOutReplenishment',
    'ticketCount',
    'mySoldTickets',
    'myCancelledTickets',
    'disabled',
    'quantity',
    'cost',
    'lastPriceUpdate',
    'listingCount',
    'vividSeatsEventUrl',
]

with open(CSV_OUTPUT_FILENAME, 'w', newline='') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    writer.writeheader()

    for row in rows:
        venue = row.pop('venue', {})
        row['venue_id'] = venue.get('id')
        row['venue_name'] = venue.get('name')
        row['venue_address'] = venue.get('address')
        row['venue_city'] = venue.get('city')
        row['venue_state'] = venue.get('state')
        row['venue_country'] = venue.get('country')
        row['venue_postalCode'] = venue.get('postalCode')
        row['venue_phone'] = venue.get('phone')
        row['venue_timeZone'] = venue.get('timeZone')

        writer.writerow(row)

print(f'Data has been written to {CSV_OUTPUT_FILENAME}')
