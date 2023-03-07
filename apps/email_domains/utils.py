from django.db.models import Count

from apps.email_domains.models import EmailDomains


def email_domains_per_value(filter_name):
    result = (
        EmailDomains.objects.values(filter_name)
        .order_by(filter_name)
        .annotate(count=Count(filter_name))
    )
    return result


def generate_data(fake, domain_name, state_abbr=None):
    first_name = fake.first_name()
    last_name = fake.last_name()
    email = f'{first_name.lower()}.{last_name.lower()}@{domain_name}'

    street_address = fake.street_address()
    city = fake.city()
    state = fake.state_abbr() if not state_abbr else state_abbr
    zip_code = (
        fake.zipcode() if not state_abbr else fake.zipcode_in_state(state_abbr=state)
    )

    full_address = f'{street_address}, {city}, {state} {zip_code}'

    data = {
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'address': full_address,
    }

    return data
