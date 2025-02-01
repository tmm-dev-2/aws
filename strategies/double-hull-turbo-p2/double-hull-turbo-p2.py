import numpy as np
import pandas as pd
import requests
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass

@dataclass
class Point:
    price: float
    ndx: int

@dataclass
class Pivot:
    price: float
    ndx: int
    indicator: float

@dataclass
class DiverLine:
    start_price: float
    end_price: float
    start_ndx: int
    end_ndx: int
    start_indicator: float
    end_indicator: float
    is_bull: bool
    is_hidden: bool

class DoubleHullTurboStrategy:
    def __init__(self):
        # Strategy Parameters
        self.rsi_length = 14
        self.smooth_length = 2
        self.mfi_length = 30
        self.fast_mfi_len = round(self.mfi_length / 1.33)
        self.slow_mfi_len = round(self.mfi_length * 1.33)
        
        # Constants from PineScript
        self.mfi_len = 7
        self.stoch_k = 2
        self.stoch_d = 5
        self.smooth_len = 1.75
        self.stoch_weight = 0.4
        self.mfi_weight = 0.4
        self.overbought = 60.0
        self.extend_mult = 1
        
        # Divergence Parameters
        self.piv_len_left = 7
        self.piv_len_right = 1
        self.min_peak_dist = 7
        self.max_peak_dist = 80
        
        # Take Profit Parameters
        self.up_border = 50
        self.dn_border = -50
        
        # Arrays for storing pivots and divergences
        self.pivot_highs: List[Pivot] = []
        self.pivot_lows: List[Pivot] = []
        self.bull_divergences: List[DiverLine] = []
        self.bear_divergences: List[DiverLine] = []
        self.bull_hidden_divergences: List[DiverLine] = []
        self.bear_hidden_divergences: List[DiverLine] = []

    def transform(self, src: np.ndarray, mult: float = 1) -> np.ndarray:
        """Transform values to a normalized range as per PineScript implementation"""
        tmp = (src / 100 - 0.5) * 2
        return mult * 100 * ((tmp > 0) * 2 - 1) * np.power(np.abs(tmp), 0.75)

    def calculate_mfi(self, high: np.ndarray, low: np.ndarray, close: np.ndarray, volume: np.ndarray, length: int) -> np.ndarray:
        """Calculate Money Flow Index with detailed implementation"""
        typical_price = (high + low + close) / 3
        money_flow = typical_price * volume
        
        positive_flow = np.where(typical_price > np.roll(typical_price, 1), money_flow, 0)
        negative_flow = np.where(typical_price < np.roll(typical_price, 1), money_flow, 0)
        
        positive_mf = pd.Series(positive_flow).rolling(window=length).sum()
        negative_mf = pd.Series(negative_flow).rolling(window=length).sum()
        
        mfi = 100 - (100 / (1 + positive_mf / negative_mf))
        return mfi.fillna(50).values

    def calculate_rsi(self, close: np.ndarray, length: int) -> np.ndarray:
        """Calculate RSI with detailed implementation"""
        delta = np.diff(close)
        gains = np.where(delta > 0, delta, 0)
        losses = np.where(delta < 0, -delta, 0)
        
        avg_gains = pd.Series(gains).rolling(window=length).mean()
        avg_losses = pd.Series(losses).rolling(window=length).mean()
        
        rs = avg_gains / avg_losses
        rsi = 100 - (100 / (1 + rs))
        return np.concatenate([[50], rsi.fillna(50).values])

    def calculate_stoch(self, src: np.ndarray, length: int) -> np.ndarray:
        """Calculate Stochastic Oscillator"""
        rolling_high = pd.Series(src).rolling(window=length).max()
        rolling_low = pd.Series(src).rolling(window=length).min()
        
        stoch = 100 * (src - rolling_low) / (rolling_high - rolling_low)
        return stoch.fillna(50).values

    def find_pivots(self, data: np.ndarray, left: int, right: int) -> Tuple[List[int], List[int]]:
        """Find pivot highs and lows with detailed implementation"""
        pivot_highs = []
        pivot_lows = []
        
        for i in range(left, len(data) - right):
            # Check for pivot high
            if all(data[i] > data[i-j] for j in range(1, left+1)) and \
               all(data[i] > data[i+j] for j in range(1, right+1)):
                pivot_highs.append(i)
            
            # Check for pivot low
            if all(data[i] < data[i-j] for j in range(1, left+1)) and \
               all(data[i] < data[i+j] for j in range(1, right+1)):
                pivot_lows.append(i)
        
        return pivot_highs, pivot_lows

    def find_divergences(self, price: np.ndarray, indicator: np.ndarray, 
                        pivot_points: List[int], is_hidden: bool = False) -> List[DiverLine]:
        """Find regular and hidden divergences with detailed implementation"""
        divergences = []
        
        for i in range(len(pivot_points) - 1):
            curr_idx = pivot_points[i]
            prev_idx = pivot_points[i + 1]
            
            if curr_idx - prev_idx < self.min_peak_dist or curr_idx - prev_idx > self.max_peak_dist:
                continue
            
            # Regular divergence conditions
            if not is_hidden:
                if (price[curr_idx] > price[prev_idx] and indicator[curr_idx] < indicator[prev_idx]) or \
                   (price[curr_idx] < price[prev_idx] and indicator[curr_idx] > indicator[prev_idx]):
                    divergences.append(DiverLine(
                        price[prev_idx], price[curr_idx],
                        prev_idx, curr_idx,
                        indicator[prev_idx], indicator[curr_idx],
                        price[curr_idx] < price[prev_idx],
                        False
                    ))
            # Hidden divergence conditions
            else:
                if (price[curr_idx] < price[prev_idx] and indicator[curr_idx] < indicator[prev_idx]) or \
                   (price[curr_idx] > price[prev_idx] and indicator[curr_idx] > indicator[prev_idx]):
                    divergences.append(DiverLine(
                        price[prev_idx], price[curr_idx],
                        prev_idx, curr_idx,
                        indicator[prev_idx], indicator[curr_idx],
                        price[curr_idx] > price[prev_idx],
                        True
                    ))
        
        return divergences

    def calculate_take_profit_signals(self, avg: np.ndarray) -> List[Dict[str, Any]]:
        """Calculate take profit signals with detailed implementation"""
        signals = []
        last_signal_bar = 0
        
        for i in range(2, len(avg)):
            if i - last_signal_bar < 10:
                continue
                
            if avg[i] > self.up_border and avg[i] > avg[i-2]:
                signals.append({
                    'type': 'sell',
                    'index': i,
                    'value': avg[i]
                })
                last_signal_bar = i
                
            elif avg[i] < self.dn_border and avg[i] < avg[i-2]:
                signals.append({
                    'type': 'buy',
                    'index': i,
                    'value': avg[i]
                })
                last_signal_bar = i
        
        return signals

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
        """Main calculation function implementing the complete strategy"""
        closes = np.array(data['close'])
        highs = np.array(data['high'])
        lows = np.array(data['low'])
        volumes = np.array(data.get('volume', [0] * len(closes)))
        timestamps = np.array(data['time'])
        
        # Calculate base indicators
        hlc3 = (highs + lows + closes) / 3
        fast_mfi = self.calculate_mfi(highs, lows, closes, volumes, self.fast_mfi_len)
        slow_mfi = self.calculate_mfi(highs, lows, closes, volumes, self.slow_mfi_len)
        
        # Calculate histogram
        mfi_avg = (fast_mfi * 0.5 + slow_mfi * 0.5)
        histogram = self.transform(pd.Series(mfi_avg).rolling(window=self.smooth_length).mean().values, 0.7)
        
        # Calculate main signal
        mfi = self.calculate_mfi(highs, lows, closes, volumes, self.mfi_len)
        rsi = self.calculate_rsi(hlc3, self.rsi_length)
        stoch = pd.Series(self.calculate_stoch(rsi, self.rsi_length)).rolling(window=self.stoch_k).mean()
        sig_stoch = pd.Series(stoch).rolling(window=self.stoch_d).mean()
        
        if np.all(volumes == 0):
            mfi = np.zeros_like(mfi)
            self.mfi_weight = 0
            
        signal = (rsi + self.mfi_weight * mfi + self.stoch_weight * stoch) / (1 + self.mfi_weight + self.stoch_weight)
        avg = self.transform(pd.Series(signal).ewm(span=self.smooth_length).mean().values, self.extend_mult)
        avg2 = self.transform(pd.Series(signal).ewm(span=round(self.smooth_length * self.smooth_len)).mean().values, self.extend_mult)
        
        # Find pivots and calculate divergences
        pivot_highs, pivot_lows = self.find_pivots(avg, self.piv_len_left, self.piv_len_right)
        
        # Calculate divergences
        regular_bull_divs = self.find_divergences(closes, avg, pivot_lows, False)
        regular_bear_divs = self.find_divergences(closes, avg, pivot_highs, False)
        hidden_bull_divs = self.find_divergences(closes, avg, pivot_lows, True)
        hidden_bear_divs = self.find_divergences(closes, avg, pivot_highs, True)
        
        # Calculate take profit signals
        tp_signals = self.calculate_take_profit_signals(avg)
        
        # Calculate status line score
        status_scores = np.zeros(len(avg))
        for i in range(len(avg)):
            score = 0
            if avg[i] > avg2[i]: score += 1
            if avg[i] > 0: score += 1
            if histogram[i] > 0: score += 1
            status_scores[i] = score
        
        return {
            'histogram': histogram.tolist(),
            'average': avg.tolist(),
            'average2': avg2.tolist(),
            'timestamps': timestamps.tolist(),
            'pivot_highs': pivot_highs,
            'pivot_lows': pivot_lows,
            'divergences': {
                'regular_bull': regular_bull_divs,
                'regular_bear': regular_bear_divs,
                'hidden_bull': hidden_bull_divs,
                'hidden_bear': hidden_bear_divs
            },
            'tp_signals': tp_signals,
            'status_scores': status_scores.tolist(),
            'visualization': {
                'colors': {
                    'up': '#6de6f693',
                    'down': '#f66d6d93',
                    'neutral': '#9E9E9E'
                }
            }
        }