import csv
import json

from loguru import logger

JSON_FILE_PATH = 'json_source_files/MLB_2024_raw_data.json'
CSV_OUTPUT_FILENAME = 'MLB2024_raw.csv'

with open(JSON_FILE_PATH, 'r') as json_file:
    data = json.load(json_file)

rows = data['rows']

fieldnames = [
    'skybox_event_id',
    'name',
    'date_time',
    'skybox_venue_id',
    'skybox_venue_timezone',
    'stubhub_event_url',
]

with open(CSV_OUTPUT_FILENAME, 'w', newline='') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    writer.writeheader()

    for row in rows:
        csv_row = {
            'skybox_event_id': row['id'],
            'name': row['name'],
            'date_time': row['date'],
            'skybox_venue_id': row['venue']['id'],
            'skybox_venue_timezone': row['venue']['timeZone'],
            'stubhub_event_url': row['stubhubEventUrl'],
        }

        writer.writerow(csv_row)

logger.info('Data has been written to {}', CSV_OUTPUT_FILENAME)
