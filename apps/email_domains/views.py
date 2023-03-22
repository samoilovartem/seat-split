from django.db.models import Prefetch
from faker import Faker
from rest_flex_fields import FlexFieldsModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.email_domains.models import EmailDomains
from apps.email_domains.serializers import EmailDomainsSerializer
from apps.email_domains.utils import email_domains_per_value, generate_data
from apps.users.models import User


class AllEmailDomainsViewSet(FlexFieldsModelViewSet):
    def get_queryset(self):
        queryset = EmailDomains.objects.all().prefetch_related(
            Prefetch('created_by', queryset=User.objects.only('id', 'username'))
        )
        return queryset

    permit_list_expands = ['created_by']
    serializer_class = EmailDomainsSerializer

    search_fields = ('domain_name',)
    ordering_fields = (
        'id',
        'created_at',
    )
    my_tags = ['All email domains']

    @action(methods=['GET'], detail=False)
    def get_email_domains_per_type(self, request):
        result = email_domains_per_value('type')
        return Response({'results': result})

    @action(methods=['POST'], detail=False)
    def generate_random_data_with_provided_domain_or_state(self, request):
        fake = Faker('en_US')

        domain_name = request.data.get('domain_name')
        state = request.data.get('state')

        if not domain_name:
            return Response({'error': 'Domain name is required'})

        if not state:
            data = generate_data(fake, domain_name)
            return Response(data)

        try:
            data = generate_data(fake, domain_name, state)
        except Exception as e:
            return Response({'error': str(e)})

        return Response(data)

    @action(methods=['GET'], detail=False)
    def generate_random_data(self, request):
        fake = Faker('en_US')

        domain_name = (
            EmailDomains.objects.values_list('domain_name', flat=True)
            .order_by('?')
            .first()
        )
        if not domain_name:
            return Response({'error': 'No email domains are available'})

        data = generate_data(fake, domain_name)

        return Response(data)
