from rest_framework import routers

from .views import *

cards_router = routers.SimpleRouter()

cards_router.register(r'cards/all', AllCardsViewSet, basename='all-cards')
cards_router.register(r'cards/lawns', LawnsCardsViewSet, basename='lawns-cards')
cards_router.register(r'cards/presales', PresalesCardsViewSet, basename='presales-cards')
cards_router.register(r'cards/mlb', MLBCardsViewSet, basename='mlb-cards')
cards_router.register(r'cards/nba', NBACardsViewSet, basename='nba-cards')
cards_router.register(r'cards/seasons', SeasonsCardsViewSet, basename='seasons-cards')
cards_router.register(r'cards/smallvenues', SmallVenuesCardsViewSet, basename='smallvenues-cards')
cards_router.register(r'cards/theatre', TheatreCardsViewSet, basename='theatre-cards')
cards_router.register(r'cards/othersports', OtherSportsCardsViewSet, basename='othersports-cards')
cards_router.register(r'cards/audrey', AudreyCardsViewSet, basename='audrey-cards')
cards_router.register(r'cards/others', OthersCardsViewSet, basename='others-cards')
cards_router.register(r'cards/universal_filter', UniversalFilterViewSet, basename='universal_filter')

