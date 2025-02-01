import numpy as np
import pandas as pd
import requests
import asyncio
import sys
import json
from typing import Dict, List, Any

class DonchianSqueezeMomentumStrategy:
    def __init__(self):
        # Strategy Parameters from PineScript
        self.length = 50
        self.mult = 3.0
        self.atr_period = 14
        self.con = 1
        self.colors = {
            'up': '#00ffbb',
            'down': '#ff1100',
            'neutral': '#808080',
            'basis_up': '#00ffbb',
            'basis_down': '#ff1100',
            'cloud_up': 'rgba(0, 255, 187, 0.3)',
            'cloud_down': 'rgba(255, 17, 0, 0.3)',
            'cloud_neutral': 'rgba(128, 128, 128, 0.3)'
        }

    async def fetch_candle_data(self, symbol: str, timeframe: str) -> Dict[str, List[float]]:
        """Fetch candle data from the API"""
        try:
            response = requests.get(
                'http://localhost:5000/fetch_candles',
                params={'symbol': symbol, 'timeframe': timeframe}
            )
            response.raise_for_status()
            data = response.json()
            
            return {
                'open': [candle['open'] for candle in data],
                'high': [candle['high'] for candle in data],
                'low': [candle['low'] for candle in data],
                'close': [candle['close'] for candle in data],
                'volume': [candle.get('volume', 0) for candle in data],
                'time': [candle['time'] for candle in data]
            }
        except Exception as e:
            print(f"Error fetching candle data: {e}")
            return {'open': [], 'high': [], 'low': [], 'close': [], 'volume': [], 'time': []}

    def calculate_donchian_channels(self, highs: np.ndarray, lows: np.ndarray) -> tuple:
        """Calculate Donchian Channel components"""
        highest = pd.Series(highs).rolling(window=self.length).max().values
        lowest = pd.Series(lows).rolling(window=self.length).min().values
        basis = (highest + lowest) / 2
        return highest, lowest, basis

    def calculate_atr(self, high: np.ndarray, low: np.ndarray, close: np.ndarray) -> np.ndarray:
        """Calculate Average True Range"""
        high_low = high - low
        high_close = np.abs(high - np.roll(close, 1))
        low_close = np.abs(low - np.roll(close, 1))
        
        ranges = np.vstack([high_low, high_close, low_close])
        true_range = np.max(ranges, axis=0)
        true_range[0] = ranges[0, 0]
        
        return pd.Series(true_range).rolling(window=self.atr_period).mean().values

    def calculate_standard_deviation(self, close: np.ndarray) -> np.ndarray:
        """Calculate Standard Deviation"""
        return pd.Series(close).rolling(window=self.length).std().values

    def calculate_crossovers(self, series1: np.ndarray, series2: np.ndarray) -> tuple:
        """Calculate crossover and crossunder signals"""
        crossover = (series1[:-1] <= series2[:-1]) & (series1[1:] > series2[1:])
        crossunder = (series1[:-1] >= series2[:-1]) & (series1[1:] < series2[1:])
        return np.append(crossover, False), np.append(crossunder, False)

    def calculate_strategy(self, data: Dict[str, List[float]]) -> Dict[str, Any]:
        """Main calculation function"""
        closes = np.array(data['close'])
        highs = np.array(data['high'])
        lows = np.array(data['low'])
        timestamps = np.array(data['time'])

        # Calculate Donchian Channel components
        highest, lowest, basis = self.calculate_donchian_channels(highs, lows)

        # Calculate Standard Deviation and ATR
        stdev = self.calculate_standard_deviation(closes)
        dev = stdev * self.mult
        vol = self.calculate_atr(highs, lows, closes)

        # Initialize arrays for fbasis and range
        fbasis = np.zeros_like(closes)
        range_values = np.zeros_like(closes)

        # Calculate fbasis and range with memory
        for i in range(len(closes)):
            if i == 0:
                fbasis[i] = basis[i]
                range_values[i] = dev[i]
            else:
                fbasis[i] = fbasis[i-1] if basis[i] == basis[i-self.con] else basis[i]
                range_values[i] = range_values[i-1] if fbasis[i] == fbasis[i-1] else dev[i]

        # Calculate all bands
        upper = fbasis + range_values
        lower = fbasis - range_values
        fu = fbasis + vol
        fl = fbasis - vol
        uu = upper + vol
        ul = upper - vol
        lu = lower + vol
        ll = lower - vol

        # Calculate crossover signals
        strong_long = np.zeros_like(closes, dtype=bool)
        strong_short = np.zeros_like(closes, dtype=bool)
        weak_long = np.zeros_like(closes, dtype=bool)
        weak_short = np.zeros_like(closes, dtype=bool)

        for i in range(1, len(closes)):
            strong_long[i] = closes[i-1] >= uu[i-1] and closes[i] < uu[i]
            strong_short[i] = closes[i-1] <= ll[i-1] and closes[i] > ll[i]
            weak_long[i] = (closes[i-1] >= ul[i-1] and closes[i] < ul[i]) and not strong_long[i]
            weak_short[i] = (closes[i-1] <= lu[i-1] and closes[i] > lu[i]) and not strong_short[i]

        # Calculate trend
        trend = np.where(closes > fbasis, 1, -1)

        # Calculate additional signals for plotting
        bullish_shift, bearish_shift = self.calculate_crossovers(closes, fbasis)

        return {
            'basis': fbasis.tolist(),
            'upper': upper.tolist(),
            'lower': lower.tolist(),
            'upper_vol': uu.tolist(),
            'lower_vol': ll.tolist(),
            'upper_inner': ul.tolist(),
            'lower_inner': lu.tolist(),
            'fu': fu.tolist(),
            'fl': fl.tolist(),
            'strong_long': strong_long.tolist(),
            'strong_short': strong_short.tolist(),
            'weak_long': weak_long.tolist(),
            'weak_short': weak_short.tolist(),
            'trend': trend.tolist(),
            'bullish_shift': bullish_shift.tolist(),
            'bearish_shift': bearish_shift.tolist(),
            'timestamps': timestamps.tolist(),
            'visualization': {
                'colors': self.colors,
                'styles': {
                    'basis': {'lineWidth': 2},
                    'bands': {'lineWidth': 1, 'style': 'dashed'},
                    'volatility': {'lineWidth': 1, 'style': 'dotted'},
                    'signals': {'size': 'tiny'}
                }
            }
        }

async def main():
    if len(sys.argv) != 3:
        print("Usage: python script.py <symbol> <timeframe>")
        sys.exit(1)

    symbol = sys.argv[1]
    timeframe = sys.argv[2]

    strategy = DonchianSqueezeMomentumStrategy()
    
    # Fetch candle data
    candle_data = await strategy.fetch_candle_data(symbol, timeframe)
    
    if not candle_data['close']:
        print(json.dumps({"error": "No data available"}))
        sys.exit(1)

    # Calculate strategy results
    results = strategy.calculate_strategy(candle_data)
    
    # Print results as JSON
    print(json.dumps(results))

if __name__ == "__main__":
    asyncio.run(main())