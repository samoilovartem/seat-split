from io import BytesIO, StringIO
import django
import pandas as pd
from ast import literal_eval


def csv_to_dict(data: str) -> list[dict[str, str]]:
    """
    Convert a list of csv strings to a list of dictionaries.

    Args:
        data: list of csv strings

    Returns:
        list of dictionaries
    """

    # convert csv string to dataframe
    df = pd.read_csv(StringIO(data))
    df.fillna("NA", inplace=True)

    # convert dataframe to list of dictionaries
    return df.to_dict("records")


def dict_to_csv(data: list[dict[str, str]]) -> list[str]:
    """
    Convert a list of dictionaries to a bytes object.

    Args:
        data: list of dictionaries

    Returns:
        A bytes object representing the csv file.
    """
    csv = pd.DataFrame(data).to_csv(index=False)

    # convert to bytes
    return csv.encode("utf-8")
