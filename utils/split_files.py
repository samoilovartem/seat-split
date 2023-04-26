import os

import pandas as pd


def split_csv_files(input_directory, output_directory, records_per_file):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for file_name in os.listdir(input_directory):
        if file_name.endswith('.csv'):
            file_path = os.path.join(input_directory, file_name)

            df = pd.read_csv(file_path)

            df = df.dropna(subset=['line'])

            df = df.drop_duplicates(subset=['line', 'city'])

            if 'postal_code' in df.columns:
                df['postal_code'] = df['postal_code'].astype('Int64')

            if len(df) > records_per_file:
                num_output_files = -(-len(df) // records_per_file)

                for i in range(num_output_files):
                    start = i * records_per_file
                    end = (i + 1) * records_per_file
                    output_df = df.iloc[start:end]

                    split_file_name = f'{file_name[:-4]}_{i + 1}.csv'
                    split_file_path = os.path.join(output_directory, split_file_name)

                    output_df.to_csv(split_file_path, index=False)
            else:
                output_file_path = os.path.join(output_directory, file_name)
                df.to_csv(output_file_path, index=False)


input_directory_path = '/Users/samoylovartem/Documents/Data/Addresses'
output_directory_path = '/Users/samoylovartem/Documents/Data/Splitted addresses'
records_per_file = 3500

if __name__ == '__main__':
    split_csv_files(input_directory_path, output_directory_path, records_per_file)
