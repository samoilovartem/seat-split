from collections import namedtuple

import config as cfg
import pandas as pd
import requests

TEAMVENUE_FILE = "team_and_homecourts.csv"
Team = namedtuple('Team', ['name', 'league', 'home_venue'], defaults=[''])


def add_homevenue(team: Team, filename=TEAMVENUE_FILE):
    df = pd.read_csv(filename)
    df = df.set_index('team')

    home_venue = df.loc[team.name, 'home_venue']
    if not home_venue:
        print("home_venue COULD NOT BE FOUND", team.name)
        return team

    return Team(team.name, team.league, home_venue)


def get_teams():

    team_list: list[Team] = []

    headers = {
        "Content-Type": "application/json",
        "Authorization": "token " + cfg.AUTH_TOKEN
    }

    try:
        req = requests.get(cfg.TEAMS_ENDPOINT, headers=headers)
        data = req.json()["results"]
        for team in data:
            target = add_homevenue(
                Team(team["name"], team["league"], team["home_venue"]))
            team_list.append(target)

    except Exception as e:
        print("teams call failed", e)
        exit()
    finally:
        # order teams by league
        team_list.sort(key=lambda x: x.league)
        return team_list
