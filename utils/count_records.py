import os

import pandas as pd


def count_csv_records(directory):
    total_records = 0

    for file_name in os.listdir(directory):
        if file_name.endswith('.csv'):
            file_path = os.path.join(directory, file_name)
            df = pd.read_csv(file_path)
            total_records += len(df)

    return total_records


directory_path = '/Users/samoylovartem/Documents/Data/Splitted addresses'
total_records = count_csv_records(directory_path)

print(f'Total records in all CSV files: {total_records}')
