from datetime import datetime
from io import BytesIO

import pandas as pd
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

FILE_KEY = 'file'
DATE_FIELDS = ['created_at', 'last_opened']


def filter_request_fields(
    model_fields: list[str], request_fields: list[dict[str, any]]
) -> list[dict[str, any]]:
    """
    Filters the request fields to only include the model fields.

    Args:
        model_fields (list): The fields of the model.
        request_fields (list): The fields of the request.

    Returns:
        list: A list containing the fields of the request that are also in the model.
    """
    model_fields_set = set(model_fields)
    request_fields = [
        field for field in request_fields if list(field.keys())[0] in model_fields_set
    ]

    return request_fields


def get_request_fields(request: Request) -> list[dict[str, any]]:
    """
    Gets the fields from a request.

    Args:
        request (Request): Request object from the endpoint.

    Returns:
        list: A list containing all the fields in the request.
    """

    request_fields = [
        {key: value} for key, value in request.data.items() if key != FILE_KEY
    ]

    return request_fields


def get_request_dates(
    request: Request, date_fields: list[str] | None = None
) -> list[dict[str, any]]:
    """
    Gets the date fields from a request.

    Args:
        request (Request): Request object from the endpoint.

    Returns:
        list (list[dict[str, any]]): A list containing all the date fields in the request.
    """

    if date_fields is None:
        return []

    request_dates = [
        {key: value} for key, value in request.data.items() if key in date_fields
    ]

    return request_dates


def use_fallback_dates(
    request_fields: list[dict[str, any]],
    date_fields: list[str],
) -> list[dict[str, any]]:
    """
    Uses the fallback dates for the request fields.

    Args:
        request_fields (list[dict[str, any]]): The fields of the request.
        date_fields (list[str]): The date fields of the model.

    Returns:
        list: A list containing the fields of the request with the fallback dates.
    """
    # use today's date as the default value for all date-fields
    local_request_fields = request_fields
    date_today = datetime.today().strftime('%Y-%m-%d')

    # apply the fallback values to the request fields
    for date_field in date_fields:
        local_request_fields.append({date_field: date_today})

    return local_request_fields


def get_request_file(request: Request) -> str:
    """
    Gets the file from a request.

    Args:
        request (Request): Request object from the endpoint.

    Returns:
        str: The file in the request.
    """
    return request.FILES.get('file').read().decode('utf-8')


def set_dict_to_default(
    dictionary: dict[str, any],
    default_values: dict[str, any],
    fallback: str = 'NA',
) -> dict[str, any]:
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

    return dictionary


def normalize_csv_request(
    request: Request,
    app_name: str,
    model_name: str,
    exclude_fields: list[str] | None = None,
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

    if exclude_fields is None:
        exclude_fields = []

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
        pd.DataFrame.from_records(csv_dict)
        .reindex(columns=model_fields, fill_value='NA')
        .to_dict('records')
    )
    new_request = request

    csv_file = dict_to_csv(csv_dict)
    update_request_file(new_request, csv_file)

    return new_request


def normalize_request_dates(
    csv_dictionary: list[dict[str, any]],
    request_fields: list[dict[str, any]],
    normalized_request: Request,
) -> list[str]:
    """Normalizes request dates by setting them to fallback values when necessary

    Args:
        csv_dictionary (list(dict[str, any])): the csv file represented as a list of dictionaries
        request_fields (list[dict[str, any]]): the fields within the request body
        normalized_request (Request): the normalized request object

    Raises:
        ValueError: if the request does not contain the date fields and the ignore_dates field is not present

    Returns:
        list[dict[str, any]]: the normalized request fields
    """

    missing_dates = get_missing_date_fields(csv_dictionary, DATE_FIELDS)
    request_dates = get_request_dates(normalized_request, DATE_FIELDS)
    unassigned_dates = (
        set(missing_dates) - set(request_dates[0].keys()) if request_dates else set()
    )

    ignore_dates = {'ignore_dates': 'true'} in request_fields
    if not ignore_dates and missing_dates and not request_dates:
        raise ValueError(
            f'Missing date fields in request: {missing_dates}. Provide the missing dates or add the ignore_dates : true flag in the request.'
        )
    if not ignore_dates and unassigned_dates:
        raise ValueError(
            f'Missing date fields in request: {unassigned_dates}. Provide the missing dates or add the ignore_dates : true flag in the request.'
        )

    if ignore_dates and missing_dates and unassigned_dates:
        fallback_date = datetime.today().strftime('%Y-%m-%d')
        for date_field in unassigned_dates:
            request_fields.append({date_field: fallback_date})

    return request_fields


def apply_fields_to_rows(
    csv_dictionary: list[dict[str, any]],
    request_fields: list[dict[str, any]],
):
    """Applies the request fields to the csv file

    Args:
        csv_dictionary (list[dict[str, any]]): the csv file represented as a list of dictionaries
        request_fields (list[dict[str, any]]): the fields within the request body
    """
    for row in csv_dictionary:
        [row.update(dictionaries) for dictionaries in request_fields]


def update_request_file(request: Request, csv_file: bytes):
    """Updates the embedded csv file in the request object to the new csv file

    Args:
        request (Request): the request object to be updated
        csv_file (bytes): the new csv file to be embedded in the request object

    Raises:
        ValueError: if the csv file is invalid
    """
    try:
        csv_file = BytesIO(csv_file)
        request.FILES.get(FILE_KEY).file = csv_file
    except AttributeError:
        raise ValueError('Invalid csv file.')


def apply_request_fields(
    request: Request,
    app_name: str,
    model_name: str,
    exclude_fields: list[str] | None = None,
    strict_fields: list[str] | None = None,
) -> Response:
    """
    Applies all request fields to the csv file.

    Args:
        request (Request): request object
        app_name (str): app name
        model_name (str): model name
        exclude_fields (list): list of fields to exclude from the model
        strict-fields (list): list of fields that must be in the model

    Returns:
        Response: the response indicating whether the request was successful or not
    """

    if FILE_KEY not in request.FILES:
        return Response(
            {'success': False, 'error': f'No file was uploaded. {request.FILES}'}
        )

    if not exclude_fields:
        exclude_fields = []
    if not strict_fields:
        strict_fields = []

    normalized_request = normalize_csv_request(
        request,
        app_name,
        model_name,
        exclude_fields,
    )

    try:
        csv_dictionary = csv_to_dict(get_request_file(normalized_request))
        request_fields = get_request_fields(normalized_request)
        model_fields = get_model_fields(
            app_name, model_name, exclude_fields=exclude_fields
        )
        request_fields = normalize_request_dates(
            csv_dictionary, request_fields, normalized_request
        )
        request_fields = filter_request_fields(model_fields, request_fields)
    except ValueError as e:
        return Response({'success': False, 'error': str(e)})

    apply_fields_to_rows(csv_dictionary, request_fields)

    missing_strict_fields = get_missing_strict_fields(csv_dictionary, strict_fields)
    if missing_strict_fields:
        error_message = f'missing strict fields {missing_strict_fields}. Please provide in the request.'
        return Response({'success': False, 'error': error_message})

    update_request_file(normalized_request, dict_to_csv(csv_dictionary))

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
