import os

import telnyx
from dotenv import load_dotenv

load_dotenv()

telnyx.api_key = os.environ.get('TELNYX_API_KEY')

user_balance = telnyx.Balance.retrieve()

print(user_balance)
