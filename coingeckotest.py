import requests, json, pprint
from datetime import datetime
import pandas, ta
import crypto_stuff

def percentage(num, total):
    division_by_total = num/total
    return division_by_total*100

print(crypto_stuff.coin_price)
print(crypto_stuff.price_update_time+"\n")

get_coin_info = requests.get("https://api.coingecko.com/api/v3/coins/ripple/ohlc?vs_currency=NGN&days=30")
status = get_coin_info.status_code

convert = get_coin_info.text
# pprint.pprint(json.loads(convert))

ohlc_data = json.loads(convert)
df=pandas.DataFrame(ohlc_data)
df.columns = ['timeframe', 'open', 'high', 'low', 'close']


df['RSI'] = ta.momentum.RSIIndicator(df['close'], window=len(df)).rsi()


rsi_value=df.loc[len(df)-1, 'RSI']
print("***RSI***")
if rsi_value > 70:
    print("overbought - Bearish")
elif rsi_value < 30:
    print("Oversold - Bullish")
else:
    print("Neither overbought or oversold - Can go either way")
print(rsi_value)

df['SMA'] = ta.trend.sma_indicator(df['close'], window=3)
df['EMA'] = ta.trend.ema_indicator(df['close'], window=3)

df['is_uptrendsma'] = df['close'] > df['SMA']
df['is_uptrendema'] = df['close'] > df['EMA']

uptrend_or_sma=df['is_uptrendsma'].sum()
uptrend_or_ema=df['is_uptrendema'].sum()

print("\n***SMA***")
if percentage(uptrend_or_sma, len(df['SMA'])) > 60:
    print(df['is_uptrendsma'])
    print(df['is_uptrendsma'].sum())
    print("Uptrend Indication")
else:
    print(percentage(uptrend_or_sma, len(df['SMA'])))
    print("Downtrend Indication")


print("\n***EMA***")
if percentage(uptrend_or_ema, len(df['EMA'])) > 60:
    print(df['is_uptrendema'])
    print(df['is_uptrendema'].sum())
    print("Uptrend Indication")
else:
    print(percentage(uptrend_or_ema, len(df['EMA'])))
    print("Downtrend Indication")

df['macd'] = ta.trend.macd(df['close'], window_slow=26, window_fast=12)

df['signal'] = ta.trend.macd_signal(df['close'], window_slow=26, window_fast=12, window_sign=9)

df['bullish_crossover'] = (df['macd'] > df['signal']) & (df['macd'].shift(1) <= df['signal'].shift(1))
df['bearish_crossover'] = (df['macd'] < df['signal']) & (df['macd'].shift(1) >= df['signal'].shift(1))


print("\n***MSAD***")
if df['bullish_crossover'].sum() > 0:
    bull_data = df[df['bullish_crossover']]
    print(f"\nbullish crossover happened {len(bull_data)} times\n")
    for i in range(len(bull_data)):
        print(f"- Bullish crossover happened at {pandas.to_datetime(bull_data['timeframe'].iat[i], unit='ms')}")
else:
    print("Zero Bullish crossovers detected")

if df['bearish_crossover'].sum() > 0:
    bear_data = df[df['bearish_crossover']]
    print(f"\nbearish crossover happened {len(bear_data)} times\n")
    for i in range(len(bear_data)):
        print(f"- Bearish crossover happened at {pandas.to_datetime(bear_data['timeframe'].iat[i], unit='ms')}")
else:
    print("Zero Bearish crossovers detected")
    
    




























# timestamps = [data[0] for data in ohlcv_data]

# # Calculate time differences
# time_diffs = [timestamps[i + 1] - timestamps[i] for i in range(len(timestamps) - 1)]

# # Convert time differences to datetime.timedelta objects for better readability
# time_diffs_readable = [datetime.timedelta(milliseconds=diff) for diff in time_diffs]

# # Print the results
# for i, diff in enumerate(time_diffs_readable, start=1):
#     print(f"Update {i}: {diff}")

# # Check if the time differences are consistent with a 30-minute interval
# consistent_interval = all(diff == datetime.timedelta(minutes=30) for diff in time_diffs_readable)
# print(f"Consistent 30-minute Interval: {consistent_interval}")