import eel
import numpy as np
import pandas as pd
import requests
from typing import List, Dict, Union, Tuple

eel.init('web')

class NNTRSI:
	def __init__(self):
		# Default parameters from PineScript
		self.rsi_length = 14
		self.nn_length = 5
		self.sd_look = 365
		self.sd_mult = 2.0
		self.ema_lengths = [10, 21, 50]  # 3EMA periods
		self.wickratio_cutoff = 10
		self.wicktobody_cutoff = 10
		
	def calculate_ema(self, data: List[float], length: int) -> List[float]:
		"""Calculate EMA indicator"""
		return pd.Series(data).ewm(span=length, adjust=False).mean().tolist()
	
	def calculate_rsi(self, data: List[float], length: int = 14) -> List[float]:
		"""Calculate RSI indicator"""
		delta = np.diff(data)
		gain = np.where(delta > 0, delta, 0)
		loss = np.where(delta < 0, -delta, 0)
		
		avg_gain = pd.Series(gain).ewm(com=length-1, adjust=False).mean()
		avg_loss = pd.Series(loss).ewm(com=length-1, adjust=False).mean()
		
		rs = avg_gain / avg_loss
		rsi = 100 - (100 / (1 + rs))
		
		return [np.nan] + rsi.tolist()

	def calculate_nn_output(self, rsi_values: List[float]) -> List[float]:
		"""Calculate Neural Network smoothed output"""
		nn_output = []
		for i in range(len(rsi_values)):
			if i < self.nn_length - 1:
				nn_output.append(np.nan)
				continue
			window = rsi_values[i-self.nn_length+1:i+1]
			weights = np.ones(self.nn_length) / self.nn_length
			value = np.sum(np.array(window) * weights)
			nn_output.append(value)
		return nn_output

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

	def calculate_heikin_ashi(self, open_prices: List[float], high_prices: List[float],
							low_prices: List[float], close_prices: List[float]) -> Dict[str, List[float]]:
		"""Calculate Heikin-Ashi candles with renamed variables"""
		ha_close = [(o + h + l + c) / 4 for o, h, l, c in zip(open_prices, high_prices, low_prices, close_prices)]
		hopen = [open_prices[0]]  # First open is the same as regular open
		
		for i in range(1, len(open_prices)):
			hopen.append((hopen[i-1] + ha_close[i-1]) / 2)
		
		hhigh = [max(h, o, c) for h, o, c in zip(high_prices, hopen, ha_close)]
		hlow = [min(l, o, c) for l, o, c in zip(low_prices, hopen, ha_close)]
		
		return {
			'hopen': hopen,
			'hhigh': hhigh,
			'hlow': hlow,
			'hclose': ha_close
		}

	def identify_swing_points(self, prices: List[float], lookback: int = 5) -> Tuple[List[bool], List[bool]]:
		"""Identify swing high and low points"""
		swing_highs = []
		swing_lows = []

		for i in range(len(prices)):
			# Check for swing high
			is_swing_high = all(prices[i] > prices[j] 
								for j in range(max(0, i-lookback), i)) and \
							 all(prices[i] > prices[j] 
								for j in range(i+1, min(len(prices), i+lookback+1)))
			swing_highs.append(is_swing_high)

			# Check for swing low
			is_swing_low = all(prices[i] < prices[j] 
								for j in range(max(0, i-lookback), i)) and \
							all(prices[i] < prices[j] 
								for j in range(i+1, min(len(prices), i+lookback+1)))
			swing_lows.append(is_swing_low)
			
		return swing_highs, swing_lows

	def detect_engulfing_patterns(self, open_prices: List[float], close_prices: List[float]) -> List[str]:
		"""Detect bullish and bearish engulfing patterns"""
		engulfing_patterns = []
		for i in range(1, len(open_prices)):
			# Bullish Engulfing
			if (close_prices[i-1] < open_prices[i-1] and  # Previous candle is bearish
				close_prices[i] > open_prices[i] and     # Current candle is bullish
				open_prices[i] < close_prices[i-1] and   # Open is lower than previous close
				close_prices[i] > open_prices[i-1]):     # Close is higher than previous open
				engulfing_patterns.append('Bullish Engulfing')
			
			# Bearish Engulfing
			elif (close_prices[i-1] > open_prices[i-1] and  # Previous candle is bullish
				  close_prices[i] < open_prices[i] and      # Current candle is bearish
				  open_prices[i] > close_prices[i-1] and    # Open is higher than previous close
				  close_prices[i] < open_prices[i-1]):      # Close is lower than previous open
				engulfing_patterns.append('Bearish Engulfing')
			else:
				engulfing_patterns.append('No Pattern')
		
		return engulfing_patterns

	def detect_morning_evening_star(self, open_prices: List[float], high_prices: List[float], 
									low_prices: List[float], close_prices: List[float]) -> List[str]:
		"""Detect Morning and Evening Star patterns"""
		star_patterns = []
		for i in range(2, len(open_prices)):
			# Morning Star (Bullish Reversal)
			if (close_prices[i-2] < open_prices[i-2] and  # First candle bearish
				abs(close_prices[i-1] - open_prices[i-1]) <= 0.1 * close_prices[i-2] and  # Doji or small body
				close_prices[i] > open_prices[i] and  # Third candle bullish
				close_prices[i] > (close_prices[i-2] + close_prices[i-1]) / 2):  # Closes above midpoint
				star_patterns.append('Morning Star')
			
			# Evening Star (Bearish Reversal)
			elif (close_prices[i-2] > open_prices[i-2] and  # First candle bullish
				  abs(close_prices[i-1] - open_prices[i-1]) <= 0.1 * close_prices[i-2] and  # Doji or small body
				  close_prices[i] < open_prices[i] and  # Third candle bearish
				  close_prices[i] < (close_prices[i-2] + close_prices[i-1]) / 2):  # Closes below midpoint
				star_patterns.append('Evening Star')
			else:
				star_patterns.append('No Pattern')
		
		return star_patterns

	def detect_dark_cloud_cover(self, open_prices: List[float], close_prices: List[float]) -> List[str]:
		"""Detect Dark Cloud Cover pattern"""
		dark_cloud_patterns = []
		for i in range(1, len(open_prices)):
			# Dark Cloud Cover (Bearish Reversal)
			if (close_prices[i-1] > open_prices[i-1] and  # Previous candle bullish
				close_prices[i] < open_prices[i] and     # Current candle bearish
				close_prices[i] < open_prices[i-1] and   # Close below previous open
				close_prices[i] <= (open_prices[i-1] + close_prices[i-1]) / 2):  # Close in upper half of previous candle
				dark_cloud_patterns.append('Dark Cloud Cover')
			else:
				dark_cloud_patterns.append('No Pattern')
		
		return dark_cloud_patterns

@eel.expose
async def calculate_indicators(symbol: str, timeframe: str) -> Dict[str, Union[List[float], Dict[str, List[float]]]]:
	"""Main calculation function exposed to JavaScript with data fetching"""
	nnt_rsi = NNTRSI()
	
	# Fetch candle data
	data = await nnt_rsi.fetch_candle_data(symbol, timeframe)
	if not data['close']:
		return {
			'nn_output': [],
			'ha_candles': {'hopen': [], 'hhigh': [], 'hlow': [], 'hclose': []},
			'upper_band': [],
			'lower_band': [],
			'mean_line': [],
			'swing_highs': [],
			'swing_lows': [],
			'engulfing_patterns': [],
			'star_patterns': [],
			'dark_cloud_patterns': []
		}
	
	# Calculate RSI and NN output
	rsi_values = nnt_rsi.calculate_rsi(data['close'])
	nn_output = nnt_rsi.calculate_nn_output(rsi_values)
	
	# Calculate Heikin-Ashi values
	ha_candles = nnt_rsi.calculate_heikin_ashi(
		data['open'], data['high'], data['low'], data['close']
	)
	
	# Calculate SD bands
	rolling_mean = pd.Series(nn_output).rolling(window=nnt_rsi.sd_look).mean()
	rolling_std = pd.Series(nn_output).rolling(window=nnt_rsi.sd_look).std()
	upper_band = rolling_mean + (rolling_std * nnt_rsi.sd_mult)
	lower_band = rolling_mean - (rolling_std * nnt_rsi.sd_mult)
	
	# Identify swing points
	swing_highs, swing_lows = nnt_rsi.identify_swing_points(data['close'])
	
	# Detect chart patterns
	engulfing_patterns = nnt_rsi.detect_engulfing_patterns(data['open'], data['close'])
	star_patterns = nnt_rsi.detect_morning_evening_star(data['open'], data['high'], data['low'], data['close'])
	dark_cloud_patterns = nnt_rsi.detect_dark_cloud_cover(data['open'], data['close'])
	
	return {
		'nn_output': nn_output,
		'ha_candles': ha_candles,
		'upper_band': upper_band.tolist(),
		'lower_band': lower_band.tolist(),
		'mean_line': rolling_mean.tolist(),
		'timestamps': data['time'],
		'swing_highs': swing_highs,
		'swing_lows': swing_lows,
		'engulfing_patterns': engulfing_patterns,
		'star_patterns': star_patterns,
		'dark_cloud_patterns': dark_cloud_patterns
	}

if __name__ == "__main__":
	eel.start('index.html')
