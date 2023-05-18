import os
from re import match

import pandas as pd
from dotenv import load_dotenv
from loguru import logger

load_dotenv()


def remove_scientific_notation(value):
    if isinstance(value, str) and match(r'\d(\.\d+)?[eE]\+\d+', value):
        return ''
    return value


file_path = os.environ.get('PREPARE_VENUES_FILE_PATH')
data = pd.read_csv(file_path)

data['phone'] = data['phone'].replace('#ERROR!', '')
data['state_code'] = data['state_code'].replace('0', '')
data['country_code'] = data['country_code'].replace('0', '')

data['phone'] = data['phone'].apply(remove_scientific_notation)

data = data.applymap(lambda x: x.strip() if isinstance(x, str) else x)

data = data.drop_duplicates(subset=['address', 'name'])

records_per_file = 3500

num_files = -(-len(data) // records_per_file)  # ceil division

input_directory = os.path.dirname(os.path.abspath(file_path))

for i in range(num_files):
    start_index = i * records_per_file
    end_index = min((i + 1) * records_per_file, len(data))
    data_slice = data.iloc[start_index:end_index]

    output_file_name = f'output_file_{i + 1}.csv'
    output_file_path = os.path.join(input_directory, output_file_name)
    data_slice.to_csv(output_file_path, index=False)

logger.info('Data processed and saved to {} files.', num_files)
