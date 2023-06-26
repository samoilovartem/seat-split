from django.db.models import Q


def filter_queryset_startswith(queryset, search_fields, search_term):
    """
    Filters a queryset by performing a case-insensitive search with a wildcard at the end of the search term.

    Args:
        queryset (QuerySet): The queryset to filter.
        search_fields (list): A list of field names to search in the queryset.
        search_term (str): The search term to filter the queryset with.

    Returns:
        QuerySet: A filtered queryset based on the search term and search fields.

    Usage example in a Django Rest Framework viewset:

        def filter_queryset(self, queryset):
            queryset = super().filter_queryset(queryset)
            search = self.request.query_params.get('search', '')
            queryset = filter_queryset_startswith(queryset, self.search_fields, search)
            return queryset
    """
    if search_term:
        query = Q()
        for field in search_fields:
            query |= Q(**{f'{field}__istartswith': search_term})
        queryset = queryset.filter(query)
    return queryset
