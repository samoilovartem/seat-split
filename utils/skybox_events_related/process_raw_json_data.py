import json
import re
from uuid import UUID

import pandas as pd
import pytz
from loguru import logger
from pandas import DataFrame


class DataProcessor:
    def __init__(
        self,
        json_file_path: str,
        csv_output_filename: str,
        season: UUID,
        league: str,
        replacements: dict[str, dict[str, str]],
    ):
        self.json_file_path = json_file_path
        self.csv_output_filename = csv_output_filename
        self.season = season
        self.league = league
        self.replacements = replacements

    @staticmethod
    def _replace_values_in_column(df: DataFrame, column_name: str, old_value_regex: str, new_value: str):
        df[column_name] = df[column_name].apply(
            lambda x: re.sub(old_value_regex, new_value, x, flags=re.IGNORECASE)
        )
        return df

    @staticmethod
    def _convert_to_timezone_aware_and_remove_timezone_column(
        df: DataFrame, date_time_col: str, timezone_col: str
    ):
        df[date_time_col] = pd.to_datetime(df[date_time_col])

        def apply_timezone(row):
            tz = pytz.timezone(row[timezone_col])
            return tz.localize(row[date_time_col])

        df[date_time_col] = df.apply(apply_timezone, axis=1)

        df.drop(columns=[timezone_col], inplace=True)

        return df

    @staticmethod
    def _clean_name(name: str):
        name = re.sub(r'\s+', ' ', name)
        match = re.search(r'(.+? - )?(.+ at .+?)(?=\s+\(|$)', name)
        if match:
            return match.group(2).strip()
        return name

    @staticmethod
    def _extract_additional_info(name: str):
        additional_info = []

        prefix_match = re.search(r'^(.+?) - ', name)
        if prefix_match:
            additional_info.append(prefix_match.group(1))

        parentheses_matches = re.findall(r'\((.+?)\)', name)
        additional_info.extend(parentheses_matches)
        return ', '.join(additional_info)

    def _load_json_data(self):
        with open(self.json_file_path, 'r') as json_file:
            data = json.load(json_file)
        return data['rows']

    @staticmethod
    def _create_data_list(rows: list[dict]):
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
        return data_list

    def _create_and_prepare_dataframe(self, data_list: list[dict]):
        df = pd.DataFrame(data_list)

        df['additional_info'] = df['name'].apply(self._extract_additional_info)
        df['name'] = df['name'].apply(self._clean_name)

        df['season'] = self.season
        df['league'] = self.league

        df = self._convert_to_timezone_aware_and_remove_timezone_column(
            df, 'date_time', 'skybox_venue_timezone'
        )

        if self.replacements:
            for column_name, replacement_dict in self.replacements.items():
                for old_value, new_value in replacement_dict.items():
                    df = self._replace_values_in_column(df, column_name, old_value, new_value)

        return df

    def process_data(self):
        rows = self._load_json_data()
        data_list = self._create_data_list(rows)
        df = self._create_and_prepare_dataframe(data_list)

        df.to_csv(self.csv_output_filename, index=False)

        logger.info('Data has been written to {}', self.csv_output_filename)


if __name__ == '__main__':
    JSON_FILE_PATH = 'json_source_files/MLB_2024_raw_data.json'
    CSV_OUTPUT_FILENAME = 'MLB2024_cleaned_raw.csv'
    SEASON = UUID('5845102f-99d4-48fb-ba8f-30d8c2799326')
    LEAGUE = 'MLB'
    REPLACEMENTS = {
        'name': {
            r'\bSt Louis Cardinals\b': 'St. Louis Cardinals',
        }
    }

    dp = DataProcessor(JSON_FILE_PATH, CSV_OUTPUT_FILENAME, SEASON, LEAGUE, REPLACEMENTS)
    dp.process_data()
