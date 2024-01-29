from apps.stt.api.v1.events import EventViewSet
from apps.stt.api.v1.purchases import PurchaseViewSet
from apps.stt.api.v1.teams import TeamViewSet
from apps.stt.api.v1.ticket_holder_team import TicketHolderTeamViewSet
from apps.stt.api.v1.ticket_holders import TicketHolderViewSet
from apps.stt.api.v1.tickets import TicketViewSet
from rest_framework import routers

stt_router_v1 = routers.DefaultRouter()
stt_router_v1.register(r'teams', TeamViewSet, basename='teams')
stt_router_v1.register(r'ticket-holders', TicketHolderViewSet, basename='ticket-holders')
stt_router_v1.register('ticket-holders-teams', TicketHolderTeamViewSet, basename='ticket-holders-teams')
stt_router_v1.register(r'tickets', TicketViewSet, basename='tickets')
stt_router_v1.register(r'events', EventViewSet, basename='events')
stt_router_v1.register(r'purchases', PurchaseViewSet, basename='purchases')
