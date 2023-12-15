import csv

import requests

MAIN_URL = 'https://app.tiqassist.com/api/registration/options'

response = requests.get(MAIN_URL)

if response.status_code == 200:
    data = response.json()

    teams = [team for team in data['teams'] if team['league'] != 'NCAAB']

    csv_file = 'teams.csv'

    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        fieldnames = teams[0].keys()
        csv_writer = csv.DictWriter(file, fieldnames=fieldnames)

        csv_writer.writeheader()

        for team in teams:
            csv_writer.writerow(team)

    print(f"CSV file '{csv_file}' created successfully.")
else:
    print(f"Failed to fetch data: {response.status_code}")
