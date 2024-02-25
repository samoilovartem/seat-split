import requests
from settings import settings

payload = {
    'vendorId': 436715,
    'tags': 'TEST',
    'lines': [
        {
            'quantity': 1,
            'description': 'test',
            'inventory': {
                'quantity': 1,
                'notes': 'test',
                'section': 'test',
                'row': 'test',
                'cost': 2,
                'lowSeat': 1,
                'highSeat': 2,
                'eventId': 4742113,
                'stockType': 'HARD',
                'seatType': 'CONSECUTIVE',
            },
        }
    ],
}

response = requests.post(
    settings.get_skybox_purchases_endpoint, headers=settings.get_skybox_api_headers, data=payload
)
print(response.content)
