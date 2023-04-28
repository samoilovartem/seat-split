from import_export.resources import modelresource_factory
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet

from apps.utils.duplicate_checker import DuplicateChecker
from apps.utils.file_importer import CSVImporter
from apps.venues.models import Venues
from apps.venues.serializers import VenuesSerializer


class AllVenuesViewSet(ModelViewSet):
    queryset = Venues.objects.all()
    serializer_class = VenuesSerializer
    search_fields = [
        'name',
        'address',
    ]
    ordering_fields = [
        'state_code',
    ]
    my_tags = ['All venues']

    @action(methods=['GET'], detail=False)
    def show_duplicates(self, request):
        duplicate_checker = DuplicateChecker(model=Venues, field='address')
        return duplicate_checker.get_duplicate_summary()

    @action(methods=['POST'], detail=False)
    def import_file(self, request):
        csv_importer = CSVImporter(
            request,
            app_name='venues',
            model_name='Venues',
            resource=modelresource_factory(Venues),
            exclude_fields=['updated_at', 'created_at', 'id', 'latitude', 'longitude'],
        )
        response = csv_importer.import_file()
        return response
