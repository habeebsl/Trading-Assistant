import requests, json, pprint
from datetime import datetime
import pandas, ta
import time


import coinmarketcapTest, coingeckotest

def percentage(num, total):
    division_by_total = num/total
    return round(division_by_total*100)

print()
print(coinmarketcapTest.coin_price)
print(coinmarketcapTest.price_update_time+"\n")

df=pandas.DataFrame(coingeckotest.ohlc_data)
df.columns = ['timeframe', 'open', 'high', 'low', 'close']


df['RSI'] = ta.momentum.RSIIndicator(df['close'], window=len(df)).rsi()


rsi_value=df.loc[len(df)-1, 'RSI']
print("***RSI***")
print(f"RSI VALUE - {rsi_value}")
print("RSI VALUE INDICATION - ", end="")
if rsi_value > 70:
    print("overbought - Bearish")
elif rsi_value < 30:
    print("Oversold - Bullish")
else:
    print("Neither overbought or oversold - Can go either way")


df['SMA'] = ta.trend.sma_indicator(df['close'], window=3)
df['EMA'] = ta.trend.ema_indicator(df['close'], window=3)

df['is_uptrendsma'] = df['close'] > df['SMA']
df['is_uptrendema'] = df['close'] > df['EMA']

uptrend_or_sma=df['is_uptrendsma'].sum()
uptrend_or_ema=df['is_uptrendema'].sum()

print("\n***SMA***")
if percentage(uptrend_or_sma, len(df['SMA'])) > 60:
    print(df['is_uptrendsma'])
    print(f"Closing price was above the SMA {percentage(uptrend_or_sma, len(df['SMA']))}% of the time")
    print("Uptrend Indication")
else:
    print(f"Closing price was above the SMA {percentage(uptrend_or_sma, len(df['SMA']))}% of the time")
    print("Downtrend Indication")


print("\n***EMA***")
if percentage(uptrend_or_ema, len(df['EMA'])) > 60:
    print(df['is_uptrendema'])
    print(f"Closing price was above the EMA {percentage(uptrend_or_ema, len(df['EMA']))}% of the time")
    print("Uptrend Indication")
else:
    print(f"Closing price was above the EMA {percentage(uptrend_or_ema, len(df['EMA']))}% of the time")
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
    
    