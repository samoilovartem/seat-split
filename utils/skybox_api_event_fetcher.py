import json

import requests
from settings import settings

LEAGUE = 'MLS'


def fetch_seasons_dates(league: str, start_year: int):
    response = requests.get(
        f'{settings.stt_endpoint}{settings.stt_seasons_prefix}',
        headers={'Authorization': f'Token {settings.stt_auth_token}'},
        params={'league': league, 'start_year': start_year},
    )

    start_regular_season_date = response.json()[0]['start_regular_season_date']
    end_regular_season_date = response.json()[0]['end_regular_season_date']

    return start_regular_season_date, end_regular_season_date


event_date_from, event_date_to = fetch_seasons_dates(LEAGUE, 2024)


params = {
    'limit': 4000,
    'eventType': 'SPORT',
    'excludeParking': 'true',
    'category': LEAGUE,
    'eventDateFrom': event_date_from,
    'eventDateTo': event_date_to,
}


def fetch_events():
    response = requests.get(
        settings.get_skybox_events_endpoint, headers=settings.get_skybox_api_headers, params=params
    )
    save_to_json_file(response)
    return response.json()


def save_to_json_file(response):
    with open('events.json', 'w') as f:
        json.dump(response.json(), f, indent=4)


if __name__ == '__main__':
    # print(fetch_events())
    print(fetch_seasons_dates('MLS', 2024))
