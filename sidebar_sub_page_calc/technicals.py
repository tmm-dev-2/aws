import talib
import numpy as np
import json
import requests

def fetch_candle_data(symbol, timeframe):
    response = requests.get(f'http://localhost:5000/fetch_candles?symbol={symbol}&timeframe={timeframe}')
    return response.json()

def calculate_technicals(candle_data):
    close_prices = np.array([candle['close'] for candle in candle_data])
    high_prices = np.array([candle['high'] for candle in candle_data])
    low_prices = np.array([candle['low'] for candle in candle_data])
    
    technicals = {
        'moving_averages': {
            'SMA': {
                'SMA20': talib.SMA(close_prices, timeperiod=20).tolist(),
                'SMA50': talib.SMA(close_prices, timeperiod=50).tolist(),
                'SMA100': talib.SMA(close_prices, timeperiod=100).tolist(),
                'SMA200': talib.SMA(close_prices, timeperiod=200).tolist(),
            },
            'EMA': {
                'EMA20': talib.EMA(close_prices, timeperiod=20).tolist(),
                'EMA50': talib.EMA(close_prices, timeperiod=50).tolist(),
                'EMA100': talib.EMA(close_prices, timeperiod=100).tolist(),
                'EMA200': talib.EMA(close_prices, timeperiod=200).tolist(),
            },
        },
        'oscillators': {
            'RSI': talib.RSI(close_prices, timeperiod=14).tolist(),
            'MACD': {
                'macd': talib.MACD(close_prices)[0].tolist(),
                'signal': talib.MACD(close_prices)[1].tolist(),
                'hist': talib.MACD(close_prices)[2].tolist(),
            },
            'Stochastic': {
                'slowk': talib.STOCH(high_prices, low_prices, close_prices)[0].tolist(),
                'slowd': talib.STOCH(high_prices, low_prices, close_prices)[1].tolist(),
            },
            'CCI': talib.CCI(high_prices, low_prices, close_prices).tolist(),
            'ADX': talib.ADX(high_prices, low_prices, close_prices).tolist(),
            'Williams%R': talib.WILLR(high_prices, low_prices, close_prices).tolist(),
        }
    }
    
    return technicals

def save_technicals_to_json(symbol, timeframe):
    candle_data = fetch_candle_data(symbol, timeframe)
    technicals = calculate_technicals(candle_data)
    with open('technicals.json', 'w') as f:
        json.dump(technicals, f)




