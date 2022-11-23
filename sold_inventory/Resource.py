from import_export import resources
from .models import MLBSoldInventory


class MLBSoldInventoryResource(resources.ModelResource):

    class Meta:
        model = MLBSoldInventory
        widgets = {
            'in_hand_date': {'format': '%Y-%m-%d'},
            'event_date': {'format': '%Y-%m-%d'},
            'last_price_update': {'format': '%Y-%m-%d'},
        }
