import csv
import os

import requests
from dotenv import find_dotenv, load_dotenv
from loguru import logger

load_dotenv(find_dotenv())


class AddressCollector:
    def __init__(
        self,
        url: str,
        state_code: str,
        headers: dict[str, str],
        file_name: str,
        status: list[str],
        sort: str,
        max_records: int = None,
    ):
        self.url = url
        self.headers = headers
        self.limit = 200
        self.state_code = state_code
        self.file_name = f'{self.state_code}_{file_name}.csv'
        self.max_records = max_records
        self.status = status
        self.sort = sort

    def fetch_addresses(self, offset: int = 0):
        payload = self._build_payload(offset)
        response = requests.post(self.url, json=payload, headers=self.headers)

        if response.headers.get('Content-Type') != 'application/json':
            logger.error('Unexpected content type at offset {}', offset)
            return {'data': {'home_search': {'total': 0, 'results': []}}}

        data = response.json()
        if data is None or data.get('data', None) is None:
            return {'data': {'home_search': {'total': 0, 'results': []}}}
        return data

    def _build_payload(self, offset: int):
        return {
            'limit': self.limit,
            'offset': offset,
            'state_code': self.state_code,
            'status': self.status,
            'type': [
                'condos',
                'condo_townhome_rowhome_coop',
                'condo_townhome',
                'townhomes',
                'duplex_triplex',
                'single_family',
                'multi_family',
                'apartment',
                'condop',
                'coop',
            ],
            'sort': {'direction': self.sort, 'field': 'list_date'},
        }

    def get_total_records(self):
        data = self.fetch_addresses(offset=0)
        total_records = data.get('data', {}).get('home_search', {}).get('total', 0)
        return total_records

    def collect_all_addresses(self):
        total_available_records = self.get_total_records()
        logger.info('Total available records: {}', total_available_records)

        offset = 0
        total_records = 0
        more_records = True
        fieldnames = [
            'city',
            'line',
            'street_name',
            'street_number',
            'street_suffix',
            'country',
            'postal_code',
            'state_code',
            'state',
            'latitude',
            'longitude',
        ]

        with open(self.file_name, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            while more_records:
                logger.info('Fetching records with offset: {}', offset)
                data = self.fetch_addresses(offset)
                total = data.get('data', {}).get('home_search', {}).get('total', 0)
                results = data.get('data', {}).get('home_search', {}).get('results', [])

                for result in results:
                    address_data = self._process_result(result)
                    if address_data:
                        writer.writerow(address_data)
                        total_records += 1

                        if self.max_records and total_records >= self.max_records:
                            more_records = False
                            break

                offset += self.limit

                if total_records >= total or (self.max_records and total_records >= self.max_records):
                    more_records = False

        logger.info('Saved {} addresses to {}', total_records, self.file_name)
        return total_records

    def _process_result(self, result):
        location = result.get('location', {})
        address = location.get('address', {})
        coordinate = address.get('coordinate', {})

        if not (coordinate and location and address):
            return None

        return {
            'city': address.get('city', ''),
            'line': address.get('line', ''),
            'street_name': address.get('street_name', ''),
            'street_number': address.get('street_number', ''),
            'street_suffix': address.get('street_suffix', ''),
            'country': address.get('country', ''),
            'postal_code': address.get('postal_code', ''),
            'state_code': address.get('state_code', ''),
            'state': address.get('state', ''),
            'latitude': coordinate.get('lat', ''),
            'longitude': coordinate.get('lon', ''),
        }


if __name__ == '__main__':
    api_url = os.environ.get('RAPID_API_URL')
    api_headers = {
        'content-type': 'application/json',
        'X-RapidAPI-Key': os.environ.get('RAPID_API_KEY'),
        'X-RapidAPI-Host': 'realty-in-us.p.rapidapi.com',
    }

    collector = AddressCollector(
        url=api_url,
        state_code='TX',
        headers=api_headers,
        file_name='addresses',
        max_records=20000,
        status=['for_rent'],
        sort='desc',
    )
    total_records = collector.collect_all_addresses()
    logger.info('Total records collected: {}', total_records)
