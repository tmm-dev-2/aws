import numpy as np
import pandas as pd
import requests
import asyncio
from typing import Dict, List, Any, NamedTuple
from dataclasses import dataclass
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@dataclass
class Bar:
    high: float
    low: float
    volume: float
    index: int
    
class DoubleHullTurboStrategy:
    def __init__(self):
        # HMA Parameters
        self.length_1 = 20
        self.length_2 = 198
        
        # Index and Volume Flow Parameters
        self.index_period = 25
        self.volume_flow_period = 14
        self.normalization_period = 500
        self.high_interest_threshold = 0.85
        
        # Additional Parameters
        self.max_memory = 90
        
        # Visualization Parameters
        self.base_transparency = 99
        self.green_color = '#00FFB'
        
        # Box Parameters
        self.box_memory = []
        self.max_box_memory = 90

    def calculate_wma(self, data: np.ndarray, length: int) -> np.ndarray:
        """
        Calculate Weighted Moving Average with detailed weighting
        Args:
            data: Input price data
            length: Period for WMA calculation
        Returns:
            Weighted Moving Average array
        """
        weights = np.arange(1, length + 1)
        wma = np.zeros_like(data)
        
        for i in range(length - 1, len(data)):
            window = data[i - length + 1:i + 1]
            wma[i] = np.sum(weights * window) / np.sum(weights)
        
        return wma

    def calculate_hma(self, data: np.ndarray, length: int) -> np.ndarray:
        """
        Calculate Hull Moving Average (HMA) with enhanced smoothing
        Args:
            data: Input price data
            length: Period for HMA calculation
        Returns:
            Hull Moving Average array
        """
        half_length = length // 2
        sqrt_length = int(np.sqrt(length))
        
        wma_half = self.calculate_wma(data, half_length)
        wma_full = self.calculate_wma(data, length)
        
        wmaf = 2 * wma_half - wma_full
        hma = self.calculate_wma(wmaf, sqrt_length)
        
        return hma

    def calculate_first_derivative(self, data: np.ndarray, length: int) -> np.ndarray:
        """
        Calculate first derivative for trend detection
        Args:
            data: Input data array
            length: Period for derivative calculation
        Returns:
            First derivative array
        """
        derivative = np.zeros_like(data)
        sma = pd.Series(data).rolling(window=length).mean().values
        
        for i in range(1, len(data)):
            derivative[i] = sma[i] - sma[i-1]
        
        return derivative

    def check_derivative_conditions(self, data: np.ndarray, length: int) -> np.ndarray:
        """
        Check derivative conditions for trend confirmation
        Args:
            data: Input data array
            length: Period for derivative calculation
        Returns:
            Array with trend conditions (1: uptrend, -1: downtrend, 0: no trend)
        """
        derivative = self.calculate_first_derivative(data, length)
        return np.where(derivative > 0, 1, np.where(derivative < 0, -1, 0))

    def calculate_box_data(self, highs: np.ndarray, lows: np.ndarray, 
                          valley_formation: np.ndarray) -> List[Dict[str, Any]]:
        """
        Calculate box visualization data with support/resistance levels
        Args:
            highs: High prices array
            lows: Low prices array
            valley_formation: Valley formation indicator array
        Returns:
            List of box visualization parameters
        """
        box_data = []
        
        for i in range(len(highs)):
            if valley_formation[i]:
                # Calculate local support and resistance
                local_high = np.max(highs[max(0, i-10):i+1])
                local_low = np.min(lows[max(0, i-10):i+1])
                
                box = {
                    'time_index': i,
                    'high': local_high,
                    'low': local_low,
                    'color': self.green_color,
                    'transparency': self.base_transparency
                }
                
                # Manage box memory
                self.box_memory.append(box)
                if len(self.box_memory) > self.max_box_memory:
                    self.box_memory.pop(0)
                
                box_data.append(box)
        
        return box_data

    def calculate_pvi_nvi(self, close: np.ndarray, volume: np.ndarray) -> tuple:
        """Calculate Positive and Negative Volume Index"""
        pvi = np.zeros_like(close)
        nvi = np.zeros_like(close)
        pvi[0] = 1000
        nvi[0] = 1000
        
        for i in range(1, len(close)):
            if volume[i] > volume[i-1]:
                pvi[i] = pvi[i-1] * (1 + (close[i] - close[i-1]) / close[i-1])
                nvi[i] = nvi[i-1]
            else:
                nvi[i] = nvi[i-1] * (1 + (close[i] - close[i-1]) / close[i-1])
                pvi[i] = pvi[i-1]
        
        return pvi, nvi

    def calculate_rsi(self, data: np.ndarray, period: int) -> np.ndarray:
        """Calculate RSI"""
        delta = np.diff(data)
        delta = np.insert(delta, 0, 0)
        gain = np.where(delta > 0, delta, 0)
        loss = np.where(delta < 0, -delta, 0)
        
        avg_gain = pd.Series(gain).rolling(window=period).mean().values
        avg_loss = pd.Series(loss).rolling(window=period).mean().values
        
        rs = np.where(avg_loss != 0, avg_gain / avg_loss, 0)
        rsi = 100 - (100 / (1 + rs))
        return rsi

    def detect_valley_formation(self, hma1: np.ndarray, hma2: np.ndarray) -> np.ndarray:
        """Detect valley formation when HMA1 > HMA2"""
        return hma1 > hma2

    async def fetch_candle_data(self, symbol: str, timeframe: str) -> Dict[str, List[float]]:
        """Fetch candle data from the API"""
        try:
            response = requests.get(
                'http://localhost:5000/historical',
                params={'symbol': symbol}
            )
            response.raise_for_status()
            data = response.json()
            
            candles = data.get('candles', [])

            return {
                'open': [candle['open'] for candle in candles],
                'high': [candle['high'] for candle in candles],
                'low': [candle['low'] for candle in candles],
                'close': [candle['close'] for candle in candles],
                'volume': [candle['volume'] for candle in candles],
                'time': [candle['time'] for candle in candles]
            }
        except Exception as e:
            print(f"Error fetching candle data: {e}")
            return {'open': [], 'high': [], 'low': [], 'close': [], 'volume': [], 'time': []}

    def calculate_strategy(self, data: Dict[str, List[float]]) -> Dict[str, Any]:
        """Main calculation function with enhanced metrics"""
        closes = np.array(data['close'])
        opens = np.array(data['open'])
        highs = np.array(data['high'])
        lows = np.array(data['low'])
        volumes = np.array(data['volume'])
        
        # Calculate HMAs with derivatives
        hma1 = self.calculate_hma(closes, self.length_1)
        hma2 = self.calculate_hma(closes, self.length_2)
        hma1_conditions = self.check_derivative_conditions(hma1, 1)
        hma2_conditions = self.check_derivative_conditions(hma2, 1)
        
        # Calculate PVI and NVI with enhanced volume analysis
        pvi, nvi = self.calculate_pvi_nvi(closes, volumes)
        pvi_ema = pd.Series(pvi).ewm(span=255).mean().values
        nvi_ema = pd.Series(nvi).ewm(span=255).mean().values
        
        # Calculate money flow indicators
        dumb = pvi - pvi_ema
        smart = nvi - nvi_ema
        drsi = self.calculate_rsi(dumb, self.volume_flow_period)
        srsi = self.calculate_rsi(smart, self.volume_flow_period)
        
        # Calculate enhanced ratio and index
        ratio = np.where(drsi != 0, srsi / drsi, 0)
        sums = pd.Series(ratio).rolling(window=self.index_period).sum().values
        peak = pd.Series(sums).rolling(window=self.normalization_period).max().values
        index = np.where(peak != 0, sums / peak, 0)
        
        # Calculate candle patterns and valley formation
        candle_direction = np.where(closes > opens, 1, -1)
        candle_length = np.abs(closes - opens)
        valley_formation = self.detect_valley_formation(hma1, hma2)
        
        # Calculate box visualization data
        box_data = self.calculate_box_data(highs, lows, valley_formation)
        
        # Detect crossovers with confirmation
        crossover = np.zeros_like(closes)
        crossunder = np.zeros_like(closes)
        
        for i in range(1, len(closes)):
            if hma1[i] > hma2[i] and hma1[i-1] <= hma2[i-1] and hma1_conditions[i] > 0:
                crossover[i] = 1
            if hma1[i] < hma2[i] and hma1[i-1] >= hma2[i-1] and hma1_conditions[i] < 0:
                crossunder[i] = 1
        
        return {
            'hma1': hma1.tolist(),
            'hma2': hma2.tolist(),
            'crossover': crossover.tolist(),
            'crossunder': crossunder.tolist(),
            'index': index.tolist(),
            'valley_formation': valley_formation.tolist(),
            'candle_direction': candle_direction.tolist(),
            'candle_length': candle_length.tolist(),
            'box_data': box_data,
            'timestamps': data['time'],
            'visualization': {
                'colors': {
                    'hma1_up': '#00FF00',
                    'hma1_down': '#FF0000',
                    'hma2_up': '#00FF00',
                    'hma2_down': '#FF0000'
                },
                'transparency': self.base_transparency,
                'box_color': self.green_color
            }
        }

@app.route('/double-hull-turbo-p1', methods=['GET'])
def calculate_double_hull():
    symbol = request.args.get('symbol')
    timeframe = request.args.get('timeframe')
    
    if not symbol or not timeframe:
        return jsonify({"error": "Missing required parameters: symbol and timeframe"}), 400
    
    try:
        strategy = DoubleHullTurboStrategy()
        data = asyncio.run(strategy.fetch_candle_data(symbol, timeframe))
        result = strategy.calculate_strategy(data)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)