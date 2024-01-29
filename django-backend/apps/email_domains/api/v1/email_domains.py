from apps.email_domains.services.data_generator import DataGenerator
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


@api_view(['POST'])
@permission_classes((AllowAny,))
def generate_random_data_with_provided_domain_or_state(request):
    domain_name = request.data.get('domain_name')
    state = request.data.get('state')

    if not domain_name:
        return Response({'error': 'Domain name is required'})

    generator = DataGenerator(domain_name, state)

    if not state:
        data = generator.generate_data()
        return Response(data)

    try:
        data = generator.generate_data()
    except Exception as e:
        return Response({'error': str(e)})

    return Response(data)
