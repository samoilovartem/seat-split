from collections import namedtuple

import pandas as pd
import requests
from config import config
from loguru import logger

Team = namedtuple('Team', ['name', 'league', 'home_venue'], defaults=[''])


def add_home_venue(team: Team, filename=config.team_venue_file):
    df = pd.read_csv(filename)
    df = df.set_index('team')

    home_venue = df.loc[team.name, 'home_venue']
    if not home_venue:
        logger.error('home_venue COULD NOT BE FOUND', team.name)
        return team

    return Team(team.name, team.league, home_venue)


def get_teams():
    team_list: list[Team] = []

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'token ' + config.stt_auth_token,
    }

    try:
        req = requests.get(config.stt_teams_endpoint, headers=headers)
        data = req.json()['results']
        for team in data:
            target = add_home_venue(Team(team['name'], team['league'], team['home_venue']))
            team_list.append(target)

    except Exception as e:
        logger.exception('teams call failed', e)
        exit()
    finally:
        # order teams by league
        team_list.sort(key=lambda x: x.league)
        return team_list
