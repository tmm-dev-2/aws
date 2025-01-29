import numpy as np
import pandas as pd
import requests
import sys
import json
import asyncio
from typing import Dict, List, Any
from scipy import stats

class RollingVWAPKosineP2Strategy:
    def __init__(self):
        # Kernel Regression Parameters
        self.lookback = 60
        self.tuning_coefficient = 15.0
        self.regression_type = "Tuneable"  # or "Stepped"

        # Indicator Setup
        self.indicators = {
            'RSI': {'enabled': True, 'length': 14},
            'Stochastic': {'enabled': True, 'length': 14},
            'BBPCT': {'enabled': True, 'length': 20},
            'CMO': {'enabled': True, 'length': 14},
            'CCI': {'enabled': True, 'length': 20},
            'Fisher': {'enabled': True, 'length': 9},
            'VZO': {'enabled': True, 'length': 21}
        }

        # Advanced Parameters
        self.trend_sensitivity = 0.1
        self.volatility_threshold = 0.5

    def cosine_kernel(self, x: float, z: float) -> float:
        """
        Compute cosine kernel with frequency tuning
        
        Args:
            x (float): Input value
            z (float): Frequency tuner
        
        Returns:
            float: Kernel value
        """
        y = np.cos(z * x)
        return np.abs(y) if np.abs(x) <= np.pi / (2 * z) else 0

    def kernel_regression(self, src: np.ndarray, lookback: int, tuning: float) -> np.ndarray:
        """
        Perform kernel regression with frequency tuning
        
        Args:
            src (np.ndarray): Source data
            lookback (int): Lookback period
            tuning (float): Tuning coefficient
        
        Returns:
            np.ndarray: Regression output
        """
        current_weight = np.zeros_like(src, dtype=float)
        total_weight = np.zeros_like(src, dtype=float)

        for i in range(min(lookback - 1, len(src))):
            y = src[i]
            w = self.cosine_kernel(i / lookback, tuning)
            current_weight[i] = y * w
            total_weight[i] = w

        return current_weight / total_weight

    def multi_cosine_regression(self, src: np.ndarray, lookback: int, steps: int) -> np.ndarray:
        """
        Perform multi-cosine kernel regression
        
        Args:
            src (np.ndarray): Source data
            lookback (int): Lookback period
            steps (int): Number of steps
        
        Returns:
            np.ndarray: Regression output
        """
        regression = np.zeros_like(src, dtype=float)
        for i in range(1, min(steps, len(src))):
            regression += self.kernel_regression(src, lookback, i)
        return regression / steps

    def calculate_rsi(self, close: np.ndarray, length: int) -> np.ndarray:
        """
        Calculate Relative Strength Index (RSI)
        
        Args:
            close (np.ndarray): Closing prices
            length (int): RSI calculation length
        
        Returns:
            np.ndarray: Rescaled RSI values
        """
        delta = np.diff(close)
        gain = np.where(delta > 0, delta, 0)
        loss = np.where(delta < 0, -delta, 0)
        
        avg_gain = pd.Series(gain).rolling(window=length).mean().values
        avg_loss = pd.Series(loss).rolling(window=length).mean().values
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        
        # Rescale RSI
        return (rsi - 50) * 2.8

    def calculate_stochastic(self, close: np.ndarray, high: np.ndarray, low: np.ndarray, length: int) -> np.ndarray:
        """
        Calculate Stochastic Oscillator
        
        Args:
            close (np.ndarray): Closing prices
            high (np.ndarray): High prices
            low (np.ndarray): Low prices
            length (int): Stochastic calculation length
        
        Returns:
            np.ndarray: Rescaled Stochastic values
        """
        lowest_low = pd.Series(low).rolling(window=length).min().values
        highest_high = pd.Series(high).rolling(window=length).max().values
        
        stochastic = 100 * (close - lowest_low) / (highest_high - lowest_low)
        return (stochastic - 50) * 2

    def calculate_bbpct(self, close: np.ndarray, length: int, multi: float = 2.0) -> np.ndarray:
        """
        Calculate Bollinger Bands Percentage
        
        Args:
            close (np.ndarray): Closing prices
            length (int): Calculation length
            multi (float): Standard deviation multiplier
        
        Returns:
            np.ndarray: Rescaled BBPCT values
        """
        basis = pd.Series(close).rolling(window=length).mean().values
        dev = multi * pd.Series(close).rolling(window=length).std().values
        
        upper = basis + dev
        lower = basis - dev
        bbpct = (close - lower) / (upper - lower)
        return (bbpct - 0.5) * 120

    def calculate_cmo(self, close: np.ndarray, length: int) -> np.ndarray:
        """
        Calculate Chande Momentum Oscillator
        
        Args:
            close (np.ndarray): Closing prices
            length (int): Calculation length
        
        Returns:
            np.ndarray: Rescaled CMO values
        """
        mom = np.diff(close)
        m1 = np.maximum(mom, 0)
        m2 = np.abs(np.minimum(mom, 0))
        
        sm1 = pd.Series(m1).rolling(window=length).sum().values
        sm2 = pd.Series(m2).rolling(window=length).sum().values
        
        cmo = 100 * (sm1 - sm2) / (sm1 + sm2)
        return cmo * 1.15

    def calculate_cci(self, close: np.ndarray, length: int) -> np.ndarray:
        """
        Calculate Commodity Channel Index
        
        Args:
            close (np.ndarray): Closing prices
            length (int): Calculation length
        
        Returns:
            np.ndarray: Rescaled CCI values
        """
        typical_price = close
        ma = pd.Series(typical_price).rolling(window=length).mean().values
        mad = pd.Series(np.abs(typical_price - ma)).rolling(window=length).mean().values
        
        cci = (typical_price - ma) / (0.015 * mad)
        return cci / 2

    def calculate_fisher_transform(self, close: np.ndarray, length: int) -> np.ndarray:
        """
        Calculate Fisher Transform
        
        Args:
            close (np.ndarray): Closing prices
            length (int): Calculation length
        
        Returns:
            np.ndarray: Rescaled Fisher Transform values
        """
        hl2 = (close + close) / 2
        lowest = pd.Series(hl2).rolling(window=length).min().values
        highest = pd.Series(hl2).rolling(window=length).max().values
        
        value = 0.66 * ((hl2 - lowest) / (highest - lowest) - 0.5)
        value = np.clip(value, -0.999, 0.999)
        
        fish = 0.5 * np.log((1 + value) / (1 - value))
        return fish * 30

    def calculate_vzo(self, close: np.ndarray, volume: np.ndarray, length: int) -> np.ndarray:
        """
        Calculate Volume Zone Oscillator
        
        Args:
            close (np.ndarray): Closing prices
            volume (np.ndarray): Trading volume
            length (int): Calculation length
        
        Returns:
            np.ndarray: Rescaled VZO values
        """
        price_change = np.sign(np.diff(close))
        vp = pd.Series(price_change * volume).rolling(window=length // 3).mean().values
        tv = pd.Series(volume).rolling(window=length // 3).mean().values
        
        return (vp / tv) * 110

    def calculate_indicators(self, data: Dict[str, np.ndarray]) -> Dict[str, np.ndarray]:
        """
        Calculate multiple technical indicators
        
        Args:
            data (Dict[str, np.ndarray]): Price and volume data
        
        Returns:
            Dict[str, np.ndarray]: Calculated indicator values
        """
        indicators = {}
        
        if self.indicators['RSI']['enabled']:
            indicators['RSI'] = self.calculate_rsi(
                data['close'], 
                self.indicators['RSI']['length']
            )
        
        if self.indicators['Stochastic']['enabled']:
            indicators['Stochastic'] = self.calculate_stochastic(
                data['close'], 
                data['high'], 
                data['low'], 
                self.indicators['Stochastic']['length']
            )
        
        if self.indicators['BBPCT']['enabled']:
            indicators['BBPCT'] = self.calculate_bbpct(
                data['close'], 
                self.indicators['BBPCT']['length']
            )
        
        if self.indicators['CMO']['enabled']:
            indicators['CMO'] = self.calculate_cmo(
                data['close'], 
                self.indicators['CMO']['length']
            )
        
        if self.indicators['CCI']['enabled']:
            indicators['CCI'] = self.calculate_cci(
                data['close'], 
                self.indicators['CCI']['length']
            )
        
        if self.indicators['Fisher']['enabled']:
            indicators['Fisher'] = self.calculate_fisher_transform(
                data['close'], 
                self.indicators['Fisher']['length']
            )
        
        if self.indicators['VZO']['enabled']:
            indicators['VZO'] = self.calculate_vzo(
                data['close'], 
                data['volume'], 
                self.indicators['VZO']['length']
            )
        
        return indicators

    async def fetch_candle_data(self, symbol: str, timeframe: str) -> Dict[str, List[float]]:
        """
        Fetch candle data from API
        
        Args:
            symbol (str): Trading symbol
            timeframe (str): Timeframe for data
        
        Returns:
            Dict[str, List[float]]: Candle data
        """
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
                'volume': [candle['volume'] for candle in data],
                'time': [candle['time'] for candle in data]
            }
        except Exception as e:
            print(f"Error fetching candle data: {e}")
            return {'open': [], 'high': [], 'low': [], 'close': [], 'volume': [], 'time': []}

    def calculate_strategy(self, data: Dict[str, List[float]]) -> Dict[str, Any]:
        """
        Main strategy calculation method
        
        Args:
            data (Dict[str, List[float]]): Candle data
        
        Returns:
            Dict[str, Any]: Strategy results
        """
        # Convert data to numpy arrays
        closes = np.array(data['close'])
        
        # Calculate indicators
        indicators = self.calculate_indicators(
            {k: np.array(data[k]) for k in ['close', 'high', 'low', 'volume']}
        )
        
        # Combine indicators
        active_indicators = [ind for ind in indicators.values() if ind is not None]
        combined_indicator = np.mean(active_indicators, axis=0)
        
        # Kernel regression
        if self.regression_type == "Tuneable":
            out = self.kernel_regression(combined_indicator, self.lookback, self.tuning_coefficient)
            out2 = self.kernel_regression(combined_indicator, self.lookback, self.tuning_coefficient / 5)
        else:
            out = self.multi_cosine_regression(combined_indicator, self.lookback, int(self.tuning_coefficient))
            out2 = self.multi_cosine_regression(combined_indicator, self.lookback, int(self.tuning_coefficient / 5))
        
        # Signal generation
        fast_trend_up = (out > out[1]) & (out[1] <= out[2])
        fast_trend_down = (out < out[1]) & (out[1] >= out[2])
        slow_trend_up = (out2 > 0) & (out2[1] <= 0)
        slow_trend_down = (out2 < 0) & (out2[1] >= 0)
        
        return {
            'out': out.tolist(),
            'out2': out2.tolist(),
            'fast_trend_up': fast_trend_up.tolist(),
            'fast_trend_down': fast_trend_down.tolist(),
            'slow_trend_up': slow_trend_up.tolist(),
            'slow_trend_down': slow_trend_down.tolist(),
            'indicators': {k: v.tolist() for k, v in indicators.items()},
            'timestamps': data['time'],
            'visualization': {
                'colors': {
                    'up': '#5ffae0',
                    'down': '#c22ed0',
                    'neutral': '#495057'
                }
            }
        }

def main():
    if len(sys.argv) != 3:
        print("Usage: python script.py <symbol> <timeframe>")
        sys.exit(1)

    symbol = sys.argv[1]
    timeframe = sys.argv[2]

    strategy = RollingVWAPKosineP2Strategy()
    candle_data = asyncio.run(strategy.fetch_candle_data(symbol, timeframe))
    result = strategy.calculate_strategy(candle_data)
    
    print(json.dumps(result))

if __name__ == "__main__":
    main()