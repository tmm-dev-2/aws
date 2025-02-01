import numpy as np
import pandas as pd
import requests
from typing import Dict, List, Any
import sys
import json
import asyncio

class RollingVWAPKosineStrategy:
    def __init__(self):
        # Strategy Parameters
        self.lookback = 50
        self.band_mult_1 = 1.0
        self.band_mult_2 = 2.0
        self.band_mult_3 = 3.0
        self.use_rolling = True
        self.calc_mode = "Standard Deviation"
        
        # Advanced Parameters
        self.volatility_threshold = 0.5
        self.trend_sensitivity = 0.1

    def calculate_advanced_typical_price(self, high: np.ndarray, low: np.ndarray, close: np.ndarray) -> np.ndarray:
        """
        Advanced Typical Price Calculation with Weighted Components
        
        Combines multiple price components with exponential smoothing
        to create a more robust typical price measure
        """
        # Basic Typical Price
        hlc3 = (high + low + close) / 3
        
        # Weighted price calculation
        weighted_close = (
            0.6 * close +  # More weight to close price
            0.2 * high +   # Some weight to high price
            0.2 * low      # Some weight to low price
        )
        
        # Exponential smoothing
        alpha = 2 / (self.lookback + 1)
        smoothed_typical = np.zeros_like(hlc3)
        smoothed_typical[0] = hlc3[0]
        
        for i in range(1, len(hlc3)):
            smoothed_typical[i] = (
                alpha * weighted_close[i] + 
                (1 - alpha) * smoothed_typical[i-1]
            )
        
        return smoothed_typical

    def calculate_vwma(self, data: np.ndarray, volume: np.ndarray, length: int) -> np.ndarray:
        """
        Calculate Volume Weighted Moving Average
        
        Provides a volume-weighted average of prices
        """
        vwma = np.zeros_like(data)
        for i in range(length - 1, len(data)):
            window_prices = data[i-length+1:i+1]
            window_volume = volume[i-length+1:i+1]
            vwma[i] = np.sum(window_prices * window_volume) / np.sum(window_volume)
        return vwma

    def calculate_robust_vwap(self, typical_price: np.ndarray, volume: np.ndarray) -> np.ndarray:
        """
        Robust VWAP Calculation with Multiple Smoothing Techniques
        
        Provides a more sophisticated VWAP calculation that adapts to 
        market conditions
        """
        cumulative_price_volume = np.zeros_like(typical_price)
        cumulative_volume = np.zeros_like(volume)
        vwap = np.zeros_like(typical_price)
        
        for i in range(len(typical_price)):
            # Determine window start considering lookback
            window_start = max(0, i - self.lookback + 1)
            
            # Cumulative calculations
            cumulative_volume[i] = np.sum(volume[window_start:i+1])
            cumulative_price_volume[i] = np.sum(
                typical_price[window_start:i+1] * volume[window_start:i+1]
            )
            
            # Calculate VWAP with exponential smoothing
            if cumulative_volume[i] > 0:
                simple_vwap = cumulative_price_volume[i] / cumulative_volume[i]
                
                # Exponential smoothing factor
                alpha = 2 / (self.lookback + 1)
                
                # Apply smoothing
                if i > 0:
                    vwap[i] = alpha * simple_vwap + (1 - alpha) * vwap[i-1]
                else:
                    vwap[i] = simple_vwap
        
        return vwap

    def calculate_advanced_volatility(self, 
                                      typical_price: np.ndarray, 
                                      volume: np.ndarray, 
                                      vwap: np.ndarray) -> np.ndarray:
        """
        Advanced Volatility Calculation with Multiple Methods
        
        Combines volume-weighted variance and median absolute deviation
        to create a robust volatility measure
        """
        # Calculate squared differences from VWAP
        squared_diff = np.power(typical_price - vwap, 2)
        weighted_squared_diff = squared_diff * volume
        
        # Cumulative calculations
        cumulative_weighted_squared_diff = np.cumsum(weighted_squared_diff)
        cumulative_volume = np.cumsum(volume)
        
        # Initialize volatility array
        volatility = np.zeros_like(typical_price)
        
        for i in range(len(typical_price)):
            if cumulative_volume[i] > 0:
                # Volume-weighted variance
                vw_variance = cumulative_weighted_squared_diff[i] / cumulative_volume[i]
                
                # Median Absolute Deviation (MAD)
                mad_volatility = np.median(np.abs(typical_price[:i+1] - vwap[i]))
                
                # Combine methods with weighted average
                volatility[i] = np.sqrt(
                    0.7 * vw_variance + 
                    0.3 * mad_volatility**2
                )
        
        return volatility

    async def fetch_candle_data(self, symbol: str, timeframe: str) -> Dict[str, List[float]]:
        """
        Fetch candle data from the API with comprehensive error handling
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
        Comprehensive strategy calculation with advanced signal generation
        """
        # Convert input data to numpy arrays
        closes = np.array(data['close'])
        highs = np.array(data['high'])
        lows = np.array(data['low'])
        volumes = np.array(data['volume'])
        times = np.array(data['time'])

        # Advanced Calculations
        typical_price = self.calculate_advanced_typical_price(highs, lows, closes)
        vwap = self.calculate_robust_vwap(typical_price, volumes)
        volatility = self.calculate_advanced_volatility(typical_price, volumes, vwap)

        # Calculate bands
        band_basis = (
            volatility if self.calc_mode == "Standard Deviation" 
            else vwap * 0.01
        )
        
        # Dynamic multiplier adjustment
        dynamic_mult_1 = self.band_mult_1 * (1 + self.trend_sensitivity)
        dynamic_mult_2 = self.band_mult_2 * (1 + self.trend_sensitivity * 1.5)
        dynamic_mult_3 = self.band_mult_3 * (1 + self.trend_sensitivity * 2)

        # Calculate bands with dynamic multipliers
        upper_band1 = vwap + band_basis * dynamic_mult_1
        lower_band1 = vwap - band_basis * dynamic_mult_1
        upper_band2 = vwap + band_basis * dynamic_mult_2
        lower_band2 = vwap - band_basis * dynamic_mult_2
        upper_band3 = vwap + band_basis * dynamic_mult_3
        lower_band3 = vwap - band_basis * dynamic_mult_3

        # Advanced Signal Generation
        buy_signals = np.zeros_like(closes, dtype=bool)
        sell_signals = np.zeros_like(closes, dtype=bool)
        
        for i in range(1, len(closes)):
            # Advanced signal conditions
            vwap_cross_up = closes[i] > vwap[i] and closes[i-1] <= vwap[i-1]
            vwap_cross_down = closes[i] < vwap[i] and closes[i-1] >= vwap[i-1]
            
            # Volatility and trend filters
            volatility_filter = volatility[i] > self.volatility_threshold
            trend_confirmation = np.abs(closes[i] - vwap[i]) / vwap[i] > self.trend_sensitivity
            
            # Generate signals with multiple conditions
            buy_signals[i] = vwap_cross_up and volatility_filter and trend_confirmation
            sell_signals[i] = vwap_cross_down and volatility_filter and trend_confirmation

        # Comprehensive result dictionary
        return {
            'vwap': vwap.tolist(),
            'typical_price': typical_price.tolist(),
            'volatility': volatility.tolist(),
            'upper_band1': upper_band1.tolist(),
            'lower_band1': lower_band1.tolist(),
            'upper_band2': upper_band2.tolist(),
            'lower_band2': lower_band2.tolist(),
            'upper_band3': upper_band3.tolist(),
            'lower_band3': lower_band3.tolist(),
            'buy_signals': buy_signals.tolist(),
            'sell_signals': sell_signals.tolist(),
            'timestamps': times.tolist(),
            'visualization': {
                'colors': {
                    'up': '#5ffae0',
                    'down': '#c22ed0',
                    'neutral': '#495057'
                }
            }
        }

def main():
    """
    Main execution function for strategy
    Handles command-line arguments and runs the strategy
    """
    # Check if correct number of arguments are provided
    if len(sys.argv) != 3:
        print("Usage: python script.py <symbol> <timeframe>")
        sys.exit(1)

    symbol = sys.argv[1]
    timeframe = sys.argv[2]

    # Create strategy instance
    strategy = RollingVWAPKosineStrategy()

    # Fetch candle data
    import asyncio
    candle_data = asyncio.run(strategy.fetch_candle_data(symbol, timeframe))

    # Calculate strategy
    result = strategy.calculate_strategy(candle_data)

    # Print result as JSON
    import json
    print(json.dumps(result))

if __name__ == "__main__":
    main()