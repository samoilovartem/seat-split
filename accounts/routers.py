from rest_framework import routers

from .views import *

lawns_router = routers.DefaultRouter()
presales_router = routers.DefaultRouter()
mlb_router = routers.DefaultRouter()
nba_router = routers.DefaultRouter()
seasons_router = routers.DefaultRouter()
smallvenues_router = routers.DefaultRouter()
theatre_router = routers.DefaultRouter()
othersports_router = routers.DefaultRouter()
audrey_router = routers.DefaultRouter()


lawns_router.register(r'lawns_accounts', LawnsAccountsViewSet, basename='lawns-accounts')
presales_router.register(r'presales_accounts', PresalesAccountsViewSet, basename='presales-accounts')
mlb_router.register(r'mlb_accounts', MLBAccountsViewSet, basename='mlb-accounts')
nba_router.register(r'nba_accounts', NBAAccountsViewSet, basename='nba-accounts')
seasons_router.register(r'seasons_accounts', SeasonsAccountsViewSet, basename='seasons-accounts')
smallvenues_router.register(r'smallvenues_accounts', SmallVenuesAccountsViewSet, basename='smallvenues-accounts')
theatre_router.register(r'theatre_accounts', TheatreAccountsViewSet, basename='theatre-accounts')
othersports_router.register(r'othersports_accounts', OtherSportsAccountsViewSet, basename='othersports-accounts')
audrey_router.register(r'audrey_accounts', AudreyAccountsViewSet, basename='audrey-accounts')

