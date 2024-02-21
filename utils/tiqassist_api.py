import csv

import requests
from loguru import logger
from rest_framework import status
from settings import settings


class TiqAssistDataProcessor:
    def __init__(self):
        self.stt_teams_fields = self.fetch_stt_teams_fields()
        self.fields_to_exclude = ['id', 'created_at']
        self.required_fields = [
            field for field in self.stt_teams_fields if field not in self.fields_to_exclude
        ]

    def fetch_stt_teams_fields(self):
        response = requests.get(
            url=settings.get_stt_teams_endpoint, headers=settings.get_stt_authorization_header
        )
        if response.status_code == status.HTTP_200_OK:
            data = response.json()
            if data['results']:
                return list(data['results'][0].keys())
        else:
            logger.error(f'Failed to fetch fields from my endpoint: {response.status_code}')
            return []
        return []

    def fetch_and_process_teams(self):
        response = requests.get(settings.tiqassist_endpoint)
        if response.status_code == status.HTTP_200_OK:
            data = response.json()
            teams = [team for team in data['teams'] if team['league'] == 'NCAAF']

            for team in teams:
                if 'id' in team:
                    team['skybox_id'] = team.pop('id')

            filtered_teams = self.filter_teams(teams)
            self.export_to_csv(filtered_teams)
        else:
            logger.error(f'Failed to fetch data from tiqassist: {response.status_code}')

    def filter_teams(self, teams):
        filtered_teams = []
        for team in teams:
            filtered_team = {key: team[key] for key in self.stt_teams_fields if key in team}
            filtered_teams.append(filtered_team)
        return filtered_teams

    def export_to_csv(self, filtered_teams):
        if filtered_teams:
            csv_file = 'ncaaf_teams.csv'
            with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
                fieldnames = filtered_teams[0].keys()
                csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
                csv_writer.writeheader()
                for team in filtered_teams:
                    csv_writer.writerow(team)
            logger.info(f"CSV file '{csv_file}' created successfully.")
        else:
            logger.info('No matching fields found between endpoints.')


if __name__ == '__main__':
    teams_data_processor = TiqAssistDataProcessor()
    teams_data_processor.fetch_and_process_teams()
