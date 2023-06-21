from import_export.resources import modelresource_factory
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet

from apps.common_services.duplicate_checker import DuplicateChecker
from apps.common_services.file_importer import CSVImporter
from apps.config import VenuesCSVConfig
from apps.venues.models import Venues
from apps.venues.serializers import VenuesSerializer

APP_NAME = Venues._meta.app_label
MODEL_NAME = Venues._meta.model_name


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
    csv_config = VenuesCSVConfig()
    my_tags = ['All venues']

    @action(methods=['GET'], detail=False)
    def show_duplicates(self, request):
        duplicate_checker = DuplicateChecker(model=Venues, field='address')
        return duplicate_checker.get_duplicate_summary()

    @action(methods=['POST'], detail=False)
    def import_file(self, request):
        csv_importer = CSVImporter(
            request,
            app_name=APP_NAME,
            model_name=MODEL_NAME,
            resource=modelresource_factory(Venues),
            exclude_fields=self.csv_config.exclude_fields,
        )
        response = csv_importer.import_file()
        return response
