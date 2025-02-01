import numpy as np
import pandas as pd
import eel
from typing import Dict, List, TypedDict, Union

# Initialize eel with your web directory
eel.init('public')  # or wherever your web files are located

class STCParams(TypedDict):
	length: int
	stcLength: int
	smoothingFactor: float
	fastLength: int
	slowLength: int
	upColor: str
	downColor: str

def calculate_correlation(close: List[float], length: int) -> List[float]:
	close_series = pd.Series(close)
	bar_index = pd.Series(range(len(close)))
	correlation = close_series.rolling(window=length).corr(bar_index)
	return correlation.fillna(0).tolist()

def calculate_ema(data: List[float], length: int) -> List[float]:
	return pd.Series(data).ewm(span=length, adjust=False).mean().tolist()

def calculate_macd(source: List[float], params: STCParams) -> Dict[str, List[float]]:
	lag = (9 - 1) / 2
	a1 = 2 / (params['fastLength'] + 1)
	a2 = 2 / (params['slowLength'] + 1)
	
	correlation = calculate_correlation(source, params['length'])
	r2 = [0.5 * pow(r, 2) + 0.5 for r in correlation]
	
	macd = [0.0] * len(source)
	for i in range(2, len(source)):
		K = r2[i] * ((1 - a1) * (1 - a2)) + (1 - r2[i]) * ((1 - a1) / (1 - a2))
		macd[i] = (source[i] - source[i-1]) * (a1 - a2) + \
				  (-a2 - a1 + 2) * macd[i-1] - \
				  K * macd[i-2]
	
	# Calculate signal line and histogram
	signal = calculate_ema(macd, 9)
	histogram = [m - s for m, s in zip(macd, signal)]
	
	return {
		'macd': macd,
		'signal': signal,
		'histogram': histogram
	}

@eel.expose
def calculate_stc(data: Dict[str, List[float]], params: STCParams) -> Dict[str, Union[List[float], List[Dict[str, Union[float, str]]]]]:
	close, high, low = data['close'], data['high'], data['low']
	
	# Initialize variables as in PineScript
	normalized_macd = [0.0] * len(close)
	smoothed_macd = [0.0] * len(close)
	smoothed_normalized_macd = [0.0] * len(close)
	stc_value = [0.0] * len(close)
	
	# Calculate initial MACD
	macd_result = calculate_macd(close, params)
	macd_value = macd_result['macd']
	
	# Calculate price range EMA for normalization
	price_range = [h - l for h, l in zip(high, low)]
	range_ema = calculate_ema(price_range, params['slowLength'])
	
	# Calculate STC following PineScript logic
	for i in range(params['stcLength'], len(close)):
		macd_slice = macd_value[i - params['stcLength'] + 1:i + 1]
		lowest_macd = min(macd_slice)
		highest_macd = max(macd_slice) - lowest_macd
		
		if highest_macd > 0:
			normalized_macd[i] = ((macd_value[i] - lowest_macd) / highest_macd) * 100
		else:
			normalized_macd[i] = normalized_macd[i-1] if i > 0 else 0
			
		smoothed_macd[i] = smoothed_macd[i-1] + params['smoothingFactor'] * (normalized_macd[i] - smoothed_macd[i-1]) if i > 0 else normalized_macd[i]
		
		smoothed_slice = smoothed_macd[i - params['stcLength'] + 1:i + 1]
		lowest_smoothed = min(smoothed_slice)
		highest_smoothed = max(smoothed_slice) - lowest_smoothed
		
		if highest_smoothed > 0:
			smoothed_normalized_macd[i] = ((smoothed_macd[i] - lowest_smoothed) / highest_smoothed) * 100
		else:
			smoothed_normalized_macd[i] = smoothed_normalized_macd[i-1] if i > 0 else 0
			
		stc_value[i] = stc_value[i-1] + params['smoothingFactor'] * (smoothed_normalized_macd[i] - stc_value[i-1]) if i > 0 else smoothed_normalized_macd[i]
	
	# Normalize MACD histogram
	normalized_histogram = [h / r * 100 for h, r in zip(macd_result['histogram'], range_ema)]
	final_histogram = [(h - calculate_ema(normalized_histogram, 9)[i])/2 for i, h in enumerate(normalized_histogram)]
	
	return {
		'stcValue': [v - 50 for v in stc_value],  # Center around zero
		'macdValue': final_histogram,
		'crossovers': calculate_crossovers(stc_value),
		'histogram_colors': calculate_histogram_colors(final_histogram, params)
	}

def calculate_crossovers(stc_values: List[float]) -> List[Dict[str, Union[float, str]]]:
	crossovers = []
	for i in range(1, len(stc_values)):
		if stc_values[i] > stc_values[i-1]:
			crossovers.append({'position': i, 'type': 'up'})
		elif stc_values[i] < stc_values[i-1]:
			crossovers.append({'position': i, 'type': 'down'})
	return crossovers

def calculate_histogram_colors(histogram: List[float], params: STCParams) -> List[str]:
	colors = []
	for i in range(len(histogram)):
		prev_value = histogram[i-1] if i > 0 else 0
		value = histogram[i]
		
		if value > prev_value and value > 0:
			colors.append(params['upColor'])
		elif value < prev_value and value < 0:
			colors.append(params['downColor'])
		elif value < 0:
			colors.append(params['downColor'])
		else:
			colors.append(params['upColor'])
	
	return colors

# Export all functions
__all__ = ['calculate_correlation', 'calculate_macd', 'calculate_stc', 'calculate_ema']

# Start eel if this file is run directly
if __name__ == '__main__':
	eel.start({'port': 3000}, host="localhost", port=8000, mode='custom', block=False)
	while True:
		eel.sleep(1.0)
