from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import coin_prop
import json

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/map'
parameters = {
  'start':'1',
  'limit':'1',
  'sort':'id',
  'symbol':coin_prop.coin_name[1]
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': open('coinMC.txt', 'r').read(),
}

session = Session()
session.headers.update(headers)

try:
  response = session.get(url, params=parameters)
  data = json.loads(response.text)
  found_id=data['data'][0]['id']
except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)