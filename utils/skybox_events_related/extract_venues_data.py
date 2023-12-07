import csv

INPUT_CSV_FILENAME = 'NHL20232024.csv'
OUTPUT_CSV_FILENAME = 'unique_nhl_venues.csv'

unique_venues = {}

with open(INPUT_CSV_FILENAME, 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        venue_id = row['venue_id']
        if venue_id and venue_id not in unique_venues:
            unique_venues[venue_id] = {
                'skybox_venue_id': venue_id,
                'name': row['venue_name'],
                'address': row['venue_address'],
                'city': row['venue_city'],
                'state': row['venue_state'],
                'postal_code': row['venue_postalCode'],
                'country': row['venue_country'],
                'timezone': row['venue_timeZone'],
                'phone': row['venue_phone'],
            }


venue_fieldnames = [
    'skybox_venue_id',
    'name',
    'address',
    'city',
    'state',
    'postal_code',
    'country',
    'timezone',
    'phone',
]

with open(OUTPUT_CSV_FILENAME, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=venue_fieldnames)

    writer.writeheader()

    for venue in unique_venues.values():
        writer.writerow(venue)

print(f'Unique venues have been written to {OUTPUT_CSV_FILENAME}')
