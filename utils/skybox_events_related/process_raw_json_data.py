import json
import re
from uuid import UUID

import pandas as pd
import pytz
from loguru import logger


def replace_values_in_column(df, column_name, old_value_regex, new_value):
    """
    Function to replace instances of an old value with a new value in a specific DataFrame column.
    """
    df[column_name] = df[column_name].apply(
        lambda x: re.sub(old_value_regex, new_value, x, flags=re.IGNORECASE)
    )
    return df


def convert_to_timezone_aware_and_remove_timezone_column(df, date_time_col, timezone_col):
    """Function to convert a DataFrame's date_time column to timezone-aware datetime objects."""
    df[date_time_col] = pd.to_datetime(df[date_time_col])

    def apply_timezone(row):
        tz = pytz.timezone(row[timezone_col])
        return tz.localize(row[date_time_col])

    df[date_time_col] = df.apply(apply_timezone, axis=1)

    df.drop(columns=[timezone_col], inplace=True)

    return df


def clean_name(name):
    """Function to clean the 'name' column in a DataFrame."""
    name = re.sub(r'\s+', ' ', name)
    match = re.search(r'(.+? - )?(.+ at .+?)(?=\s+\(|$)', name)
    if match:
        return match.group(2).strip()
    return name


def extract_additional_info(name):
    """Function to extract additional information from the 'name' column in a DataFrame."""
    additional_info = []

    prefix_match = re.search(r'^(.+?) - ', name)
    if prefix_match:
        additional_info.append(prefix_match.group(1))

    parentheses_matches = re.findall(r'\((.+?)\)', name)
    additional_info.extend(parentheses_matches)
    return ', '.join(additional_info)


JSON_FILE_PATH = 'json_source_files/MLB_2024_raw_data.json'
CSV_OUTPUT_FILENAME = 'MLB2024_cleaned_raw.csv'

SEASON = UUID('5845102f-99d4-48fb-ba8f-30d8c2799326')
LEAGUE = 'MLB'
REPLACEMENTS = {
    'name': {
        r'\bSt Louis Cardinals\b': 'St. Louis Cardinals',
    }
}

with open(JSON_FILE_PATH, 'r') as json_file:
    data = json.load(json_file)

rows = data['rows']

data_list = []
for row in rows:
    data_list.append(
        {
            'skybox_event_id': row['id'],
            'name': row['name'],
            'date_time': row['date'],
            'skybox_venue_id': row['venue']['id'],
            'skybox_venue_timezone': row['venue']['timeZone'],
            'stubhub_event_url': row['stubhubEventUrl'],
        }
    )

df = pd.DataFrame(data_list)

df['additional_info'] = df['name'].apply(extract_additional_info)
df['name'] = df['name'].apply(clean_name)

df['season'] = SEASON
df['league'] = LEAGUE

df = convert_to_timezone_aware_and_remove_timezone_column(df, 'date_time', 'skybox_venue_timezone')

if REPLACEMENTS:
    for column_name, replacement_dict in REPLACEMENTS.items():
        for old_value, new_value in replacement_dict.items():
            df = replace_values_in_column(df, column_name, old_value, new_value)

df.to_csv(CSV_OUTPUT_FILENAME, index=False)

logger.info('Data has been written to {}', CSV_OUTPUT_FILENAME)
