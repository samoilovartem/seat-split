from random import choice, randint

from faker import Faker

from apps.accounts.models import Accounts


class DataGenerator:
    def __init__(self, domain_name: str, state_abbr: str = None):
        self.fake = Faker('en_US')
        self.domain_name = domain_name
        self.state_abbr = state_abbr

    @staticmethod
    def generate_transformed_name_parts(first_name: str, last_name: str):
        transformations = [
            (lambda s: s),
            (lambda s: s[0] if s else ''),
            (lambda s: f'.{s}' if s else ''),
        ]

        transformed_first = choice(transformations)(first_name.lower())
        transformed_last = choice(transformations)(last_name.lower())

        if transformed_first[0] == '.':
            transformed_first = transformed_first[1:]

        return transformed_first, transformed_last

    def generate_email(self, first_name: str, last_name: str):
        transformed_first, transformed_last = self.generate_transformed_name_parts(
            first_name, last_name
        )

        random_number = str(randint(1, 99999))
        if choice([True, False]):
            return f'{random_number}{transformed_first}{transformed_last}@{self.domain_name}'
        else:
            return f'{transformed_first}{transformed_last}{random_number}@{self.domain_name}'

    def generate_unique_email(self):
        while True:
            first_name = self.fake.first_name()
            last_name = self.fake.last_name()
            email = self.generate_email(first_name, last_name)
            if not Accounts.objects.filter(email=email).exists():
                break
        return first_name, last_name, email

    def generate_data(self):
        first_name, last_name, email = self.generate_unique_email()

        street_address = self.fake.street_address()
        city = self.fake.city()
        state = self.fake.state_abbr() if not self.state_abbr else self.state_abbr
        zip_code = (
            self.fake.zipcode()
            if not self.state_abbr
            else self.fake.zipcode_in_state(state_abbr=state)
        )

        full_address = f'{street_address}, {city}, {state} {zip_code}'

        data = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'address': full_address,
        }

        return data
