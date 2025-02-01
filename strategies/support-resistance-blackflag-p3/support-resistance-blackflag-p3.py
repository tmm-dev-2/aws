import numpy as np
import pandas as pd
import requests
import sys
import json
from typing import Dict, List, Any, Tuple
import math
from scipy import stats

class SupportResistanceBlackflagP3Strategy:
    def __init__(self):
        # MFI Settings
        self.src_type = 'hlc3'
        self.mfi_length = 14
        
        # K-means Clustering Settings
        self.length = 300
        self.iterations = 5
        self.overbought = 80.0
        self.neutral = 50.0
        self.oversold = 20.0
        
        # Advanced Indicator Parameters
        self.rsi_length = 14
        self.stoch_length = 14
        self.macd_fast = 12
        self.macd_slow = 26
        self.macd_signal = 9
        self.atr_length = 14
        
        # Appearance Settings
        self.adj = True
        self.mlt = 1.0
        self.green = '#00ffbb'
        self.red = '#ff1100'
        
        # Additional Strategy Parameters
        self.volatility_threshold = 1.5
        self.trend_strength_threshold = 0.7
        self.reversal_sensitivity = 0.5

    def calculate_mfi(self, data: Dict[str, List[float]]) -> np.ndarray:
        """Calculate Money Flow Index"""
        close = np.array(data['close'])
        high = np.array(data['high'])
        low = np.array(data['low'])
        volume = np.array(data['volume'])
        
        # Calculate typical price
        typical_price = (high + low + close) / 3
        
        # Calculate raw money flow
        money_flow = typical_price * volume
        
        # Calculate positive and negative money flow
        positive_flow = np.zeros_like(money_flow)
        negative_flow = np.zeros_like(money_flow)
        
        for i in range(1, len(typical_price)):
            if typical_price[i] > typical_price[i-1]:
                positive_flow[i] = money_flow[i]
            else:
                negative_flow[i] = money_flow[i]
        
        # Calculate money flow ratio
        positive_mf_sum = np.zeros_like(money_flow)
        negative_mf_sum = np.zeros_like(money_flow)
        
        for i in range(self.mfi_length, len(money_flow)):
            positive_mf_sum[i] = np.sum(positive_flow[i-self.mfi_length:i])
            negative_mf_sum[i] = np.sum(negative_flow[i-self.mfi_length:i])
        
        # Calculate MFI
        money_flow_ratio = np.divide(
            positive_mf_sum, 
            negative_mf_sum, 
            out=np.zeros_like(positive_mf_sum), 
            where=negative_mf_sum!=0
        )
        
        mfi = 100 - (100 / (1 + money_flow_ratio))
        return mfi

    def k_means_clustering(self, mfi: np.ndarray) -> Dict[str, float]:
        """Implement K-means clustering for MFI"""
        a, b, c = self.overbought, self.neutral, self.oversold
        
        for _ in range(self.iterations):
            ob_points = []
            ne_points = []
            os_points = []
            
            for i in range(min(self.length, len(mfi))):
                distances = [
                    abs(mfi[i] - b),
                    abs(mfi[i] - a),
                    abs(mfi[i] - c)
                ]
                
                min_index = distances.index(min(distances))
                
                if min_index == 0:
                    ne_points.append(mfi[i])
                elif min_index == 1:
                    ob_points.append(mfi[i])
                else:
                    os_points.append(mfi[i])
            
            # Update cluster centers
            a = np.mean(ob_points) if ob_points else a
            b = np.mean(ne_points) if ne_points else b
            c = np.mean(os_points) if os_points else c
        
        return {
            'overbought': a,
            'neutral': b,
            'oversold': c
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

    def calculate_rsi(self, close: np.ndarray, length: int) -> np.ndarray:
        """Calculate Relative Strength Index"""
        delta = np.diff(close)
        gain = (delta > 0) * delta
        loss = (delta < 0) * -delta
        
        avg_gain = pd.Series(gain).rolling(window=length, min_periods=1).mean().values
        avg_loss = pd.Series(loss).rolling(window=length, min_periods=1).mean().values
        
        rs = avg_gain / (avg_loss + 1e-10)
        rsi = 100 - (100 / (1 + rs))
        
        return np.concatenate(([50], rsi))

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

    def calculate_atr(self, high: np.ndarray, low: np.ndarray, close: np.ndarray, length: int) -> np.ndarray:
        """Calculate Average True Range"""
        tr1 = high - low
        tr2 = np.abs(high - np.roll(close, 1))
        tr3 = np.abs(low - np.roll(close, 1))
        
        tr = np.maximum(np.maximum(tr1, tr2), tr3)
        return pd.Series(tr).rolling(window=length).mean().values

    def calculate_trend_strength(self, close: np.ndarray, length: int = 14) -> np.ndarray:
        """Calculate trend strength using linear regression"""
        trend_strength = np.zeros_like(close)
        
        for i in range(length, len(close)):
            window = close[i-length:i]
            x = np.arange(len(window))
            slope, _, r_value, _, _ = stats.linregress(x, window)
            trend_strength[i] = abs(r_value) * np.sign(slope)
        
        return trend_strength

    def calculate_strategy(self, data: Dict[str, List[float]]) -> Dict[str, Any]:
        """Main calculation function with comprehensive analysis"""
        if not data or len(data['close']) == 0:
            return {}
        
        # Convert data to numpy arrays
        opens = np.array(data['open'])
        highs = np.array(data['high'])
        lows = np.array(data['low'])
        closes = np.array(data['close'])
        volumes = np.array(data['volume'])
        timestamps = np.array(data['time'])
        
        # Calculate MFI
        mfi = self.calculate_mfi(data)
        
        # Perform K-means clustering
        clusters = self.k_means_clustering(mfi)
        
        # Calculate position between bands
        position_between_bands = 100 * ((mfi - clusters['oversold']) / 
                                        (clusters['overbought'] - clusters['oversold']))
        
        # Determine value based on adjustment
        val = position_between_bands if self.adj else mfi
        
        # Calculate standard deviation
        st = np.std(val)
        
        # Determine color and trend
        trend = 'up' if mfi > clusters['neutral'] else 'down'
        
        # Additional Indicators
        rsi = self.calculate_rsi(closes, self.rsi_length)
        stoch = self.calculate_stochastic(closes, highs, lows, self.stoch_length)
        macd = self.calculate_macd(closes, self.macd_fast, self.macd_slow, self.macd_signal)
        atr = self.calculate_atr(highs, lows, closes, self.atr_length)
        trend_strength = self.calculate_trend_strength(closes)
        
        # Volatility Analysis
        volatility = atr / np.mean(closes)
        is_volatile = volatility > self.volatility_threshold
        
        # Trend Reversal Detection
        trend_reversal_signal = (
            (rsi > 70 and trend == 'up') or 
            (rsi < 30 and trend == 'down')
        )
        
        return {
            'open': opens.tolist(),
            'high': highs.tolist(),
            'low': lows.tolist(),
            'close': closes.tolist(),
            'volume': volumes.tolist(),
            'mfi': mfi.tolist(),
            'clusters': clusters,
            'position_between_bands': position_between_bands.tolist(),
            'val': val.tolist(),
            'standard_deviation': st,
            'trend': trend,
            'timestamps': timestamps.tolist(),
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
            'atr': atr.tolist(),
            'volatility': volatility.tolist(),
            'is_volatile': is_volatile.tolist(),
            'trend_strength': trend_strength.tolist(),
            'trend_reversal_signal': trend_reversal_signal,
            'visualization': {
                'colors': {
                    'up': self.green,
                    'down': self.red,
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
    
    strategy = SupportResistanceBlackflagP3Strategy()
    data = await strategy.fetch_candle_data(symbol, timeframe)
    result = strategy.calculate_strategy(data)
    print(json.dumps(result))

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())