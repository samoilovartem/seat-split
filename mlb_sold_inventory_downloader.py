import pandas as pd
import requests

from config.settings.local import GILBERT_API_TOKEN

URL = f'https://api.lewanddowski.com/sold_inventory.php?token:{GILBERT_API_TOKEN}&eventDateFrom=2022-10' \
      '-19&eventDateTo=2023-12-31&includeTags=mlb_baseball&fulfillmentStatus=Pending&excludeTags=cancelledevent,' \
      'pending-offerupgrade'

response = requests.get(URL).json()

columns = {
    'inHandDate': 'in_hand_date',
    'eventId': 'event_id',
    'faceValue': 'face_value',
    'listPrice': 'list_price',
    'lastPriceUpdate': 'last_price_update',
    'unitCostAverage': 'unit_cost_average',
    'invoiceId': 'invoice_id',
    'invoiceDate': 'invoice_date',
    'fulfillmentStatus': 'fulfillment_status',
    'paymentStatus': 'payment_status',
    'profitMargin': 'profit_margin',
    'fulfillmentDate': 'fulfillment_date',
    'invoiceTags': 'invoice_tags',
    'unitTicketSales': 'unit_ticket_sales',
    'rowCount': 'row_count',
    'Tags': 'tags',
    'Customer': 'customer',
    'invoiceStatus': 'invoice_status',
    'purchaseIds': 'purchase_ids',
}

df = pd.DataFrame(response['data'])
df.rename(columns=columns, inplace=True)
df['last_price_update'] = df['last_price_update'].str[:10]
df.loc[df['fulfillment_date'] == '0000-00-00 00:00:00', 'fulfillment_date'] = ''
df.to_csv('response_python.csv')