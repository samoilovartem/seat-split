from time import sleep
from timeit import default_timer as timer

import pandas as pd
import requests
from config import config
from events import normalize_event
from leagues import League, get_leagues
from loguru import logger
from teams import Team, get_teams


def can_fetch():
    response = requests.get(config.sentinel_endpoint)
    return response.json()['total'] != '1'


def build_query(team: Team, Leagues: dict[str, League]):
    params = {
        'keywords': [f'{team.name} {team.home_venue}'],
        'excludeParking': 'true',
        'eventType': 'SPORT',
        'eventDateFrom': Leagues[team.league].start_date,
        'eventDateTo': Leagues[team.league].end_date,
    }
    return params


def normalize_df(df, Teams: list):
    schema = ['skybox_event_id', 'name', 'league', 'date_time', 'season']

    output_df = pd.DataFrame(columns=schema)
    team_names = [team.name for team in Teams]

    def get_league(team_name: str):
        for team in Teams:
            if team.name == team_name:
                return team.league

        return ''

    def django_date(date: str):
        date, time = date.split('T')
        return f'{date} {time}'

    for entry in df.to_dict(orient='records'):
        if 'at' not in entry['name'] or 'includes' in entry['name']:
            logger.info('skipping', entry['name'])
            continue

        name = normalize_event(entry['name'], team_names)
        league = get_league(name)
        date_time = django_date(entry['date'])

        output_df = output_df._append(
            {
                'skybox_event_id': entry['id'],
                'name': name,
                'league': league,
                'date_time': date_time,
                'season': '2023',
            },
            ignore_index=True,
        )

    return output_df


def build_df(data, team, Leagues):
    response = requests.get(
        config.skybox_endpoint,
        headers=config.team_headers,
        params=build_query(
            team,
            Leagues,
        ),
    )
    if response.status_code != 200:
        logger.error(
            'skybox call failed for team {}: {} | {}',
            team.name,
            response.status_code,
            response.text,
        )
        # return an empty dataframe
        return pd.DataFrame()

    data = response.json()['rows']
    df = pd.DataFrame(data)
    return df


def main():
    df = pd.DataFrame()

    teams = get_teams()
    leagues = get_leagues()

    time = timer()
    sleep_time = config.sleep_time
    interval_time = config.interval_time

    for team in teams:
        while not can_fetch():
            logger.info('waiting for API to be free for {} seconds', sleep_time)
            sleep(sleep_time)

            end = timer()
            elapsed_time = (end - time) / 60

            logger.info('elapsed time: {} minutes', elapsed_time)

        entry_df = build_df(df, team, leagues)

        if entry_df.empty:
            logger.warning('no events found for {}', team.name)
            continue

        try:
            df = df._append(entry_df, ignore_index=True)
        except Exception as e:
            logger.exception('dataframe append failed | error: {}', e)
        finally:
            logger.success('successfully fetched events for {}', team.name)

        time = timer()
        logger.info('sleeping for {} seconds before next call', interval_time)
        sleep(interval_time)

    final_df = normalize_df(df, teams)
    final_df.to_csv(config.output_file, index=False)


if __name__ == '__main__':
    main()
