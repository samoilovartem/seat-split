import os

import pandas as pd
from dotenv import load_dotenv

load_dotenv()

INPUT_DIRECTORY_PATH = os.environ.get('SPLIT_FILES_INPUT_DIRECTORY_PATH')
OUTPUT_DIRECTORY_PATH = os.environ.get('SPLIT_FILES_OUTPUT_DIRECTORY_PATH')
records_per_file = 3500


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


if __name__ == '__main__':
    split_csv_files(INPUT_DIRECTORY_PATH, OUTPUT_DIRECTORY_PATH, records_per_file)
