import numpy as np
import pandas as pd
import requests
import asyncio
import sys
import json
from typing import Dict, List, Any, Tuple
import scipy.stats as stats

class DonchianSqueezeMomentumP2Strategy:
    def __init__(self):
        # PineScript Strategy Parameters
        self.green = '#00ffbb'
        self.red = '#ff1100'
        
        # Momentum Settings
        self.len = 10
        self.Length = 20
        
        # Squeeze Settings
        self.periodForCalculation = 14
        self.lengthForSmoothing = 7
        self.lengthForEMA = 14
        self.lengthForHyperSqueezeDetection = 5
        
        # Divergence Settings
        self.lbL = 15
        self.lbR = 1
        self.plotBullish = True
        self.plotBear = True

    def _exponential_moving_average(self, data: np.ndarray, length: int) -> np.ndarray:
        """Calculate Exponential Moving Average"""
        weights = np.exp(np.linspace(-1., 0., length))
        weights /= weights.sum()
        return np.convolve(data, weights, mode='full')[:len(data)]

    def _simple_moving_average(self, data: np.ndarray, length: int) -> np.ndarray:
        """Calculate Simple Moving Average"""
        return pd.Series(data).rolling(window=length, min_periods=1).mean().values

    def _hull_moving_average(self, data: np.ndarray, length: int) -> np.ndarray:
        """Calculate Hull Moving Average"""
        sqrt_length = int(np.sqrt(length))
        wma_half = self._weighted_moving_average(data, length // 2)
        wma_full = self._weighted_moving_average(data, length)
        hull = self._weighted_moving_average(2 * wma_half - wma_full, sqrt_length)
        return hull

    def _weighted_moving_average(self, data: np.ndarray, length: int) -> np.ndarray:
        """Calculate Weighted Moving Average"""
        weights = np.arange(1, length + 1)
        wma = np.zeros_like(data)
        for i in range(length - 1, len(data)):
            wma[i] = np.dot(data[i-length+1:i+1], weights) / weights.sum()
        return wma

    def _rolling_lowest(self, data: np.ndarray, length: int) -> np.ndarray:
        """Calculate rolling lowest values"""
        return pd.Series(data).rolling(window=length, min_periods=1).min().values

    def _rolling_highest(self, data: np.ndarray, length: int) -> np.ndarray:
        """Calculate rolling highest values"""
        return pd.Series(data).rolling(window=length, min_periods=1).max().values

    def _rising(self, data: np.ndarray, length: int) -> np.ndarray:
        """Check if values are rising"""
        rising = np.zeros_like(data, dtype=bool)
        for i in range(length, len(data)):
            rising[i] = np.all(data[i-length:i] < data[i])
        return rising

    def _pivot_low(self, data: np.ndarray, left: int, right: int) -> np.ndarray:
        """Detect pivot lows"""
        pivots = np.zeros_like(data, dtype=bool)
        for i in range(left, len(data) - right):
            is_pivot = True
            for j in range(1, left + 1):
                if data[i] > data[i - j]:
                    is_pivot = False
                    break
            for j in range(1, right + 1):
                if data[i] > data[i + j]:
                    is_pivot = False
                    break
            pivots[i] = is_pivot
        return pivots

    def _pivot_high(self, data: np.ndarray, left: int, right: int) -> np.ndarray:
        """Detect pivot highs"""
        pivots = np.zeros_like(data, dtype=bool)
        for i in range(left, len(data) - right):
            is_pivot = True
            for j in range(1, left + 1):
                if data[i] < data[i - j]:
                    is_pivot = False
                    break
            for j in range(1, right + 1):
                if data[i] < data[i + j]:
                    is_pivot = False
                    break
            pivots[i] = is_pivot
        return pivots

    def _previous_pivot_low_index(self, pivots: np.ndarray, current_index: int) -> int:
        """Find previous pivot low index"""
        for i in range(current_index - 1, -1, -1):
            if pivots[i]:
                return i
        return None

    def _previous_pivot_high_index(self, pivots: np.ndarray, current_index: int) -> int:
        """Find previous pivot high index"""
        for i in range(current_index - 1, -1, -1):
            if pivots[i]:
                return i
        return None

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

    def calculate_volatility_indicators(self, high: np.ndarray, low: np.ndarray, close: np.ndarray) -> Dict[str, np.ndarray]:
        """Calculate volatility indicators similar to PineScript"""
        # Average True Range calculation
        tr = np.maximum(
            high - low, 
            np.abs(high - np.roll(close, 1)), 
            np.abs(low - np.roll(close, 1))
        )
        averageTrueRange = self._exponential_moving_average(tr, self.periodForCalculation)
        emaOfATR = self._exponential_moving_average(averageTrueRange, self.periodForCalculation * 2)
        volatilityIndicator = emaOfATR - averageTrueRange

        # EMA of High-Low Difference
        emaHighLowDifference = self._exponential_moving_average(high - low, self.periodForCalculation * 2)

        # Squeeze Value Calculation
        squeezeValue = self._exponential_moving_average(
            volatilityIndicator / (emaHighLowDifference + 1e-10) * 100, 
            self.lengthForSmoothing
        )
        squeezeValueMA = self._exponential_moving_average(squeezeValue, self.lengthForEMA)

        # Hypersqueeze Detection
        hypersqueeze = (squeezeValue > 0) & self._rising(squeezeValue, self.lengthForHyperSqueezeDetection)

        return {
            'volatilityIndicator': volatilityIndicator,
            'squeezeValue': squeezeValue,
            'squeezeValueMA': squeezeValueMA,
            'hypersqueeze': hypersqueeze
        }

    def calculate_momentum_oscillator(self, high: np.ndarray, low: np.ndarray, close: np.ndarray) -> Dict[str, np.ndarray]:
        """Calculate momentum oscillator components"""
        # EMA of lowest and highest
        l = self._exponential_moving_average(
            self._rolling_lowest(low, self.len), 
            self.len
        )
        h = self._exponential_moving_average(
            self._rolling_highest(high, self.len), 
            self.len
        )

        # Trend direction
        d = np.zeros_like(close, dtype=int)
        for i in range(1, len(close)):
            if close[i] > h[i-1]:
                d[i] = 1
            elif close[i] < l[i-1]:
                d[i] = -1
            else:
                d[i] = d[i-1]

        # Value calculation
        val = np.where(d == 1, l, h)
        val1 = close - val
        val2 = self._hull_moving_average(val1, self.len)
        vf = (val2 / (self._exponential_moving_average(high - low, self.len * 2) + 1e-10) * 100) / 8

        # Z-score calculation
        basis = self._simple_moving_average(vf, self.Length)
        zscore = (vf - basis) / (np.std(vf) + 1e-10)
        zscore = self._exponential_moving_average(zscore, self.Length) * 66

        return {
            'vf': vf,
            'zscore': zscore,
            'basis': basis
        }

    def detect_divergences(self, zscore: np.ndarray, close: np.ndarray, low: np.ndarray, high: np.ndarray) -> Dict[str, np.ndarray]:
        """Detect bullish and bearish divergences"""
        plFound = self._pivot_low(zscore, self.lbL, self.lbR)
        phFound = self._pivot_high(zscore, self.lbL, self.lbR)

        # Regular Bullish Divergence
        oscHL = np.zeros_like(zscore, dtype=bool)
        priceLL = np.zeros_like(zscore, dtype=bool)
        bullCond = np.zeros_like(zscore, dtype=bool)

        # Regular Bearish Divergence
        oscLH = np.zeros_like(zscore, dtype=bool)
        priceHH = np.zeros_like(zscore, dtype=bool)
        bearCond = np.zeros_like(zscore, dtype=bool)

        for i in range(len(zscore)):
            if plFound[i]:
                prev_low_index = self._previous_pivot_low_index(plFound, i)
                if prev_low_index is not None:
                    oscHL[i] = zscore[i] > zscore[prev_low_index]
                    priceLL[i] = low[i] < low[prev_low_index]
                    bullCond[i] = self.plotBullish and priceLL[i] and oscHL[i]

            if phFound[i]:
                prev_high_index = self._previous_pivot_high_index(phFound, i)
                if prev_high_index is not None:
                    oscLH[i] = zscore[i] < zscore[prev_high_index]
                    priceHH[i] = high[i] > high[prev_high_index]
                    bearCond[i] = self.plotBear and priceHH[i] and oscLH[i]

        return {
            'bullish_divergence': bullCond,
            'bearish_divergence': bearCond
        }

    def calculate_strategy(self, data: Dict[str, List[float]]) -> Dict[str, Any]:
        """Main strategy calculation"""
        closes = np.array(data['close'])
        highs = np.array(data['high'])
        lows = np.array(data['low'])
        timestamps = np.array(data['time'])

        # Calculate volatility indicators
        volatility = self.calculate_volatility_indicators(highs, lows, closes)

        # Calculate momentum oscillator
        momentum = self.calculate_momentum_oscillator(highs, lows, closes)

        # Detect divergences
        divergences = self.detect_divergences(momentum['zscore'], closes, lows, highs)

        # Additional Alerts and Conditions
        underlying_momentum_bullish = np.zeros_like(momentum['vf'], dtype=bool)
        underlying_momentum_bearish = np.zeros_like(momentum['vf'], dtype=bool)
        swing_momentum_bullish = np.zeros_like(momentum['zscore'], dtype=bool)
        swing_momentum_bearish = np.zeros_like(momentum['zscore'], dtype=bool)
        normal_squeeze = np.zeros_like(volatility['squeezeValue'], dtype=bool)

        for i in range(1, len(momentum['vf'])):
            underlying_momentum_bullish[i] = momentum['vf'][i-1] <= 0 and momentum['vf'][i] > 0
            underlying_momentum_bearish[i] = momentum['vf'][i-1] >= 0 and momentum['vf'][i] < 0
            swing_momentum_bullish[i] = momentum['zscore'][i-1] <= momentum['zscore'][i-1] and momentum['zscore'][i] > momentum['zscore'][i-1]
            swing_momentum_bearish[i] = momentum['zscore'][i-1] >= momentum['zscore'][i-1] and momentum['zscore'][i] < momentum['zscore'][i-1]
            normal_squeeze[i] = volatility['squeezeValueMA'][i-1] - volatility['squeezeValue'][i-1] < 0

        return {
            'close': closes.tolist(),
            'timestamps': timestamps.tolist(),
            'vf': momentum['vf'].tolist(),
            'zscore': momentum['zscore'].tolist(),
            'squeeze_value': volatility['squeezeValue'].tolist(),
            'squeeze_value_ma': volatility['squeezeValueMA'].tolist(),
            'hypersqueeze': volatility['hypersqueeze'].tolist(),
            'bullish_divergence': divergences['bullish_divergence'].tolist(),
            'bearish_divergence': divergences['bearish_divergence'].tolist(),
            'underlying_momentum_bullish': underlying_momentum_bullish.tolist(),
            'underlying_momentum_bearish': underlying_momentum_bearish.tolist(),
            'swing_momentum_bullish': swing_momentum_bullish.tolist(),
            'swing_momentum_bearish': swing_momentum_bearish.tolist(),
            'normal_squeeze': normal_squeeze.tolist(),
            'visualization': {
                'colors': {
                    'up': self.green,
                    'down': self.red
                }
            }
        }

async def main():
    if len(sys.argv) != 3:
        print("Usage: python script.py <symbol> <timeframe>")
        sys.exit(1)

    symbol = sys.argv[1]
    timeframe = sys.argv[2]

    strategy = DonchianSqueezeMomentumP2Strategy()
    candle_data = await strategy.fetch_candle_data(symbol, timeframe)
    
    if not candle_data['close']:
        print(json.dumps({"error": "No data available"}))
        sys.exit(1)
        results = strategy.calculate_strategy(candle_data)
        print(json.dumps(results))

if __name__ == "__main__":
    asyncio.run(main())