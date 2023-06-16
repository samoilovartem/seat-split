from datetime import datetime
from io import BytesIO

from loguru import logger
from numpy import record
from pandas import DataFrame as df
from rest_framework.request import Request
from rest_framework.response import Response

from django.apps import apps
from django.db.models.fields import NOT_PROVIDED

from apps.accounts.resource import AccountsResource
from apps.common_services.csv_converter import csv_to_dict, dict_to_csv
from apps.common_services.file_importer import CSVImporter
from apps.common_services.utils import (
    get_missing_date_fields,
    get_missing_strict_fields,
    get_model_fields,
)


def filter_request_fields(model_fields: list, request_fields: list) -> list:
    request_fields = [
        field for field in request_fields if list(field.keys())[0] in model_fields
    ]

    return request_fields


def get_request_fields(request: Request) -> list:
    """
    Gets the fields from a request.

    Args:
        request (Request): Request object from the endpoint.

    Returns:
        list: A list containing all the fields in the request.
    """

    request_fields = [
        {key: value} for key, value in request.data.items() if key != 'file'
    ]

    return request_fields


def use_fallback_dates(
    request_fields: list[dict[str, any]],
    date_fields: list,
) -> list:
    # use today's date as the default value for the last_opened field
    local_request_fields = request_fields
    date_today = datetime.today().strftime('%Y-%m-%d')

    # apply the fallback values to the request fields
    for date_field in date_fields:
        local_request_fields.append({date_field: date_today})


def get_request_file(request: Request) -> dict:
    """
    Gets the file from a request.

    Args:
        request (Request): Request object from the endpoint.

    Returns:
        dict: A dictionary containing the data from the request file.
    """
    return request.FILES.get('file').read().decode('utf-8')


def set_dict_to_default(
    dictionary: dict,
    default_values: dict,
    fallback: str = 'NA',
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

    logger.warning(f'Dictionary: {dictionary}')

    return dictionary


def normalize_request_dates(
    csv_dictionary: record,
    request_fields: list[dict],
    date_fields: list = ["created_at", "last_opened"],
) -> list[dict]:
    missing_dates = get_missing_date_fields(csv_dictionary, date_fields)

    ignore_dates = {'ignore_dates': 'true'} in request_fields

    if missing_dates:
        if not ignore_dates:
            error_message = f'missing dates {missing_dates}. Please provide dates or set ignore_dates:true'
            return Response({'success': False, 'error': error_message})

        fallback_date = datetime.today().strftime('%Y-%m-%d')

        supplied_dates = [
            date for date in request_fields if list(date.keys())[0] in date_fields
        ]

        # check if the request covers all the missing dates
        unassigned_dates = set(missing_dates) - set(supplied_dates)
        for date_field in unassigned_dates:
            request_fields.append({date_field: fallback_date})

    return request_fields


def normalize_csv_request(
    request: Request,
    app_name: str,
    model_name: str,
    exclude_fields: list = [],
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

    if 'file' not in request.FILES:
        raise ValueError('No file was uploaded.')

    csv_dict = csv_to_dict(str(get_request_file(request)))
    csv_headers = set(csv_dict[0].keys())

    # get the fields in the model that are not in the csv file
    model_fields = get_model_fields(app_name, model_name, exclude_fields=exclude_fields)

    missing_fields = [field for field in model_fields if field not in csv_headers]

    default_values = {
        field.name: field.default
        for field in apps.get_model(app_name, model_name)._meta.fields
        if field.name in missing_fields
    }

    for row in csv_dict:
        [row.update({field: default_values[field]}) for field in missing_fields]

    for row in csv_dict:
        row = set_dict_to_default(row, default_values)

    csv_dict = (
        df.from_records(csv_dict)
        .reindex(columns=model_fields, fill_value='NA')
        .to_dict('records')
    )

    csv_file = dict_to_csv(csv_dict)

    # create a new request object with the updated csv file
    new_request = request
    new_request.FILES['file'].file = BytesIO(csv_file)

    return new_request


def apply_request_fields(
    request: Request,
    app_name: str,
    model_name: str,
    exclude_fields: list = [],
    strict_fields: list = [],
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

    if 'file' not in request.FILES:
        raise ValueError('No file was uploaded.')

    normalized_request = normalize_csv_request(
        request,
        app_name,
        model_name,
        exclude_fields,
    )

    csv_file = (
        normalized_request.FILES.get('file').read().decode('utf-8')
    )  # get the csv file

    csv_dictionary = csv_to_dict(csv_file)  # convert the csv file to a dictionary
    request_fields = get_request_fields(normalized_request)
    model_fields = get_model_fields(app_name, model_name, exclude_fields=exclude_fields)

    request_fields = normalize_request_dates(csv_dictionary, request_fields)
    request_fields = filter_request_fields(model_fields, request_fields)

    for row in csv_dictionary:
        [row.update(dictionaries) for dictionaries in request_fields]

    missing_strict_fields = get_missing_strict_fields(
        csv_dictionary,
        strict_fields=["recovery_email"],
    )

    if missing_strict_fields:
        error_message = f'missing strict fields {missing_strict_fields}. Please provide in the request.'
        return Response({'success': False, 'error': error_message})

    csv_file = dict_to_csv(csv_dictionary)
    normalized_request.FILES.get('file').file = BytesIO(csv_file)

    csv_importer = CSVImporter(
        normalized_request,
        app_name='accounts',
        model_name='Accounts',
        resource=AccountsResource,
        duplicate_check_column='email',
        exclude_fields=['updated_at', 'id'],
    )

    response = csv_importer.import_file()

    return response
