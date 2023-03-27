from apps.cards.views import AllCardsViewSet
from rest_framework import routers

cards_router = routers.SimpleRouter()

cards_router.register(r'cards', AllCardsViewSet, basename='all-cards')
