from json import dumps

import requests
from settings import settings

GOOD_ACCOUNT_EXAMPLE = 508883
GOOD_USERNAME_EXAMPLE = 'aliceparkerson111@gmail.com'

response = requests.get(
    url=f'{settings.get_seatscouts_accounts_endpoint}{GOOD_ACCOUNT_EXAMPLE}',
    headers=settings.get_seatscouts_api_headers,
)

if __name__ == '__main__':
    print(dumps(response.json(), indent=4))
