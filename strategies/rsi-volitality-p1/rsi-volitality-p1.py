import numpy as np
import pandas as pd
import requests
from typing import Dict, List, Any

class RSIVolatilityStrategy:

	def __init__(self):
		# Strategy Parameters
		self.rsi_length = 14
		self.vol_length = 20
		self.rsi_overbought = 70
		self.rsi_oversold = 30
		self.vol_threshold = 1.5
		
		# Visualization Parameters
		self.colors = {
			'rsi_line': '#2196F3',  # Blue
			'overbought_line': '#FF5252',  # Red
			'oversold_line': '#4CAF50',  # Green
			'vol_high': '#FF9800',  # Orange
			'vol_normal': '#9E9E9E',  # Gray
			'signal_long': '#4CAF50',  # Green
			'signal_short': '#FF5252'  # Red
		}
		self.line_widths = {
			'rsi_line': 2,
			'level_lines': 1,
			'vol_line': 2
		}

	def calculate_rsi(self, closes: np.ndarray) -> np.ndarray:
		"""Calculate RSI indicator"""
		delta = np.diff(closes)
		gain = np.where(delta > 0, delta, 0)
		loss = np.where(delta < 0, -delta, 0)
		
		# Prepend zero to match array length
		gain = np.insert(gain, 0, 0)
		loss = np.insert(loss, 0, 0)
		
		# Calculate average gain and loss
		avg_gain = pd.Series(gain).rolling(window=self.rsi_length).mean().values
		avg_loss = pd.Series(loss).rolling(window=self.rsi_length).mean().values
		
		# Calculate RS and RSI
		rs = np.divide(avg_gain, avg_loss, out=np.zeros_like(avg_gain), where=avg_loss != 0)
		rsi = 100 - (100 / (1 + rs))
		
		return rsi

	def calculate_volatility(self, closes: np.ndarray) -> np.ndarray:
		"""Calculate price volatility"""
		returns = np.diff(np.log(closes))
		returns = np.insert(returns, 0, 0)
		volatility = pd.Series(returns).rolling(window=self.vol_length).std().values
		return volatility

	async def fetch_candle_data(self, symbol: str, timeframe: str) -> Dict[str, List[float]]:
		"""Fetch candle data from the API"""
		try:
			response = requests.get(
				f'http://localhost:5000/fetch_candles',
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

	def generate_signals(self, rsi: np.ndarray, volatility: np.ndarray, 
						vol_sma: np.ndarray) -> tuple[List[bool], List[bool]]:
		"""Generate trading signals based on RSI and volatility"""
		long_signals = []
		short_signals = []
		
		for i in range(len(rsi)):
			# High volatility condition
			high_vol = volatility[i] > (vol_sma[i] * self.vol_threshold)
			
			# Generate signals only in high volatility conditions
			if high_vol:
				long_signals.append(rsi[i] < self.rsi_oversold)
				short_signals.append(rsi[i] > self.rsi_overbought)
			else:
				long_signals.append(False)
				short_signals.append(False)
		
		return long_signals, short_signals

	def calculate_strategy(self, data: Dict[str, List[float]]) -> Dict[str, Any]:
		"""Main calculation function"""
		closes = np.array(data['close'])
		
		# Calculate indicators
		rsi = self.calculate_rsi(closes)
		volatility = self.calculate_volatility(closes)
		vol_sma = pd.Series(volatility).rolling(window=self.vol_length).mean().values
		
		# Generate signals
		long_signals, short_signals = self.generate_signals(rsi, volatility, vol_sma)
		
		return {
			'rsi': rsi.tolist(),
			'volatility': volatility.tolist(),
			'vol_sma': vol_sma.tolist(),
			'long_signals': long_signals,
			'short_signals': short_signals,
			'timestamps': data['time'],
			'visualization': {
				'colors': self.colors,
				'line_widths': self.line_widths
			}
		}

def calculate_indicators(symbol: str, timeframe: str) -> Dict[str, Any]:
	"""Main calculation function exposed to API"""
	strategy = RSIVolatilityStrategy()
	
	# Fetch candle data
	data = strategy.fetch_candle_data(symbol, timeframe)
	if not data['close']:
		return {
			'rsi': [],
			'volatility': [],
			'vol_sma': [],
			'long_signals': [],
			'short_signals': [],
			'timestamps': [],
			'visualization': {
				'colors': strategy.colors,
				'line_widths': strategy.line_widths
			}
		}
	
	# Calculate strategy indicators and signals
	result = strategy.calculate_strategy(data)
	return result

if __name__ == "__main__":
	print("RSI Volatility Strategy Module")
