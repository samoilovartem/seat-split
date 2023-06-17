from io import StringIO

import pandas as pd


def csv_to_dict(data: str) -> list[dict[str, str]]:
    """
    Convert a list of csv strings to a list of dictionaries.

    Args:
        data: list of csv strings

    Returns:
        list of dictionaries
    """
    try:
        # convert csv string to dataframe
        df = pd.read_csv(StringIO(data))
        df.fillna('NA', inplace=True)

        # convert dataframe to list of dictionaries
        return df.to_dict('records')
    except pd.errors.ParserError as e:
        raise ValueError(f'Invalid CSV file: {e}')


def dict_to_csv(data: list[dict[str, str]]) -> bytes:
    """
    Convert a list of dictionaries to a bytes object.

    Args:
        data: list of dictionaries

    Returns:
        A bytes object representing the csv file.
    """
    try:
        csv = pd.DataFrame(data).to_csv(index=False)

        return csv.encode('utf-8')
    except ValueError as e:
        raise ValueError(f'Invalid CSV file: {e}')
