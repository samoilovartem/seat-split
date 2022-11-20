from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework.permissions import IsAuthenticated
from .serializers import CardsSerializer
from .pagination import CardsApiListPagination

from .models import Cards


class AllCardsViewSet(viewsets.ModelViewSet):
    queryset = Cards.objects.all()
    serializer_class = CardsSerializer
    pagination_class = CardsApiListPagination
    permission_classes = [HasAPIKey | IsAuthenticated]
    my_tags = ["All cards"]

    @action(methods=['get'], detail=False)
    def get_all_creators(self, request):
        result = Cards.objects.order_by().values_list('created_by', flat=True).distinct()
        return Response({'results': {'All creators': result}})


class LawnsCardsViewSet(viewsets.ModelViewSet):
    serializer_class = CardsSerializer
    pagination_class = CardsApiListPagination
    permission_classes = [HasAPIKey | IsAuthenticated]
    my_tags = ["Lawns cards"]

    def get_queryset(self):
        pk = self.kwargs.get('pk')

        if not pk:
            return Cards.objects.filter(team__icontains='LAWNS')
        return Cards.objects.filter(team__icontains='LAWNS', pk=pk)

    @action(methods=['get'], detail=False)
    def get_creators(self, request):
        result = Cards.objects.filter(team__icontains='LAWNS') \
            .order_by().values_list('created_by', flat=True).distinct()
        return Response({'results': {'All creators': result}})


class PresalesCardsViewSet(viewsets.ModelViewSet):
    serializer_class = CardsSerializer
    pagination_class = CardsApiListPagination
    permission_classes = [HasAPIKey | IsAuthenticated]
    my_tags = ["Presales cards"]

    def get_queryset(self):
        pk = self.kwargs.get('pk')

        if not pk:
            return Cards.objects.filter(team__icontains='PRESALES')
        return Cards.objects.filter(team__icontains='PRESALES', pk=pk)


class MLBCardsViewSet(viewsets.ModelViewSet):
    serializer_class = CardsSerializer
    pagination_class = CardsApiListPagination
    permission_classes = [HasAPIKey | IsAuthenticated]
    my_tags = ["MLB cards"]

    def get_queryset(self):
        pk = self.kwargs.get('pk')

        if not pk:
            return Cards.objects.filter(team__icontains='MLB')
        return Cards.objects.filter(team__icontains='MLB', pk=pk)


class NBACardsViewSet(viewsets.ModelViewSet):
    serializer_class = CardsSerializer
    pagination_class = CardsApiListPagination
    permission_classes = [HasAPIKey | IsAuthenticated]
    my_tags = ["NBA cards"]

    def get_queryset(self):
        pk = self.kwargs.get('pk')

        if not pk:
            return Cards.objects.filter(team__icontains='NBA')
        return Cards.objects.filter(team__icontains='NBA', pk=pk)


class SeasonsCardsViewSet(viewsets.ModelViewSet):
    serializer_class = CardsSerializer
    pagination_class = CardsApiListPagination
    permission_classes = [HasAPIKey | IsAuthenticated]
    my_tags = ["Seasons cards"]

    def get_queryset(self):
        pk = self.kwargs.get('pk')

        if not pk:
            return Cards.objects.filter(team__icontains='SEASONS')
        return Cards.objects.filter(team__icontains='SEASONS', pk=pk)


class SmallVenuesCardsViewSet(viewsets.ModelViewSet):
    serializer_class = CardsSerializer
    pagination_class = CardsApiListPagination
    permission_classes = [HasAPIKey | IsAuthenticated]
    my_tags = ["Small Venues cards"]

    def get_queryset(self):
        pk = self.kwargs.get('pk')

        if not pk:
            return Cards.objects.filter(team__icontains='SMALL VENUES')
        return Cards.objects.filter(team__icontains='SMALL VENUES', pk=pk)


class TheatreCardsViewSet(viewsets.ModelViewSet):
    serializer_class = CardsSerializer
    pagination_class = CardsApiListPagination
    permission_classes = [HasAPIKey | IsAuthenticated]
    my_tags = ["Theatre cards"]

    def get_queryset(self):
        pk = self.kwargs.get('pk')

        if not pk:
            return Cards.objects.filter(team__icontains='THEATRE')
        return Cards.objects.filter(team__icontains='THEATRE', pk=pk)


class OtherSportsCardsViewSet(viewsets.ModelViewSet):
    serializer_class = CardsSerializer
    pagination_class = CardsApiListPagination
    permission_classes = [HasAPIKey | IsAuthenticated]
    my_tags = ["Other Sports cards"]

    def get_queryset(self):
        pk = self.kwargs.get('pk')

        if not pk:
            return Cards.objects.filter(team__icontains='OTHER SPORTS')
        return Cards.objects.filter(team__icontains='OTHER SPORTS', pk=pk)


class AudreyCardsViewSet(viewsets.ModelViewSet):
    serializer_class = CardsSerializer
    pagination_class = CardsApiListPagination
    permission_classes = [HasAPIKey | IsAuthenticated]
    my_tags = ["Audrey cards"]

    def get_queryset(self):
        pk = self.kwargs.get('pk')

        if not pk:
            return Cards.objects.filter(team__icontains='AUDREY')
        return Cards.objects.filter(team__icontains='AUDREY', pk=pk)


class OthersCardsViewSet(viewsets.ModelViewSet):
    serializer_class = CardsSerializer
    pagination_class = CardsApiListPagination
    permission_classes = [HasAPIKey | IsAuthenticated]
    my_tags = ["Others cards"]

    def get_queryset(self):
        pk = self.kwargs.get('pk')

        if not pk:
            return Cards.objects.filter(team__icontains='OTHERS')
        return Cards.objects.filter(team__icontains='OTHERS', pk=pk)


class UniversalFilterViewSet(viewsets.ModelViewSet):
    serializer_class = CardsSerializer
    pagination_class = CardsApiListPagination
    permission_classes = [HasAPIKey | IsAuthenticated]

    def get_queryset(self):
        filter_name = self.request.query_params.get('filter_name')
        value = self.request.query_params.get('value')
        return Cards.objects.filter(**{f"{filter_name}__icontains": value})
