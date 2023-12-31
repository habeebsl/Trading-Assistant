from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import datetime, pytz

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
  'start':'1',
  'limit':'5000',
  'sort':'price',
  'convert':'NGN'
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': open('coinMC.txt', 'r').read(),
}

session = Session()
session.headers.update(headers)

def find_index_by_name(data_list, target_id):
    for index, crypto_dict in enumerate(data_list):
        if crypto_dict.get("id") == target_id:
            return index
    return 'not found'

def convert_WAT(to_convert):
    utc_timezone = datetime.datetime.strptime(to_convert, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=pytz.UTC)
    wat_timezone = pytz.timezone("Africa/Lagos")
    return utc_timezone.astimezone(wat_timezone)

try:
  response = session.get(url, params=parameters)
  data = json.loads(response.text)
  target_crypto_id = 52
  index_of_coin = find_index_by_name(data["data"], target_crypto_id)
  coin_price=f"XRP PRICE - N{round(data['data'][index_of_coin]['quote']['NGN']['price'], 3)}"
  time=data['data'][1204]['quote']['NGN']['last_updated']
  
  converted_wat = convert_WAT(time)

  price_update_time=f'Price Was Last Updated - {converted_wat.strftime("%d/%m/%Y  %I:%M:%S %p")}'
except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)

