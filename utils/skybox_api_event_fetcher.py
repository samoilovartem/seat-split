import json

import requests
from loguru import logger
from requests import Response
from settings import settings


class SportsEventsFetcher:
    def __init__(self, league: str, start_year: int):
        self.league = league
        self.start_year = start_year
        self.event_date_from, self.event_date_to = self._fetch_seasons_dates()

    def _fetch_seasons_dates(self):
        response = requests.get(
            url=f'{settings.stt_endpoint}{settings.stt_seasons_prefix}',
            headers=settings.get_stt_authorization_header,
            params={'league': self.league, 'start_year': self.start_year},
        )

        data = response.json().get('results')[0]
        start_regular_season_date = data['start_regular_season_date']
        end_regular_season_date = data['end_regular_season_date']

        return start_regular_season_date, end_regular_season_date

    def _create_params(self):
        return {
            'limit': 4000,
            'eventType': 'SPORT',
            'excludeParking': 'true',
            'category': self.league,
            'eventDateFrom': self.event_date_from,
            'eventDateTo': self.event_date_to,
        }

    def fetch_events(self):
        response = requests.get(
            url=settings.get_skybox_events_endpoint,
            headers=settings.get_skybox_api_headers,
            params=self._create_params(),
        )
        self._save_to_json_file(response)
        return response.json()

    @staticmethod
    def _save_to_json_file(response: Response):
        with open('events.json', 'w') as f:
            json.dump(response.json(), f, indent=4)


if __name__ == '__main__':
    league = 'MLS'
    start_year = 2024
    sports_events_fetcher = SportsEventsFetcher(league, start_year)
    logger.info(json.dumps(sports_events_fetcher.fetch_events(), indent=4))
