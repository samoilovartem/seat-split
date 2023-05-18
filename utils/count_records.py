import os

import pandas as pd
from dotenv import load_dotenv
from loguru import logger

load_dotenv()


def count_csv_records(directory):
    total_records = 0

    for file_name in os.listdir(directory):
        if file_name.endswith('.csv'):
            file_path = os.path.join(directory, file_name)
            df = pd.read_csv(file_path)
            num_records = len(df)
            total_records += num_records
            logger.info('Number of records in {}: {}', file_name, num_records)

    return total_records


directory_path = os.environ.get('COUNT_RECORDS_DIRECTORY_PATH')
total_records = count_csv_records(directory_path)

logger.info('Total records in all CSV files: {}', total_records)
