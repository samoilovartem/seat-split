from collections import namedtuple
from time import sleep
from timeit import default_timer as timer

import config as cfg
import leagues as leagues
import pandas as pd
import requests
import teams
from events import normalize_event


def can_fetch():
    response = requests.get(cfg.SENTINEL_ENDPOINT)
    return response.json()['total'] != "1"


def build_query(team: teams.Team, Leagues: dict[str, leagues.League]):
    params = {
        "keywords": [f"{team.name} {team.home_venue}"],
        "excludeParking": "true",
        "eventType": "SPORT",
        "eventDateFrom": Leagues[team.league].start_date,
        "eventDateTo": Leagues[team.league].end_date,
    }
    return params


def normalize_df(df, Teams: list):
    schema = ["skybox_event_id",
              "name", "league", "date_time", "season"]

    output_df = pd.DataFrame(columns=schema)
    team_names = [team.name for team in Teams]

    def get_league(name: str):
        for team in Teams:
            if team.name == name:
                return team.league

        return ""

    def django_date(date: str):
        date, time = date.split('T')
        return f"{date} {time}"

    for entry in df.to_dict(orient='records'):
        if 'at' not in entry['name'] or 'includes' in entry['name']:
            print("skipping", entry['name'])
            continue

        name = normalize_event(entry['name'], team_names)
        league = get_league(name)
        date_time = django_date(entry['date'])

        output_df = output_df._append({
            "skybox_event_id": entry['id'],
            "name": name,
            "league": league,
            "date_time": date_time,
            "season": "2023"
        }, ignore_index=True)

    return output_df


def build_df(data, team, Leagues):
    response = requests.get(cfg.ENDPOINT, headers=cfg.TEAM_HEADERS,
                            params=build_query(team, Leagues,),)
    if response.status_code != 200:
        print(
            f"""skybox call failed for team {team.name}:
                    {response.status_code} | {response.text}""")
        # return an empty dataframe
        return pd.DataFrame()

    data = response.json()['rows']
    df = pd.DataFrame(data)
    return df


def main():
    df = pd.DataFrame()

    Teams = teams.get_teams()
    Leagues = leagues.get_leagues()

    time = timer()
    sleep_time = cfg.sleep_time
    interval_time = cfg.interval_time

    for team in Teams:
        while not can_fetch():
            print(f"waiting for API to be free for {sleep_time} seconds")
            sleep(sleep_time)

            end = timer()
            elapsed_time = (end - time)/60

            print(f"elapsed time: {elapsed_time} minutes")

        entry_df = build_df(df, team, Leagues)

        if entry_df.empty:
            print(f"no events found for {team.name}")
            continue

        try:
            df = df._append(entry_df, ignore_index=True)
        except Exception as e:
            print(f"dataframe append failed | error: {e}")
        finally:
            print(f"successfully fetched events for {team.name}")

        time = timer()
        print(f"sleeping for {interval_time} seconds before next call")
        sleep(interval_time)

    final_df = normalize_df(df, Teams)
    final_df.to_csv(cfg.output_file, index=False)


if __name__ == "__main__":
    main()
