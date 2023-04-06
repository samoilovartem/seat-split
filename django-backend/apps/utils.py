from typing import Optional

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
