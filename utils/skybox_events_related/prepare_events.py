import re

import pandas as pd
import pytz


def convert_to_timezone_aware_and_remove_timezone_column(
    df, date_time_col, timezone_col
):
    """Function to convert a DataFrame's date_time column to timezone-aware datetime objects."""
    df[date_time_col] = pd.to_datetime(df[date_time_col])

    def apply_timezone(row):
        tz = pytz.timezone(row[timezone_col])
        return tz.localize(row[date_time_col])

    df[date_time_col] = df.apply(apply_timezone, axis=1)

    df.drop(columns=[timezone_col], inplace=True)

    return df


def clean_and_rename_columns(csv_file_path, season_value, league_value):
    """Function to clean and rename columns in a DataFrame."""

    df = pd.read_csv(csv_file_path)

    df['additional_info'] = df['name'].apply(extract_additional_info)
    df['name'] = df['name'].apply(clean_name)

    df = df[
        [
            'id',
            'name',
            'date',
            'venue_id',
            'venue_timeZone',
            'stubhubEventUrl',
            'additional_info',
        ]
    ]

    df.rename(
        columns={
            'id': 'skybox_event_id',
            'date': 'date_time',
            'venue_id': 'skybox_venue_id',
            'venue_timeZone': 'venue_timezone',
            'stubhubEventUrl': 'stubhub_event_url',
        },
        inplace=True,
    )

    df['season'] = season_value
    df['league'] = league_value

    df = convert_to_timezone_aware_and_remove_timezone_column(
        df, 'date_time', 'venue_timezone'
    )

    return df


def clean_name(name):
    """Function to clean the 'name' column in a DataFrame."""

    # Normalize the whitespace by replacing sequences of whitespace characters with a single space
    name = re.sub(r'\s+', ' ', name)

    # Find all occurrences of the pattern "Team1 at Team2"
    match = re.search(r'(.+? - )?(.+ at .+?)(?=\s+\(|$)', name)
    if match:
        return match.group(2).strip()
    return name


def extract_additional_info(name):
    """Function to extract additional information from the 'name' column in a DataFrame."""
    additional_info = []

    # Find any leading text before " - " and add it to additional_info list
    prefix_match = re.search(r'^(.+?) - ', name)
    if prefix_match:
        additional_info.append(prefix_match.group(1))

    # Find any text within parentheses and add it to additional_info list
    parentheses_matches = re.findall(r'\((.+?)\)', name)
    additional_info.extend(parentheses_matches)
    return ', '.join(additional_info)


SEASON = '2024'
LEAGUE = 'MLB'

INPUT_CSV_FILE_PATH = 'MLB2024.csv'
OUTPUT_CSV_FILE_PATH = f'{INPUT_CSV_FILE_PATH.split(".")[0]}_cleaned.csv'
cleaned_df = clean_and_rename_columns(INPUT_CSV_FILE_PATH, SEASON, LEAGUE)

cleaned_df.to_csv(OUTPUT_CSV_FILE_PATH, index=False)
