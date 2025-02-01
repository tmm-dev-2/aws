import numpy as np
import pandas as pd
from scipy.stats import norm
from typing import Dict, List, Any, Tuple
import requests

class KernelRegressionStrategy:
	def __init__(self):
		# Strategy Parameters from PineScript with detailed explanations
		self.bandwidth = 45      # Controls the smoothing window for kernel regression
		self.width = 2.0        # Scaling factor for the wave signal
		self.sd_lookback = 150  # Lookback period for standard deviation calculations
		self.sd_mult = 3.0      # Multiplier for standard deviation bands
		
		# Additional parameters for signal generation
		self.min_wave_change = 0.001  # Minimum change required for trend signal
		self.signal_smoothing = 3     # Smoothing period for signal generation
		
	def gaussian_kernel(self, x: np.ndarray) -> np.ndarray:
		"""
		Gaussian kernel function for smooth transitions
		Args:
			x: Input array of distances
		Returns:
			Array of kernel weights
		"""
		return np.exp(-0.5 * x**2) / np.sqrt(2 * np.pi)
		
	def epanechnikov_kernel(self, x: np.ndarray) -> np.ndarray:
		"""
		Epanechnikov kernel function for efficient estimation
		Args:
			x: Input array of distances
		Returns:
			Array of kernel weights
		"""
		return np.where(np.abs(x) <= 1, 3/4 * (1 - x**2), 0)
	
	def logistic_kernel(self, x: np.ndarray) -> np.ndarray:
		"""
		Logistic kernel function for robust estimation
		Args:
			x: Input array of distances
		Returns:
			Array of kernel weights
		"""
		return 1 / (np.exp(x) + 2 + np.exp(-x))
	
	def wave_kernel(self, x: np.ndarray) -> np.ndarray:
		"""
		Wave kernel function for oscillatory patterns
		Args:
			x: Input array of distances
		Returns:
			Array of kernel weights
		"""
		return np.where(np.abs(x) <= 1, (1 - x**2) * np.sin(1 / (1 - x**2)), 0)
	
	def kernel_regression(self, data: np.ndarray, kernel_type: str) -> np.ndarray:
		"""
		Calculate kernel regression using specified kernel
		Args:
			data: Input price data
			kernel_type: Type of kernel function to use
		Returns:
			Array of regression values
		"""
		n = len(data)
		y_pred = np.zeros(n)
		
		for i in range(n):
			weights = np.zeros(n)
			for j in range(n):
				x = (i - j) / self.bandwidth
				
				if kernel_type == 'Epanechnikov':
					weights[j] = self.epanechnikov_kernel(x)
				elif kernel_type == 'Logistic':
					weights[j] = self.logistic_kernel(x)
				elif kernel_type == 'Gaussian':
					weights[j] = self.gaussian_kernel(x)
				else:  # Wave
					weights[j] = self.wave_kernel(x)
			
			weights = weights / np.sum(weights)
			y_pred[i] = np.sum(weights * data)
		
		return y_pred
	
	def calculate_wave(self, data: np.ndarray) -> np.ndarray:
		"""
		Calculate wave signal using kernel regression
		Args:
			data: Input price data
		Returns:
			Wave signal array
		"""
		scaled_data = data * self.width
		return self.kernel_regression(scaled_data, 'Wave')
	
	def calculate_std_bands(self, data: np.ndarray, lookback: int, multiplier: float) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
		"""
		Calculate standard deviation bands
		Args:
			data: Input price data
			lookback: Period for rolling calculations
			multiplier: Standard deviation multiplier
		Returns:
			Tuple of (mid_line, upper_band, lower_band)
		"""
		rolling_mean = pd.Series(data).rolling(window=lookback).mean()
		rolling_std = pd.Series(data).rolling(window=lookback).std()
		
		upper_band = rolling_mean + (rolling_std * multiplier)
		lower_band = rolling_mean - (rolling_std * multiplier)
		
		return rolling_mean.values, upper_band.values, lower_band.values
	
	def calculate_momentum(self, wave: np.ndarray) -> np.ndarray:
		"""
		Calculate momentum of the wave signal
		Args:
			wave: Wave signal array
		Returns:
			Momentum indicator array
		"""
		return np.gradient(wave)
	
	def calculate_volatility(self, data: np.ndarray) -> np.ndarray:
		"""
		Calculate rolling volatility
		Args:
			data: Input price data
		Returns:
			Volatility measure array
		"""
		return pd.Series(data).rolling(window=self.sd_lookback).std().values
	
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
		"""
		Main calculation function
		Args:
			data: Dictionary containing OHLCV data
		Returns:
			Dictionary containing all calculated indicators and signals
		"""
		closes = np.array(data['close'])
		highs = np.array(data['high'])
		lows = np.array(data['low'])
		
		# Calculate main wave signal
		wave = self.calculate_wave(closes)
		
		# Calculate confirmations using different kernels
		ep_signal = self.kernel_regression(closes, 'Epanechnikov')
		log_signal = self.kernel_regression(closes, 'Logistic')
		wave_signal = self.kernel_regression(closes, 'Wave')
		gauss_signal = self.kernel_regression(closes, 'Gaussian')
		
		# Calculate combined signal
		avg_signal = (ep_signal + log_signal + wave_signal + gauss_signal) / 4 + closes
		
		# Calculate momentum and volatility
		momentum = self.calculate_momentum(wave)
		volatility = self.calculate_volatility(closes)
		
		# Calculate SD bands
		mid, upper1, lower1 = self.calculate_std_bands(avg_signal, self.sd_lookback, self.sd_mult/2)
		_, upper2, lower2 = self.calculate_std_bands(avg_signal, self.sd_lookback, self.sd_mult)
		
		# Calculate trend signals with momentum confirmation
		trend_up = np.zeros(len(wave), dtype=bool)
		trend_down = np.zeros(len(wave), dtype=bool)
		
		for i in range(2, len(wave)):
			trend_up[i] = (wave[i] > wave[i-1] and 
						  not (wave[i-1] > wave[i-2]) and 
						  momentum[i] > self.min_wave_change)
			trend_down[i] = (wave[i] < wave[i-1] and 
						   not (wave[i-1] < wave[i-2]) and 
						   momentum[i] < -self.min_wave_change)
		
		return {
			'wave': wave.tolist(),
			'upper_band1': upper1.tolist(),
			'lower_band1': lower1.tolist(),
			'upper_band2': upper2.tolist(),
			'lower_band2': lower2.tolist(),
			'mid_line': mid.tolist(),
			'momentum': momentum.tolist(),
			'volatility': volatility.tolist(),
			'trend_up': trend_up.tolist(),
			'trend_down': trend_down.tolist(),
			'timestamps': data['time']
		}