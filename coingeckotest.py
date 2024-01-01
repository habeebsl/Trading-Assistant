import json, requests
import coin_prop

get_coin_info = requests.get(f"https://api.coingecko.com/api/v3/coins/{coin_prop.coin_name[0].lower()}/ohlc?vs_currency={coin_prop.currency_code}&days={coin_prop.ta_days}")
status = get_coin_info.status_code

convert = get_coin_info.text
# pprint.pprint(json.loads(convert))

ohlc_data = json.loads(convert)
