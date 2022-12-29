from rest_framework import routers

from cards.views import *

cards_router = routers.SimpleRouter()

cards_router.register(r'cards', AllCardsViewSet, basename='all-cards')

