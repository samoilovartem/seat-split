from apps.email_domains.models import EmailDomains
from apps.email_domains.services.data_generator import DataGenerator


def get_random_domain_name():
    domain_name = (
        EmailDomains.objects.values_list('domain_name', flat=True).order_by('?').first()
    )
    return domain_name


def generate_random_email_data(domain_name):
    generator = DataGenerator(domain_name)
    data = generator.generate_data()
    return data
