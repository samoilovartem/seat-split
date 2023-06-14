from io import BytesIO

from loguru import logger
from pandas import DataFrame as df
from rest_framework.request import Request

from django.apps import apps
from django.db.models.fields import NOT_PROVIDED

from apps.common_services.csv_converter import csv_to_dict, dict_to_csv
from apps.common_services.utils import get_model_fields


def get_request_fields(request: Request) -> list:
    """
    Gets the fields from a request.

    Args:
        request (Request): Request object from the endpoint.

    Returns:
        list: A list containing all the fields in the request.
    """

    request_fields = [
        {key: value} for key, value in request.data.items() if key != "file"
    ]

    return request_fields


def get_request_file(request: Request) -> dict:
    """
    Gets the file from a request.

    Args:
        request (Request): Request object from the endpoint.

    Returns:
        dict: A dictionary containing the data from the request file.
    """
    return request.FILES.get("file").read().decode("utf-8")


def set_dict_to_default(
    dictionary: dict, default_values: dict, fallback: str = "NA"
) -> dict:
    """
    Sets the values of a dictionary to the default values.

    Args:
        dictionary (dict): Dictionary to set the values of.
        default_values (dict): Default values to set the dictionary to.
        fallback (str, optional): Default value of a dict item, if it is not provided. Defaults to "NA".

    Returns:
        dict: Dictionary with the default values set.
    """
    for key in default_values:
        dictionary.setdefault(key, default_values[key])

    for key, value in dictionary.items():
        dictionary[key] = (
            fallback if isinstance(value, NOT_PROVIDED.__class__) else value
        )

    logger.warning(f"Dictionary: {dictionary}")

    return dictionary


def normalize_csv_request(
    request: Request, app_name: str, model_name: str, exclude_fields: list = []
) -> Request:
    """
    This function is used to normalize the request data from the frontend.

    If the csv file in the request does not have all fields within the Accounts model,
    then the function will add the missing fields to the csv file.

    Args:
        request (Request): request object
        app_name (str): app name
        model_name (str): model name
        exclude_fields (list): list of fields to exclude from the model

    Returns:
        Request: A new request object with the updated data.
    """

    if "file" not in request.FILES:
        raise ValueError("No file was uploaded.")

    csv_dict = csv_to_dict(str(get_request_file(request)))
    csv_headers = set(csv_dict[0].keys())

    # get the fields in the model that are not in the csv file
    model_fields = get_model_fields(app_name, model_name, exclude_fields=exclude_fields)
    missing_fields = [field for field in model_fields if field not in csv_headers]

    # get the default values for the missing fields and apply them to the csv file
    default_values = {
        field.name: field.default
        for field in apps.get_model(app_name, model_name)._meta.fields
        if field.name in missing_fields
    }
    for row in csv_dict:
        [row.update({field: default_values[field]}) for field in missing_fields]

    # fill in the missing values with the default values
    df(csv_dict).fillna("NA", inplace=True)
    for row in csv_dict:
        row = set_dict_to_default(row, default_values)

    # convert the csv file back to a bytes object
    csv_file = dict_to_csv(csv_dict)

    # create a new request object with the updated csv file
    new_request = request
    new_request.FILES["file"].file = BytesIO(csv_file)

    return new_request


def apply_request_fields(
    request: Request,
    app_name: str,
    model_name: str,
    exclude_fields: list = [],
) -> Request:
    """
    Applies all request fields to the csv file.

    Args:
        request (Request): request object
        app_name (str): app name
        model_name (str): model name
        exclude_fields (list): list of fields to exclude from the model

    Returns:
        Request: A new request object with the updated data.
    """

    if "file" not in request.FILES:
        raise ValueError("No file was uploaded.")

    normalized_request = normalize_csv_request(
        request,
        app_name,
        model_name,
        exclude_fields,
    )

    csv_file = (
        normalized_request.FILES.get("file").read().decode("utf-8")
    )  # get the csv file

    csv_dictionary = csv_to_dict(csv_file)  # convert the csv file to a dictionary

    request_fields = get_request_fields(normalized_request)

    model_fields = get_model_fields(app_name, model_name, exclude_fields=exclude_fields)

    request_fields = [
        field for field in request_fields if list(field.keys())[0] in model_fields
    ]

    for row in csv_dictionary:
        [row.update(dictionaries) for dictionaries in request_fields]

    csv_file = dict_to_csv(csv_dictionary)
    normalized_request.FILES.get("file").file = BytesIO(csv_file)

    return normalized_request
