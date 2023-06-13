from io import BytesIO
from django.db.models.fields import NOT_PROVIDED
from loguru import logger
from apps.common_services.utils import get_model_fields
from apps.common_services.csv_converter import (
    csv_to_dict,
    dict_to_csv,
)
from django.apps import apps


def apply_request_fields(
    request, request_fields, app_name, model_name, exclude_fields=[]
):
    """
    Applies all request fields to the csv file.

    Args:
        request: request object
        request_fields: list of fields from the request
        app_name: app name
        model_name: model name

    Returns:
        A new request object with the updated data.
    """

    # get the csv file

    csv_file = request.FILES.get("file").read().decode("utf-8")

    # convert the csv file to a dictionary
    csv_dictionary = csv_to_dict(csv_file)
    logger.warning(f"csv_dictionary: {csv_dictionary}")

    model_fields = get_model_fields(app_name, model_name, exclude_fields=exclude_fields)
    request_fields = [
        {key: value} for key, value in request.data.items() if key in model_fields
    ]

    for row in csv_dictionary:
        for dictionaries in request_fields:
            for key, value in dictionaries.items():
                row[key] = value

    # convert the csv file data back to a csv file
    csv_file = dict_to_csv(csv_dictionary)

    new_request = request
    new_request.FILES.get("file").file = BytesIO(csv_file)

    return new_request


def normalize_csv_request(request, app_name, model_name, exclude_fields=[]):
    """
    This function is used to normalize the request data from the frontend.

    If the csv file in the request does not have all fields within the Accounts model,
    then the function will add the missing fields to the csv file.
    """

    # get the csv file
    csv_file = str(request.FILES.get("file").read().decode("utf-8"))

    # convert the csv file to a dictionary
    csv_dict = csv_to_dict(csv_file)

    # get the csv file headers
    csv_file_headers = set(csv_dict[0].keys())
    model_fields = get_model_fields(app_name, model_name, exclude_fields=exclude_fields)

    # get the missing fields
    missing_fields = [field for field in model_fields if field not in csv_file_headers]

    # get default values
    default_values = {
        field.name: field.default
        for field in apps.get_model(app_name, model_name)._meta.fields
        if field.name in missing_fields
    }

    # add the missing fields to the csv file
    for row in csv_dict:
        for field in missing_fields:
            row[field] = default_values[field]

    for row in csv_dict:
        for key, value in row.items():
            if key in default_values:
                row[key] = value
            elif not value:
                row[key] = "NA"

    # convert the csv file data back to a csv file
    csv_file = dict_to_csv(csv_dict)
    logger.warning(f"csv_file: {csv_file}")

    new_request = request
    new_request.FILES["file"].file = BytesIO(csv_file)

    return new_request
