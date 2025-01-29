import numpy as np
import pandas as pd
import requests
import sys
import json
from typing import Dict, List, Any, Tuple
from scipy import stats

class SupportResistanceBlackflagStrategy:
    def __init__(self):
        # Strategy Parameters from PineScript
        self.trail_type = 'modified'
        self.atr_period = 28
        self.atr_factor = 5
        self.show_fib_entries = False
        
        # Wilders Moving Average parameters
        self.wild_ma_length = 14
        
        # Colors
        self.col_up = '#00ff00'  # lime
        self.col_down = '#ff0000'  # red
        self.col_neutral = '#808080'  # gray
        
        # Additional parameters
        self.key_value = 3
        self.atr_period_trailing = 5
        self.use_heikin_ashi = False
        
        # Fibonacci specific parameters
        self.fib_levels = [61.8, 78.6, 88.6]
        
        # Additional indicator parameters
        self.rsi_length = 14
        self.stoch_length = 14
        self.macd_fast = 12
        self.macd_slow = 26
        self.macd_signal = 9

    def wilders_ma(self, src: np.ndarray, length: int) -> np.ndarray:
        """Implement Wilder's Moving Average"""
        wild = np.zeros_like(src, dtype=float)
        wild[0] = src[0]
        
        for i in range(1, len(src)):
            wild[i] = wild[i-1] + (src[i] - wild[i-1]) / length
        
        return wild

    def calculate_true_range(self, high: np.ndarray, low: np.ndarray, close: np.ndarray) -> np.ndarray:
        """Calculate True Range with modified and unmodified versions"""
        prev_close = np.roll(close, 1)
        prev_close[0] = close[0]
        
        hilo = np.minimum(high - low, 1.5 * np.mean(high - low))
        
        href = np.where(low <= high[:-1], 
                        high[1:] - close[:-1], 
                        high[1:] - close[:-1] - 0.5 * (low[1:] - high[:-1]))
        
        lref = np.where(high >= low[:-1], 
                        close[:-1] - low[1:], 
                        close[:-1] - low[1:] - 0.5 * (low[:-1] - high[1:]))
        
        if self.trail_type == 'modified':
            true_range = np.maximum(np.maximum(hilo, href), lref)
        else:
            true_range = np.maximum(np.maximum(high - low, np.abs(high - prev_close)), np.abs(low - prev_close))
        
        return true_range

    def calculate_atr(self, high: np.ndarray, low: np.ndarray, close: np.ndarray, period: int) -> np.ndarray:
        """Calculate Average True Range"""
        tr = self.calculate_true_range(high, low, close)
        return pd.Series(tr).rolling(window=period).mean().values

    def calculate_rsi(self, close: np.ndarray, length: int) -> np.ndarray:
        """Calculate Relative Strength Index"""
        delta = np.diff(close)
        gain = (delta > 0) * delta
        loss = (delta < 0) * -delta
        
        avg_gain = pd.Series(gain).rolling(window=length, min_periods=1).mean().values
        avg_loss = pd.Series(loss).rolling(window=length, min_periods=1).mean().values
        
        rs = avg_gain / (avg_loss + 1e-10)
        rsi = 100 - (100 / (1 + rs))
        
        return np.concatenate(([50], rsi))  # First value as 50 for initialization

    def calculate_stochastic(self, close: np.ndarray, high: np.ndarray, low: np.ndarray, length: int) -> Dict[str, np.ndarray]:
        """Calculate Stochastic Oscillator"""
        lowest_low = pd.Series(low).rolling(window=length).min().values
        highest_high = pd.Series(high).rolling(window=length).max().values
        
        stoch_k = 100 * (close - lowest_low) / (highest_high - lowest_low + 1e-10)
        stoch_d = pd.Series(stoch_k).rolling(window=3).mean().values
        
        return {
            'k': stoch_k,
            'd': stoch_d
        }

    def calculate_macd(self, close: np.ndarray, fast: int, slow: int, signal: int) -> Dict[str, np.ndarray]:
        """Calculate MACD Indicator"""
        fast_ema = pd.Series(close).ewm(span=fast, adjust=False).mean().values
        slow_ema = pd.Series(close).ewm(span=slow, adjust=False).mean().values
        
        macd_line = fast_ema - slow_ema
        signal_line = pd.Series(macd_line).ewm(span=signal, adjust=False).mean().values
        
        return {
            'macd': macd_line,
            'signal': signal_line,
            'histogram': macd_line - signal_line
        }

    def calculate_trend_and_trailing_stop(self, close: np.ndarray) -> Dict[str, Any]:
        """Calculate Trend and Trailing Stop with Enhanced Logic"""
        loss = self.atr_factor * self.wilders_ma(self.calculate_true_range(close, close, close), self.atr_period)
        
        up = close - loss
        dn = close + loss
        
        trend_up = np.zeros_like(close)
        trend_down = np.zeros_like(close)
        trend = np.ones_like(close, dtype=int)
        
        trend_up[0] = up[0]
        trend_down[0] = dn[0]
        
        for i in range(1, len(close)):
            # Trend Up calculation
            trend_up[i] = close[i-1] > trend_up[i-1] and close[i] > trend_up[i-1] \
                          and up[i] > trend_up[i-1] \
                          and up[i] or up[i]
            
            # Trend Down calculation
            trend_down[i] = close[i-1] < trend_down[i-1] and close[i] < trend_down[i-1] \
                            and dn[i] < trend_down[i-1] \
                            and dn[i] or dn[i]
            
            # Trend determination
            trend[i] = 1 if close[i] > trend_down[i-1] else -1 if close[i] < trend_up[i-1] else trend[i-1]
        
        # Trailing stop calculation
        trail = np.where(trend == 1, trend_up, trend_down)
        
        # Extremum calculation
        ex = np.zeros_like(close)
        ex[0] = close[0]
        
        for i in range(1, len(close)):
            if trend[i] == 1:
                ex[i] = max(ex[i-1], close[i])
            elif trend[i] == -1:
                ex[i] = min(ex[i-1], close[i])
            else:
                ex[i] = ex[i-1]
        
        return {
            'trailing_stop': trail,
            'trend': trend,
            'extremum': ex
        }

    def calculate_fibonacci_levels(self, ex: float, trail: float) -> Dict[str, float]:
        """Calculate Fibonacci Levels with Enhanced Logic"""
        levels = {}
        for i, level in enumerate(self.fib_levels):
            key = f'f{i+1}'
            levels[key] = ex + (trail - ex) * level / 100
        
        levels['l100'] = trail
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
        """Main calculation function with comprehensive strategy logic"""
        # Ensure all data is converted to numpy arrays
        opens = np.array(data['open'])
        highs = np.array(data['high'])
        lows = np.array(data['low'])
        closes = np.array(data['close'])
        volumes = np.array(data['volume'])
        timestamps = np.array(data['time'])
        
        if len(closes) == 0:
            return {}
        
        # Calculate trend, trailing stop, and extremum
        trend_data = self.calculate_trend_and_trailing_stop(closes)
        
        # Determine state (long/short)
        state = ['long' if t == 1 else 'short' for t in trend_data['trend']]
        
        # Calculate Fibonacci levels for the last point
        last_index = len(closes) - 1
        fib_levels = self.calculate_fibonacci_levels(
            trend_data['extremum'][last_index], 
            trend_data['trailing_stop'][last_index]
        )
        
        # Prepare Fibonacci entry signals
        fib_entries = {
            'l1': any(closes[i] < fib_levels['f1'] for i in range(len(closes))),
            'l2': any(closes[i] < fib_levels['f2'] for i in range(len(closes))),
            'l3': any(closes[i] < fib_levels['f3'] for i in range(len(closes))),
            's1': any(closes[i] > fib_levels['f1'] for i in range(len(closes))),
            's2': any(closes[i] > fib_levels['f2'] for i in range(len(closes))),
            's3': any(closes[i] > fib_levels['f3'] for i in range(len(closes)))
        }
        
        # Calculate additional indicators
        rsi = self.calculate_rsi(closes, self.rsi_length)
        stoch = self.calculate_stochastic(closes, highs, lows, self.stoch_length)
        macd = self.calculate_macd(closes, self.macd_fast, self.macd_slow, self.macd_signal)
        
        return {
            'open': opens.tolist(),
            'high': highs.tolist(),
            'low': lows.tolist(),
            'close': closes.tolist(),
            'volume': volumes.tolist(),
            'trailing_stop': trend_data['trailing_stop'].tolist(),
            'trend': trend_data['trend'].tolist(),
            'extremum': trend_data['extremum'].tolist(),
            'state': state,
            'fibonacci_levels': list(fib_levels.values()),
            'fibonacci_entry_signals': fib_entries,
            'rsi': rsi.tolist(),
            'stochastic': {
                'k': stoch['k'].tolist(),
                'd': stoch['d'].tolist()
            },
            'macd': {
                'line': macd['macd'].tolist(),
                'signal': macd['signal'].tolist(),
                'histogram': macd['histogram'].tolist()
            },
            'timestamps': timestamps.tolist(),
            'visualization': {
                'colors': {
                    'up': self.col_up,
                    'down': self.col_down,
                    'neutral': self.col_neutral
                }
            }
        }

async def main():
    if len(sys.argv) != 3:
        print("Usage: script.py <symbol> <timeframe>")
        sys.exit(1)

    symbol = sys.argv[1]
    timeframe = sys.argv[2]
    
    strategy = SupportResistanceBlackflagStrategy()
    data = await strategy.fetch_candle_data(symbol, timeframe)
    result = strategy.calculate_strategy(data)
    print(json.dumps(result))

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())