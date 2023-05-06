from django_filters.rest_framework import DjangoFilterBackend


class NotEqualFilterBackend(DjangoFilterBackend):
    def filter_queryset(self, request, queryset, view):
        exclude_columns = request.query_params.get('exclude_columns', '')
        exclude_values = request.query_params.get('exclude_values', '')

        if exclude_columns and exclude_values:
            exclude_columns = exclude_columns.split(',')
            exclude_values = exclude_values.split(',')

            if len(exclude_columns) == len(exclude_values):
                for column, value in zip(exclude_columns, exclude_values):
                    queryset = queryset.exclude(**{column: value})

        return queryset
