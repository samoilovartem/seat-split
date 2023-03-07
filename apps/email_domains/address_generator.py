from faker import Faker

fake = Faker('en_US')

city = fake.city()
# state = 'CA'
state = fake.state_abbr()
# zip_code = fake.zipcode_in_state(state_abbr=state)
zip_code = fake.zipcode()

address = f"{fake.street_address()}, {city}, {state} {zip_code}"


first_name = fake.first_name()
last_name = fake.last_name()
email = f"{first_name.lower()}.{last_name.lower()}@example.com"

for _ in range(300):
    print(fake.state_abbr())
