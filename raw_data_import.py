import os

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

dotenv_file = ".env"
if os.path.isfile(dotenv_file):
    load_dotenv(dotenv_file)

DB = os.environ.get("HEROKU_PGDB").replace("postgres", "postgresql")


def process_sql_using_pandas():
    engine = create_engine(DB)
    conn = engine.connect().execution_options(stream_results=True)
    frames = []
    for chunk_dataframe in pd.read_sql(
        "SELECT * FROM accounts_accounts", conn, chunksize=1000
    ):
        print(f"Got dataframe w/{len(chunk_dataframe)} rows")
        frames.append(chunk_dataframe)
    print(len(frames))
    dataframe = pd.concat(frames)
    print(len(dataframe))


if __name__ == "__main__":
    process_sql_using_pandas()
