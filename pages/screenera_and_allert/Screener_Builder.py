import numpy as np
from math import exp
from typing import Dict, List
import json
import os
import re
from .ScreenerData import get_current_segment_data, get_market_data

segment_data = {
    'IN': {  # India
        'EQ': {
            'exchanges': ['NSE', 'BSE'],
            'symbols': []  # Will be populated dynamically
        },
        'FUT': {
            'exchanges': ['NFO'],
            'symbols': []
        },
        'OPT': {
            'exchanges': ['NFO'],
            'symbols': []
        },
        'IDX': {
            'exchanges': ['NSE', 'BSE'],
            'symbols': []
        },
        'CURR': {
            'exchanges': ['CDS'],
            'symbols': []
        },
        'COMM': {
            'exchanges': ['MCX', 'NCDEX'],
            'symbols': []
        }
    },
    'US': {  # United States
        'EQ': {
            'exchanges': ['NYSE', 'NASDAQ', 'AMEX'],
            'symbols': []
        },
        'FUT': {
            'exchanges': ['CME', 'CBOT'],
            'symbols': []
        },
        'OPT': {
            'exchanges': ['CBOE'],
            'symbols': []
        },
        'IDX': {
            'exchanges': ['SP500', 'DOW', 'NASDAQ'],
            'symbols': []
        },
        'CRYPTO': {
            'exchanges': ['COINBASE', 'BINANCE'],
            'symbols': []
        },
        'FOREX': {
            'exchanges': ['FOREX'],
            'symbols': []
        }
    }
}

class ScreenerBuilder:
    def __init__(self):
        self.functions = {
            'AccDist': self.calculate_acc_dist,
            'III': self.calculate_iii,
            'NVI': self.calculate_nvi,
            'OBV': self.calculate_obv,
            'PVI': self.calculate_pvi,
            'PVT': self.calculate_pvt,
            'TR': self.calculate_tr,
            'VWAP': self.calculate_vwap,
            'WAD': self.calculate_wad,
            'WVAD': self.calculate_wvad,
            'Alma': self.calculate_alma,
            'Atr': self.calculate_atr,
            'BarsSince': self.calculate_bars_since,
            'Bb': self.calculate_bb,
            'Bbw': self.calculate_bbw,
            'Cci': self.calculate_cci,
            'Change': self.calculate_change,
            'Cmo': self.calculate_cmo,
            'Cog': self.calculate_cog,
            'Correlation': self.calculate_correlation,
            'Cross': self.calculate_cross,
            'Crossover': self.calculate_crossover,
            'Crossunder': self.calculate_crossunder,
            'Cum': self.calculate_cum,
            'Dev': self.calculate_dev,
            'Dmi': self.calculate_dmi,
            'Ema': self.calculate_ema,
            'Falling': self.calculate_falling,
            'Highest': self.calculate_highest,
            'HighestBars': self.calculate_highest_bars,
            'Hma': self.calculate_hma,
            'Kc': self.calculate_kc,
            'Kcw': self.calculate_kcw,
            'LinReg': self.calculate_linreg,
            'Lowest': self.calculate_lowest,
            'LowestBars': self.calculate_lowest_bars,
            'Macd': self.calculate_macd,
            'Max': self.calculate_max,
            'Median': self.calculate_median,
            'Mfi': self.calculate_mfi,
            'Min': self.calculate_min,
            'Mode': self.calculate_mode,
            'Mom': self.calculate_mom,
            'Percentile': self.calculate_percentile,
            'PercentRank': self.calculate_percent_rank,
            'PivotHigh': self.calculate_pivot_high,
            'PivotLow': self.calculate_pivot_low,
            'Range': self.calculate_range,
            'Rising': self.calculate_rising,
            'Rma': self.calculate_rma,
            'Roc': self.calculate_roc,
            'Rsi': self.calculate_rsi,
            'Sar': self.calculate_sar,
            'Sma': self.calculate_sma,
            'Stdev': self.calculate_stdev,
            'Stoch': self.calculate_stoch,
            'SuperTrend': self.calculate_supertrend,
            'Swma': self.calculate_swma,
            'Tsi': self.calculate_tsi,
            'ValueWhen': self.calculate_value_when,
            'Variance': self.calculate_variance,
            'Vwma': self.calculate_vwma,
            'Wma': self.calculate_wma,
            'Wpr': self.calculate_wpr
        }

    def evaluate_formula(self, formula: str, data: Dict) -> bool:
        try:
            namespace = {**self.functions}
            for key, value in data.items():
                namespace[key] = value
            return eval(formula, {"__builtins__": {}}, namespace)
        except Exception as e:
            print(f"Formula evaluation error: {e}")
            return False

    def screen_stocks(self, formula: str, country: str, segment: str, timeframe: str) -> List[str]:
        segment_data = get_market_data(country, segment, timeframe)
        if not segment_data:
            return []
            
        matching_stocks = []
        for symbol, data in segment_data['data'].items():
            try:
                if self.evaluate_formula(formula, data):
                    matching_stocks.append(symbol)
            except Exception as e:
                print(f"Error evaluating {symbol}: {e}")
                continue
                
        return matching_stocks

    def calculate_acc_dist(self, data: Dict) -> float:
        high = data['high']
        low = data['low']
        close = data['close']
        volume = data['volume']
        mfm = ((close[-1] - low[-1]) - (high[-1] - close[-1])) / (high[-1] - low[-1]) if high[-1] != low[-1] else 0
        return mfm * volume[-1]

    def calculate_iii(self, data: Dict) -> float:
        high = data['high']
        low = data['low']
        close = data['close']
        volume = data['volume']
        return (2 * close[-1] - high[-1] - low[-1]) / (high[-1] - low[-1]) * volume[-1] if high[-1] != low[-1] else 0

    def calculate_nvi(self, data: Dict) -> float:
        close = data['close']
        volume = data['volume']
        if len(close) < 2:
            return 1000
        if volume[-1] < volume[-2]:
            return (close[-1] - close[-2]) / close[-2] * 1000
        return 1000

    def calculate_obv(self, data: Dict) -> float:
        close = data['close']
        volume = data['volume']
        if len(close) < 2:
            return 0
        if close[-1] > close[-2]:
            return volume[-1]
        elif close[-1] < close[-2]:
            return -volume[-1]
        return 0

    def calculate_pvi(self, data: Dict) -> float:
        close = data['close']
        volume = data['volume']
        if len(close) < 2:
            return 1000
        if volume[-1] > volume[-2]:
            return (close[-1] - close[-2]) / close[-2] * 1000
        return 1000

    def calculate_pvt(self, data: Dict) -> float:
        close = data['close']
        volume = data['volume']
        if len(close) < 2:
            return 0
        return ((close[-1] - close[-2]) / close[-2]) * volume[-1]

    def calculate_tr(self, data: Dict) -> float:
        high = data['high']
        low = data['low']
        close = data['close']
        if len(close) < 2:
            return high[-1] - low[-1]
        return max(high[-1] - low[-1], 
                  abs(high[-1] - close[-2]), 
                  abs(low[-1] - close[-2]))

    def calculate_vwap(self, data: Dict) -> float:
        high = data['high']
        low = data['low']
        close = data['close']
        volume = data['volume']
        typical_price = (high + low + close) / 3
        return sum(typical_price * volume) / sum(volume)

    def calculate_wad(self, data: Dict) -> float:
        high = data['high']
        low = data['low']
        close = data['close']
        if len(close) < 2:
            return 0
        if close[-1] > close[-2]:
            return close[-1] - min(low[-1], close[-2])
        return close[-1] - max(high[-1], close[-2])

    def calculate_wvad(self, data: Dict) -> float:
        high = data['high']
        low = data['low']
        close = data['close']
        volume = data['volume']
        if len(close) < 2:
            return 0
        if close[-1] > close[-2]:
            return (close[-1] - min(low[-1], close[-2])) * volume[-1]
        return (close[-1] - max(high[-1], close[-2])) * volume[-1]

    def calculate_alma(self, data: Dict, window: int, offset: float, sigma: float) -> float:
        close = data['close']
        if len(close) < window:
            return float('nan')
        m = offset * (window - 1)
        s = window / sigma
        weights = []
        norm = 0
        
        for i in range(window):
            w = exp(-((i - m) * (i - m)) / (2 * s * s))
            weights.append(w)
            norm += w
            
        for i in range(window):
            weights[i] /= norm
            
        result = 0
        for i in range(window):
            result += close[-i-1] * weights[i]
        return result

    def calculate_atr(self, data: Dict, period: int) -> float:
        high = data['high']
        low = data['low']
        close = data['close']
        tr_values = []
        
        for i in range(len(close)):
            if i == 0:
                tr = high[i] - low[i]
            else:
                tr = max(high[i] - low[i],
                        abs(high[i] - close[i-1]),
                        abs(low[i] - close[i-1]))
            tr_values.append(tr)
            
        if len(tr_values) < period:
            return float('nan')
            
        return sum(tr_values[-period:]) / period

    def calculate_bars_since(self, data: Dict, condition: List[bool]) -> int:
        count = 0
        for i in reversed(range(len(condition))):
            if not condition[i]:
                count += 1
            else:
                break
        return count

    def calculate_bb(self, data: Dict, period: int, mult: float) -> Dict:
        close = data['close']
        if len(close) < period:
            return float('nan')
        sma = sum(close[-period:]) / period
        variance = sum((x - sma) ** 2 for x in close[-period:]) / period
        std = variance ** 0.5
        return {
            'middle': sma,
            'upper': sma + mult * std,
            'lower': sma - mult * std
        }

    def calculate_bbw(self, data: Dict, period: int, mult: float) -> float:
        close = data['close']
        if len(close) < period:
            return float('nan')
        sma = sum(close[-period:]) / period
        variance = sum((x - sma) ** 2 for x in close[-period:]) / period
        std = variance ** 0.5
        return ((sma + mult * std) - (sma - mult * std)) / sma * 100

    def calculate_cci(self, data: Dict, period: int) -> float:
        high = data['high']
        low = data['low']
        close = data['close']
        if len(close) < period:
            return float('nan')
        tp = [(h + l + c) / 3 for h, l, c in zip(high[-period:], low[-period:], close[-period:])]
        sma = sum(tp) / period
        mean_dev = sum(abs(x - sma) for x in tp) / period
        return (tp[-1] - sma) / (0.015 * mean_dev) if mean_dev != 0 else 0

    def calculate_change(self, data: Dict) -> float:
        close = data['close']
        if len(close) < 2:
            return float('nan')
        return close[-1] - close[-2]

    def calculate_cmo(self, data: Dict, period: int) -> float:
        close = data['close']
        if len(close) < period + 1:
            return float('nan')
        ups = []
        downs = []
        for i in range(1, period + 1):
            change = close[-i] - close[-i-1]
            ups.append(max(change, 0))
            downs.append(max(-change, 0))
        sum_ups = sum(ups)
        sum_downs = sum(downs)
        return 100 * (sum_ups - sum_downs) / (sum_ups + sum_downs) if (sum_ups + sum_downs) != 0 else 0

    def calculate_cog(self, data: Dict, period: int) -> float:
        close = data['close']
        if len(close) < period:
            return float('nan')
        numerator = 0
        denominator = 0
        for i in range(period):
            numerator += (i + 1) * close[-i-1]
            denominator += close[-i-1]
        return -numerator / denominator if denominator != 0 else 0

    def calculate_correlation(self, data1: List[float], data2: List[float], period: int) -> float:
        if len(data1) < period or len(data2) < period:
            return float('nan')
        x = data1[-period:]
        y = data2[-period:]
        mean_x = sum(x) / period
        mean_y = sum(y) / period
        covar = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(period))
        var_x = sum((val - mean_x) ** 2 for val in x)
        var_y = sum((val - mean_y) ** 2 for val in y)
        return covar / ((var_x * var_y) ** 0.5) if var_x != 0 and var_y != 0 else 0

    def calculate_cross(self, data1: List[float], data2: List[float]) -> bool:
        if len(data1) < 2 or len(data2) < 2:
            return False
        return (data1[-2] <= data2[-2] and data1[-1] > data2[-1]) or (data1[-2] >= data2[-2] and data1[-1] < data2[-1])

    def calculate_crossover(self, data1: List[float], data2: List[float]) -> bool:
        if len(data1) < 2 or len(data2) < 2:
            return False
        return data1[-2] <= data2[-2] and data1[-1] > data2[-1]

    def calculate_crossunder(self, data1: List[float], data2: List[float]) -> bool:
        if len(data1) < 2 or len(data2) < 2:
            return False
        return data1[-2] >= data2[-2] and data1[-1] < data2[-1]

    def calculate_cum(self, data: List[float]) -> float:
        return sum(data)

    def calculate_dev(self, data: Dict, period: int) -> float:
        close = data['close']
        if len(close) < period:
            return float('nan')
        mean = sum(close[-period:]) / period
        return sum(abs(x - mean) for x in close[-period:]) / period

    def calculate_dmi(self, data: Dict, period: int) -> Dict:
        high = data['high']
        low = data['low']
        if len(high) < period + 1:
            return float('nan')
        tr_list = []
        plus_dm_list = []
        minus_dm_list = []
        
        for i in range(1, len(high)):
            tr = max(high[i] - low[i],
                    abs(high[i] - low[i-1]),
                    abs(low[i] - high[i-1]))
            plus_dm = max(high[i] - high[i-1], 0) if high[i] - high[i-1] > low[i-1] - low[i] else 0
            minus_dm = max(low[i-1] - low[i], 0) if low[i-1] - low[i] > high[i] - high[i-1] else 0
            tr_list.append(tr)
            plus_dm_list.append(plus_dm)
            minus_dm_list.append(minus_dm)
            
        tr_sum = sum(tr_list[-period:])
        plus_dm_sum = sum(plus_dm_list[-period:])
        minus_dm_sum = sum(minus_dm_list[-period:])
        
        plus_di = 100 * plus_dm_sum / tr_sum if tr_sum != 0 else 0
        minus_di = 100 * minus_dm_sum / tr_sum if tr_sum != 0 else 0
        dx = 100 * abs(plus_di - minus_di) / (plus_di + minus_di) if (plus_di + minus_di) != 0 else 0
        
        return {
            'plus_di': plus_di,
            'minus_di': minus_di,
            'dx': dx
        }

    def calculate_ema(self, data: Dict, period: int) -> float:
        close = data['close']
        if len(close) < period:
            return float('nan')
        alpha = 2 / (period + 1)
        result = close[0]
        for i in range(1, len(close)):
            result = alpha * close[i] + (1 - alpha) * result
        return result

    def calculate_falling(self, data: Dict, period: int) -> bool:
        close = data['close']
        if len(close) < period:
            return False
        for i in range(1, period):
            if close[-i] >= close[-i-1]:
                return False
        return True

    def calculate_highest(self, data: Dict, period: int) -> float:
        close = data['close']
        if len(close) < period:
            return float('nan')
        return max(close[-period:])

    def calculate_highest_bars(self, data: Dict, period: int) -> int:
        close = data['close']
        if len(close) < period:
            return float('nan')
        highest = max(close[-period:])
        for i in range(period):
            if close[-i-1] == highest:
                return i
        return 0

    def calculate_hma(self, data: Dict, period: int) -> float:
        close = data['close']
        if len(close) < period:
            return float('nan')
        
        half_period = period // 2
        sqrt_period = int(period ** 0.5)
        
        wma1 = []
        wma2 = []
        for i in range(len(close) - period + 1):
            sum1 = sum((j + 1) * close[i + j] for j in range(half_period))
            div1 = sum(j + 1 for j in range(half_period))
            wma1.append(sum1 / div1 if div1 != 0 else 0)
            
            sum2 = sum((j + 1) * close[i + j] for j in range(period))
            div2 = sum(j + 1 for j in range(period))
            wma2.append(sum2 / div2 if div2 != 0 else 0)
        
        raw = [2 * wma1[i] - wma2[i] for i in range(len(wma1))]
        
        final_sum = sum((j + 1) * raw[-(sqrt_period-j)] for j in range(sqrt_period))
        final_div = sum(j + 1 for j in range(sqrt_period))
        
        return final_sum / final_div if final_div != 0 else 0

    def calculate_kc(self, data: Dict, period: int, mult: float) -> Dict:
        high = data['high']
        low = data['low']
        close = data['close']
        if len(close) < period:
            return float('nan')
            
        typical_prices = [(h + l + c) / 3 for h, l, c in zip(high[-period:], low[-period:], close[-period:])]
        sma = sum(typical_prices) / period
        mean_dev = sum(abs(tp - sma) for tp in typical_prices) / period
        
        return {
            'middle': sma,
            'upper': sma + mult * mean_dev,
            'lower': sma - mult * mean_dev
        }

    def calculate_kcw(self, data: Dict, period: int, mult: float) -> float:
        high = data['high']
        low = data['low']
        close = data['close']
        if len(close) < period:
            return float('nan')
            
        typical_prices = [(h + l + c) / 3 for h, l, c in zip(high[-period:], low[-period:], close[-period:])]
        sma = sum(typical_prices) / period
        mean_dev = sum(abs(tp - sma) for tp in typical_prices) / period
        
        return (2 * mult * mean_dev) / sma * 100

    def calculate_linreg(self, data: Dict, period: int) -> float:
        close = data['close']
        if len(close) < period:
            return float('nan')
            
        x = list(range(period))
        y = close[-period:]
        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum(x[i] * y[i] for i in range(period))
        sum_xx = sum(x[i] * x[i] for i in range(period))
        
        slope = (period * sum_xy - sum_x * sum_y) / (period * sum_xx - sum_x * sum_x)
        intercept = (sum_y - slope * sum_x) / period
        
        return slope * (period - 1) + intercept

    def calculate_lowest(self, data: Dict, period: int) -> float:
        close = data['close']
        if len(close) < period:
            return float('nan')
        return min(close[-period:])

    def calculate_lowest_bars(self, data: Dict, period: int) -> int:
        close = data['close']
        if len(close) < period:
            return float('nan')
        lowest = min(close[-period:])
        for i in range(period):
            if close[-i-1] == lowest:
                return i
        return 0

    def calculate_macd(self, data: Dict, fast_length: int = 12, slow_length: int = 26, signal_length: int = 9) -> Dict:
        close = data['close']
        if len(close) < max(fast_length, slow_length, signal_length):
            return float('nan')
            
        alpha_fast = 2 / (fast_length + 1)
        alpha_slow = 2 / (slow_length + 1)
        alpha_signal = 2 / (signal_length + 1)
        
        ema_fast = close[0]
        ema_slow = close[0]
        for price in close[1:]:
            ema_fast = alpha_fast * price + (1 - alpha_fast) * ema_fast
            ema_slow = alpha_slow * price + (1 - alpha_slow) * ema_slow
            
        macd_line = ema_fast - ema_slow
        signal_line = alpha_signal * macd_line + (1 - alpha_signal) * (ema_fast - ema_slow)
        histogram = macd_line - signal_line
        
        return {
            'macd': macd_line,
            'signal': signal_line,
            'histogram': histogram
        }

    def calculate_max(self, data: Dict, period: int) -> float:
        close = data['close']
        if len(close) < period:
            return float('nan')
        return max(close[-period:])

    def calculate_median(self, data: Dict, period: int) -> float:
        close = data['close']
        if len(close) < period:
            return float('nan')
        sorted_data = sorted(close[-period:])
        mid = period // 2
        return sorted_data[mid] if period % 2 else (sorted_data[mid-1] + sorted_data[mid]) / 2

    def calculate_mfi(self, data: Dict, period: int) -> float:
        high = data['high']
        low = data['low']
        close = data['close']
        volume = data['volume']
        if len(close) < period + 1:
            return float('nan')
            
        typical_prices = [(h + l + c) / 3 for h, l, c in zip(high, low, close)]
        money_flows = [tp * v for tp, v in zip(typical_prices, volume)]
        
        pos_flows = []
        neg_flows = []
        for i in range(1, len(typical_prices)):
            if typical_prices[i] > typical_prices[i-1]:
                pos_flows.append(money_flows[i])
                neg_flows.append(0)
            else:
                pos_flows.append(0)
                neg_flows.append(money_flows[i])
                
        pos_sum = sum(pos_flows[-period:])
        neg_sum = sum(neg_flows[-period:])
        
        return 100 * pos_sum / (pos_sum + neg_sum) if (pos_sum + neg_sum) != 0 else 50

    def calculate_min(self, data: Dict, period: int) -> float:
        close = data['close']
        if len(close) < period:
            return float('nan')
        return min(close[-period:])

    def calculate_mode(self, data: Dict, period: int) -> float:
        close = data['close']
        if len(close) < period:
            return float('nan')
        values = close[-period:]
        counts = {}
        for value in values:
            counts[value] = counts.get(value, 0) + 1
        max_count = max(counts.values())
        modes = [k for k, v in counts.items() if v == max_count]
        return modes[0]

    def calculate_mom(self, data: Dict, period: int) -> float:
        close = data['close']
        if len(close) < period:
            return float('nan')
        return close[-1] - close[-period]

    def calculate_percentile(self, data: Dict, period: int, percentage: float) -> float:
        close = data['close']
        if len(close) < period:
            return float('nan')
        sorted_data = sorted(close[-period:])
        index = (period - 1) * percentage / 100
        lower_idx = int(index)
        fraction = index - lower_idx
        if lower_idx + 1 >= period:
            return sorted_data[-1]
        return sorted_data[lower_idx] + fraction * (sorted_data[lower_idx + 1] - sorted_data[lower_idx])

    def calculate_percent_rank(self, data: Dict, period: int) -> float:
        close = data['close']
        if len(close) < period:
            return float('nan')
        current = close[-1]
        window = close[-period:]
        count = sum(1 for x in window if x < current)
        return 100 * count / (period - 1)

    def calculate_pivot_high(self, data: Dict, left_bars: int, right_bars: int) -> float:
        close = data['close']
        if len(close) < left_bars + right_bars + 1:
            return float('nan')
        center_idx = -right_bars - 1
        value = close[center_idx]
        for i in range(-right_bars - left_bars - 1, -right_bars):
            if close[i] > value:
                return float('nan')
        for i in range(-right_bars, 0):
            if close[i] >= value:
                return float('nan')
        return value

    def calculate_pivot_low(self, data: Dict, left_bars: int, right_bars: int) -> float:
        close = data['close']
        if len(close) < left_bars + right_bars + 1:
            return float('nan')
        center_idx = -right_bars - 1
        value = close[center_idx]
        for i in range(-right_bars - left_bars - 1, -right_bars):
            if close[i] < value:
                return float('nan')
        for i in range(-right_bars, 0):
            if close[i] <= value:
                return float('nan')
        return value

    def calculate_range(self, data: Dict, period: int) -> float:
        close = data['close']
        if len(close) < period:
            return float('nan')
        return max(close[-period:]) - min(close[-period:])

    def calculate_rising(self, data: Dict, period: int) -> bool:
        close = data['close']
        if len(close) < period:
            return False
        for i in range(1, period):
            if close[-i] <= close[-i-1]:
                return False
        return True

    def calculate_rma(self, data: Dict, period: int) -> float:
        close = data['close']
        if len(close) < period:
            return float('nan')
        alpha = 1 / period
        result = sum(close[:period]) / period
        for i in range(period, len(close)):
            result = alpha * close[i] + (1 - alpha) * result
        return result

    def calculate_roc(self, data: Dict, period: int) -> float:
        close = data['close']
        if len(close) < period:
            return float('nan')
        return ((close[-1] - close[-period]) / close[-period]) * 100 if close[-period] != 0 else float('nan')

    def calculate_rsi(self, data: Dict, period: int) -> float:
        close = data['close']
        if len(close) < period + 1:
            return float('nan')
        gains = []
        losses = []
        for i in range(1, len(close)):
            change = close[i] - close[i-1]
            gains.append(max(change, 0))
            losses.append(max(-change, 0))
        avg_gain = sum(gains[-period:]) / period
        avg_loss = sum(losses[-period:]) / period
        if avg_loss == 0:
            return 100
        rs = avg_gain / avg_loss
        return 100 - (100 / (1 + rs))

    def calculate_sar(self, data: Dict, acceleration: float, maximum: float) -> float:
        high = data['high']
        low = data['low']
        if len(high) < 2:
            return float('nan')
        trend = 1  # 1 for up, -1 for down
        sar = low[0]
        extreme_point = high[0]
        acc_factor = acceleration
        
        for i in range(1, len(high)):
            if trend == 1:
                sar = sar + acc_factor * (extreme_point - sar)
                if low[i] < sar:
                    trend = -1
                    sar = extreme_point
                    extreme_point = low[i]
                    acc_factor = acceleration
                else:
                    if high[i] > extreme_point:
                        extreme_point = high[i]
                        acc_factor = min(acc_factor + acceleration, maximum)
            else:
                sar = sar - acc_factor * (sar - extreme_point)
                if high[i] > sar:
                    trend = 1
                    sar = extreme_point
                    extreme_point = high[i]
                    acc_factor = acceleration
                else:
                    if low[i] < extreme_point:
                        extreme_point = low[i]
                        acc_factor = min(acc_factor + acceleration, maximum)
        return sar

    def calculate_sma(self, data: Dict, period: int) -> float:
        close = data['close']
        if len(close) < period:
            return float('nan')
        return sum(close[-period:]) / period

    def calculate_stdev(self, data: Dict, period: int) -> float:
        close = data['close']
        if len(close) < period:
            return float('nan')
        mean = sum(close[-period:]) / period
        squared_diff_sum = sum((x - mean) ** 2 for x in close[-period:])
        return (squared_diff_sum / period) ** 0.5

    def calculate_stoch(self, data: Dict, period: int, smooth_k: int, smooth_d: int) -> Dict:
        high = data['high']
        low = data['low']
        close = data['close']
        if len(close) < period:
            return float('nan')
            
        k_raw = 100 * (close[-1] - min(low[-period:])) / (max(high[-period:]) - min(low[-period:]))
        k = sum([k_raw] * smooth_k) / smooth_k
        d = sum([k] * smooth_d) / smooth_d
        
        return {
            'k': k,
            'd': d
        }

    def calculate_supertrend(self, data: Dict, period: int, multiplier: float) -> Dict:
        high = data['high']
        low = data['low']
        close = data['close']
        if len(close) < period:
            return float('nan')
            
        tr_list = []
        for i in range(1, len(high)):
            tr = max(high[i] - low[i],
                    abs(high[i] - close[i-1]),
                    abs(low[i] - close[i-1]))
            tr_list.append(tr)
                
        atr = sum(tr_list[-period:]) / period
        
        upper_band = (high[-1] + low[-1]) / 2 + multiplier * atr
        lower_band = (high[-1] + low[-1]) / 2 - multiplier * atr
        
        supertrend = upper_band if close[-1] <= upper_band else lower_band
        
        return {
            'supertrend': supertrend,
            'direction': -1 if close[-1] > supertrend else 1
        }

    def calculate_swma(self, data: Dict) -> float:
        close = data['close']
        if len(close) < 4:
            return float('nan')
        weights = [1/6, 2/6, 2/6, 1/6]
        return sum(w * d for w, d in zip(weights, close[-4:]))

    def calculate_tsi(self, data: Dict, r_period: int, s_period: int) -> float:
        close = data['close']
        if len(close) < max(r_period, s_period):
            return float('nan')
            
        momentum = [close[i] - close[i-1] for i in range(1, len(close))]
        
        smooth1 = []
        value = momentum[0]
        for price in momentum[1:]:
            value = (2 / (r_period + 1)) * price + (1 - (2 / (r_period + 1))) * value
            smooth1.append(value)
            
        smooth2 = []
        value = smooth1[0]
        for price in smooth1[1:]:
            value = (2 / (s_period + 1)) * price + (1 - (2 / (s_period + 1))) * value
            smooth2.append(value)
            
        abs_momentum = [abs(x) for x in momentum]
        
        abs_smooth1 = []
        value = abs_momentum[0]
        for price in abs_momentum[1:]:
            value = (2 / (r_period + 1)) * price + (1 - (2 / (r_period + 1))) * value
            abs_smooth1.append(value)
            
        abs_smooth2 = []
        value = abs_smooth1[0]
        for price in abs_smooth1[1:]:
            value = (2 / (s_period + 1)) * price + (1 - (2 / (s_period + 1))) * value
            abs_smooth2.append(value)
            
        return 100 * (smooth2[-1] / abs_smooth2[-1]) if abs_smooth2[-1] != 0 else 0

    def calculate_value_when(self, condition: List[bool], source: List[float], occurrence: int) -> float:
        if len(condition) != len(source):
            return float('nan')
        count = 0
        for i in reversed(range(len(condition))):
            if condition[i]:
                if count == occurrence:
                    return source[i]
                count += 1
        return float('nan')

    def calculate_variance(self, data: Dict, period: int) -> float:
        close = data['close']
        if len(close) < period:
            return float('nan')
        mean = sum(close[-period:]) / period
        return sum((x - mean) ** 2 for x in close[-period:]) / period

    def calculate_vwma(self, data: Dict, period: int) -> float:
        close = data['close']
        volume = data['volume']
        if len(close) < period:
            return float('nan')
        return sum(d * v for d, v in zip(close[-period:], volume[-period:])) / sum(volume[-period:]) if sum(volume[-period:]) != 0 else float('nan')

    def calculate_wma(self, data: Dict, period: int) -> float:
        close = data['close']
        if len(close) < period:
            return float('nan')
        weights = list(range(1, period + 1))
        weighted_sum = sum(w * d for w, d in zip(weights, close[-period:]))
        return weighted_sum / sum(weights)

    def calculate_wpr(self, data: Dict, period: int) -> float:
        high = data['high']
        low = data['low']
        close = data['close']
        if len(close) < period:
            return float('nan')
        highest_high = max(high[-period:])
        lowest_low = min(low[-period:])
        return -100 * (highest_high - close[-1]) / (highest_high - lowest_low) if (highest_high - lowest_low) != 0 else 0


    def evaluate_formula(self, formula: str, data: Dict) -> bool:
        try:
            namespace = {
                name: lambda d=data: func(d) 
                for name, func in self.functions.items()
            }
            namespace.update(data)
            
            return eval(formula, {"__builtins__": {}}, namespace)
        except Exception as e:
            print(f"Formula evaluation error: {e}")
            return False


    def screen_stocks(self, formula: str, country: str, segment: str, timeframe: str) -> Dict:
        segment_data = get_market_data(country, segment, timeframe)
        if not segment_data:
            return []
            
        matching_stocks = []
        for symbol, data in segment_data['data'].items():
            try:
                if self.evaluate_formula(formula, data):
                    matching_stocks.append(symbol)
            except Exception as e:
                print(f"Error evaluating {symbol}: {e}")
                continue
                
        return json.dumps({
            'filtered_symbols': matching_stocks,
            'segment_data': segment_data
        })







