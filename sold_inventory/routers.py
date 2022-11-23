from rest_framework import routers
from .views import *

sold_inventory_router = routers.SimpleRouter()

sold_inventory_router.register(r'mlb_sold_inventory/all', MLBSoldInventoryViewSet,
                               basename='MLBSoldInventory')
sold_inventory_router.register(r'mlb_sold_inventory/universal_filter', MLBSoldInventoryUniversalFilterViewSet,
                               basename='MLBSoldInventory_universal_filter')
