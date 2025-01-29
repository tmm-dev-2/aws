import numpy as np
import pandas as pd
import requests
from typing import Dict, List, Any
from scipy import stats

class RSIVolatilityBandsStrategy:
	def __init__(self):
		# Strategy Parameters from PineScript
		self.norm_sens = 10
		self.vis_atr = 13
		self.sed_atr = 40
		self.vis_std = 20
		self.sed_std = 100
		self.adx_len = 14
		self.di_len = 14
		self.adx_base = 25
		self.period = 20
		self.tr_sens = 350

	def calculate_tr(self, high: np.ndarray, low: np.ndarray, close: np.ndarray) -> np.ndarray:
		"""Calculate True Range"""
		prev_close = np.roll(close, 1)
		prev_close[0] = close[0]
		
		tr1 = high - low
		tr2 = np.abs(high - prev_close)
		tr3 = np.abs(low - prev_close)
		
		tr = np.maximum(np.maximum(tr1, tr2), tr3)
		return tr

	def calculate_atr(self, high: np.ndarray, low: np.ndarray, close: np.ndarray, period: int) -> np.ndarray:
		"""Calculate Average True Range"""
		tr = self.calculate_tr(high, low, close)
		atr = pd.Series(tr).rolling(window=period).mean().values
		return atr

	def calculate_dynamic_stdev(self, data: np.ndarray, period: int) -> np.ndarray:
		"""Calculate Dynamic Standard Deviation"""
		return pd.Series(data).rolling(window=period).std().values

	def calculate_dynamic_median(self, data: np.ndarray, period: int) -> np.ndarray:
		"""Calculate Dynamic Median"""
		return pd.Series(data).rolling(window=period).median().values

	def calculate_dv(self, high: np.ndarray, low: np.ndarray, close: np.ndarray) -> np.ndarray:
		"""
		Calculate Modified Damiani Voltmeter (DV)
		This is a volatility indicator that combines ATR ratios and standard deviation ratios
		"""
		# Initialize arrays
		vol = np.zeros(len(close))
		lag_s_k = 0.5
		
		# Calculate ATR and StdDev components for the entire series
		vis_atr_values = self.calculate_atr(high, low, close, self.vis_atr)
		sed_atr_values = self.calculate_atr(high, low, close, self.sed_atr)
		vis_std_values = self.calculate_dynamic_stdev(close, self.vis_std)
		sed_std_values = self.calculate_dynamic_stdev(close, self.sed_std)
		
		# Calculate vol and threshold
		for i in range(len(close)):
			if i > 0:
				s1 = vol[i-1]
				s3 = vol[i-3] if i >= 3 else 0
				
				# ATR ratio calculation
				atr_ratio = vis_atr_values[i] / sed_atr_values[i] if sed_atr_values[i] != 0 else 0
				vol[i] = atr_ratio + lag_s_k * (s1 - s3)
			
			# Calculate anti-threshold using standard deviation ratio
			std_ratio = vis_std_values[i] / sed_std_values[i] if sed_std_values[i] != 0 else 0
			
			# Final threshold calculation
			threshold = 1.4 - std_ratio - vol[i]
			vol[i] = -threshold * 100
		
		return vol

	def calculate_adx(self, high: np.ndarray, low: np.ndarray, close: np.ndarray) -> np.ndarray:
		"""Calculate Average Directional Index (ADX)"""
		# Calculate +DM and -DM
		high_diff = np.diff(high)
		low_diff = np.diff(low)
		
		plus_dm = np.zeros(len(high))
		minus_dm = np.zeros(len(high))
		
		for i in range(1, len(high)):
			plus_dm[i] = high_diff[i-1] if high_diff[i-1] > 0 and high_diff[i-1] > -low_diff[i-1] else 0
			minus_dm[i] = -low_diff[i-1] if -low_diff[i-1] > 0 and -low_diff[i-1] > high_diff[i-1] else 0
		
		# Calculate TR
		tr = self.calculate_tr(high, low, close)
		
		# Calculate smoothed values
		smoothed_tr = pd.Series(tr).rolling(window=self.di_len).mean().values
		smoothed_plus_dm = pd.Series(plus_dm).rolling(window=self.di_len).mean().values
		smoothed_minus_dm = pd.Series(minus_dm).rolling(window=self.di_len).mean().values
		
		# Calculate DI+ and DI-
		plus_di = 100 * smoothed_plus_dm / smoothed_tr
		minus_di = 100 * smoothed_minus_dm / smoothed_tr
		
		# Calculate DX and ADX
		dx = 100 * np.abs(plus_di - minus_di) / (plus_di + minus_di)
		adx = pd.Series(dx).rolling(window=self.adx_len).mean().values
		
		return adx

	def calculate_dispersion(self, close: np.ndarray) -> np.ndarray:
		"""
		Calculate Linear Regression Dispersion
		This measures the deviation of prices from their linear regression line
		"""
		dispersion = np.zeros(len(close))
		
		for i in range(self.period - 1, len(close)):
			# Get window of data
			window = close[max(0, i-self.period+1):i+1]
			x = np.arange(len(window))
			
			# Calculate linear regression
			slope, intercept, _, _, _ = stats.linregress(x, window)
			reg_line = slope * x + intercept
			
			# Calculate deviations
			deviations = window - reg_line
			
			# Calculate dispersion metrics
			std_dev = np.std(deviations)
			median_dev = np.median(np.abs(deviations))
			
			# Final dispersion value
			dispersion[i] = (std_dev - median_dev) / 2
		
		return dispersion

	def normalize(self, data: np.ndarray, target_min: float, target_max: float, window: int) -> np.ndarray:
		"""
		Normalize data to a target range using a dynamic window
		"""
		normalized = np.zeros(len(data))
		
		for i in range(len(data)):
			window_start = max(0, i - window + 1)
			window_data = data[window_start:i+1]
			
			if len(window_data) > 0:
				data_min = np.min(window_data)
				data_max = np.max(window_data)
				
				if data_max != data_min:
					normalized[i] = target_min + (target_max - target_min) * \
								  (data[i] - data_min) / (data_max - data_min)
				else:
					normalized[i] = data[i]
		
		return normalized

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
		"""Main calculation function"""
		# Convert to numpy arrays for calculations
		closes = np.array(data['close'])
		highs = np.array(data['high'])
		lows = np.array(data['low'])
		
		# Calculate main indicators
		dvm = self.calculate_dv(highs, lows, closes)
		adx = self.calculate_adx(highs, lows, closes)