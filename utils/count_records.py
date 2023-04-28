import os

import pandas as pd


def count_csv_records(directory):
    total_records = 0

    for file_name in os.listdir(directory):
        if file_name.endswith('.csv'):
            file_path = os.path.join(directory, file_name)
            df = pd.read_csv(file_path)
            num_records = len(df)
            total_records += num_records
            print(f'Number of records in {file_name}: {num_records}')

    return total_records


directory_path = '/Users/samoylovartem/Documents/Data/Addresses'
total_records = count_csv_records(directory_path)

print(f'Total records in all CSV files: {total_records}')
