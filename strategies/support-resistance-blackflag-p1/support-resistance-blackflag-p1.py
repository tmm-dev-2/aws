import numpy as np
import pandas as pd
import requests
import sys
import json
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass

@dataclass
class PivotPoint:
    bar_index: int
    price: float
    type: str  # 'high' or 'low'
    strength: float  # Relative strength of the pivot

class SupportResistanceStrategy:
    def __init__(self):
        # Strategy Parameters from PineScript
        self.fade = 5
        self.left = 10
        self.right = 1
        self.show_pp = False
        self.opt = 'line'  # or 'value'
        
        # Colors
        self.col_up = '#00ff00'  # lime
        self.col_down = '#ff0000'  # red
        
        # SMA and other parameters
        self.lengths = {
            'sma1': 50, 'sma2': 100, 'sma3': 20,
            'len4': 20, 'len5': 20, 'len6': 20,
            'len7': 20, 'len8': 20, 'len9': 20
        }
        self.multipliers = {
            'mlt1': 2, 'mlt2': 2, 'mlt3': 2,
            'mlt4': 2, 'mlt5': 2, 'mlt6': 2,
            'mlt7': 2, 'mlt8': 2, 'mlt9': 2
        }
        self.timeframes = {
            'res1': 'D', 'res2': 'D', 'res3': 'W',
            'res4': 'W', 'res5': 'W', 'res6': 'D',
            'res7': 'D', 'res8': 'D', 'res9': 'W'
        }

    def calculate_pivot_points(self, high: np.ndarray, low: np.ndarray, close: np.ndarray) -> Tuple[List[PivotPoint], List[PivotPoint]]:
        """Calculate pivot high and low points with enhanced logic"""
        pivot_highs = []
        pivot_lows = []
        
        for i in range(self.left, len(high) - self.right):
            # Check for pivot high with strength calculation
            if all(high[i] > high[j] for j in range(i-self.left, i)) and \
               all(high[i] > high[j] for j in range(i+1, i+self.right+1)):
                strength = (high[i] - np.mean(high[max(0, i-self.left):min(len(high), i+self.right+1)])) / high[i]
                pivot_highs.append(PivotPoint(i, high[i], 'high', strength))
            
            # Check for pivot low with strength calculation
            if all(low[i] < low[j] for j in range(i-self.left, i)) and \
               all(low[i] < low[j] for j in range(i+1, i+self.right+1)):
                strength = (np.mean(low[max(0, i-self.left):min(len(low), i+self.right+1)]) - low[i]) / low[i]
                pivot_lows.append(PivotPoint(i, low[i], 'low', strength))
        
        return pivot_highs, pivot_lows

    def calculate_ema(self, data: np.ndarray, length: int) -> np.ndarray:
        """Calculate Exponential Moving Average"""
        return pd.Series(data).ewm(span=length, adjust=False).mean().values

    def calculate_sma(self, data: np.ndarray, length: int) -> np.ndarray:
        """Calculate Simple Moving Average with proper handling of NaN values"""
        sma = pd.Series(data).rolling(window=length, min_periods=1).mean().values
        return np.nan_to_num(sma, nan=data[0])

    def calculate_bollinger_bands(self, close: np.ndarray, length: int, mult: float) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Calculate Bollinger Bands with proper standard deviation"""
        sma = self.calculate_sma(close, length)
        std = pd.Series(close).rolling(window=length, min_periods=1).std(ddof=0).values
        std = np.nan_to_num(std, nan=0)
        
        upper = sma + (std * mult)
        lower = sma - (std * mult)
        return sma, upper, lower

    def calculate_breaks(self, price_level: float, close: np.ndarray, high: np.ndarray, low: np.ndarray) -> int:
        """Calculate number of breaks through a price level with enhanced accuracy"""
        breaks = 0
        position = 1  # 1 for above, 0 for below
        
        for i in range(len(close)):
            if position == 1:
                if low[i] < price_level:
                    breaks += 1
                    position = 0
            else:
                if high[i] > price_level:
                    position = 1
        
        return breaks

    def calculate_fibonacci_levels(self, high: float, low: float) -> List[float]:
        """Calculate Fibonacci retracement levels"""
        diff = high - low
        levels = [0.0, 0.236, 0.382, 0.5, 0.618, 0.786, 1.0]
        return [low + (level * diff) for level in levels]

    def calculate_support_resistance(self, pivot_points: List[PivotPoint], 
                                   close: np.ndarray, high: np.ndarray, low: np.ndarray,
                                   highest: float, lowest: float) -> List[dict]:
        """Calculate support and resistance levels with enhanced grading"""
        levels = []
        
        for pp in pivot_points:
            if lowest <= pp.price <= highest:
                breaks = self.calculate_breaks(pp.price, close, high, low)
                grade = min(100, round((100 / self.fade) * breaks))
                strength_factor = pp.strength * 100
                
                levels.append({
                    'price': pp.price,
                    'grade': grade,
                    'breaks': breaks,
                    'bar_index': pp.bar_index,
                    'strength': strength_factor,
                    'type': pp.type
                })
        
        # Sort levels by strength and grade
        levels.sort(key=lambda x: (x['strength'], x['grade']), reverse=True)
        return levels

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

    def calculate_strategy(self, data: Dict[str, List[float]]) -> Dict[str, Any]:
        """Main calculation function with enhanced logic"""
        # Convert to numpy arrays
        closes = np.array(data['close'])
        highs = np.array(data['high'])
        lows = np.array(data['low'])
        
        if len(closes) == 0:
            return {
                'support_levels': [],
                'resistance_levels': [],
                'sma_values': {},
                'bb_values': {},
                'timestamps': [],
                'visualization': {
                    'colors': {
                        'up': self.col_up,
                        'down': self.col_down,
                        'neutral': '#808080'
                    }
                }
            }
        
        # Calculate highest and lowest
        highest = np.max(highs)
        lowest = np.min(lows)
        
        # Calculate pivot points with enhanced logic
        pivot_highs, pivot_lows = self.calculate_pivot_points(highs, lows, closes)
        
        # Calculate support and resistance levels
        support_levels = self.calculate_support_resistance(pivot_lows, closes, highs, lows, highest, lowest)
        resistance_levels = self.calculate_support_resistance(pivot_highs, closes, highs, lows, highest, lowest)
        
        # Calculate SMAs and Bollinger Bands
        sma_values = {}
        bb_values = {}
        ema_values = {}
        fibonacci_levels = self.calculate_fibonacci_levels(highest, lowest)
        
        for i in range(1, 10):
            length = self.lengths[f'sma{i}']
            mult = self.multipliers[f'mlt{i}']
            
            sma_values[f'sma{i}'] = self.calculate_sma(closes, length).tolist()
            ema_values[f'ema{i}'] = self.calculate_ema(closes, length).tolist()
            sma, upper, lower = self.calculate_bollinger_bands(closes, length, mult)
            bb_values[f'bb{i}'] = {
                'upper': upper.tolist(),
                'lower': lower.tolist(),
                'middle': sma.tolist()
            }
        
        return {
            'support_levels': support_levels,
            'resistance_levels': resistance_levels,
            'sma_values': sma_values,
            'ema_values': ema_values,
            'bb_values': bb_values,
            'fibonacci_levels': fibonacci_levels,
            'pivot_points': {
                'highs': [(p.bar_index, p.price, p.strength) for p in pivot_highs],
                'lows': [(p.bar_index, p.price, p.strength) for p in pivot_lows]
            },
            'timestamps': data['time'],
            'candles': {
                'open': data['open'],
                'high': data['high'],
                'low': data['low'],
                'close': data['close'],
                'volume': data['volume'],
                'time': data['time']
            },
            'visualization': {
                'colors': {
                    'up': self.col_up,
                    'down': self.col_down,
                    'neutral': '#808080'
                }
            }
        }

async def main():
    if len(sys.argv) != 3:
        print("Usage: script.py <symbol> <timeframe>")
        sys.exit(1)

    symbol = sys.argv[1]
    timeframe = sys.argv[2]
    
    strategy = SupportResistanceStrategy()
    data = await strategy.fetch_candle_data(symbol, timeframe)
    result = strategy.calculate_strategy(data)
    print(json.dumps(result))

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())