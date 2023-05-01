from rest_framework.response import Response

from django.db.models import Count


class DuplicateChecker:
    def __init__(self, model, field):
        self.model = model
        self.field = field

    def _get_duplicates(self):
        duplicates = (
            self.model.objects.values(self.field)
            .annotate(duplicates=Count('id'))
            .order_by()
            .filter(duplicates__gt=1)
        )
        return duplicates

    def _get_unique_count(self):
        unique_count = self.model.objects.values(self.field).distinct().count()
        return unique_count

    @staticmethod
    def _get_unique_duplicates_count(duplicates):
        unique_duplicates_count = duplicates.count()
        return unique_duplicates_count

    def get_duplicate_summary(self):
        duplicates = self._get_duplicates()
        unique_count = self._get_unique_count()
        unique_duplicates_count = self._get_unique_duplicates_count(duplicates)

        total_count = unique_duplicates_count + unique_count

        result = {
            'total number of records': total_count,
            'total number of unique duplicate records': unique_duplicates_count,
            'total number of unique records': unique_count,
            'all duplicate records': duplicates,
        }

        return Response(result)
