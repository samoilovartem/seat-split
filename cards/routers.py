from rest_framework import routers

from .views import *

cards_router = routers.SimpleRouter()

cards_router.register(r'cards', AllCardsViewSet, basename='all-cards')

