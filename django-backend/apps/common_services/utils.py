from typing import Optional

from numpy import record
from pygments import highlight
from pygments.formatters import TerminalFormatter
from pygments.lexers import PostgresLexer
from sqlparse import format

from django.apps import apps
from django.db.models import Count, Model, QuerySet


def records_per_value(model: type[Model], filter_name: str) -> list[dict[str, int]]:
    result = (
        model.objects.values(filter_name)
        .order_by(filter_name)
        .annotate(count=Count(filter_name))
    )
    return result


def get_missing_strict_fields(csv_dict: record, strict_fields: list[str] | None = None) -> list[dict[str, str]]:
    """Get fields with properly assigned values in the CSV file


    Args:
        csv_dict (numpy record): the csv file represented as a numpy record
        strict_fields (list): the list of fields that must be strictly enforced

    Returns:
        list: a list of dictionaries, each in the format
        email: account_email, field: missing_field
    """

    if strict_fields is None:
        return []

    missing_strict_fields = list()

    for row in csv_dict:
        for field in strict_fields:
            if row.get(field) == 'NA':
                entry = {'email': row.get('email'), 'field': field}
                missing_strict_fields.append(entry)

    return missing_strict_fields


def get_missing_date_fields(csv_dict: record, date_fields: list[str] | None = None) -> list[str]:
    """Get date fields with invalid values in the CSV file

    Args:
        csv_dict (numpy record): the csv file represented as a numpy record
        date_fields (list): the list of date fields to bvc un
    Returns:
        list: The list of date fields or columns that have no proper values
    """

    if date_fields is None:
        return []

    missing_dates = [
        date_field
        for date_field, date in csv_dict[0].items()
        if date_field in date_fields and date == 'NA'
    ]

    return missing_dates


def get_model_fields(
    app_name: str, model_name: str, exclude_fields: Optional[list[str]] = None
) -> list[str]:
    model = apps.get_model(app_name, model_name)
    fields = [field.name for field in model._meta.fields]

    if exclude_fields:
        fields = [field for field in fields if field not in exclude_fields]

    return fields


def show_changed_fields(obj, fields):
    delta = obj.diff_against(obj.prev_record)

    for change in delta.changes:
        fields += str(
            f'<strong>{change.field}</strong> changed from <span style="background-color:#E4260C">{change.old}'
            f'</span> to <span style="background-color:#92BF0F">{change.new}</span> . <br/>'
        )
    return fields


def print_sql(queryset: QuerySet) -> None:
    formatted = format(str(queryset.query), reindent=True)
    print(highlight(formatted, PostgresLexer(), TerminalFormatter()))
