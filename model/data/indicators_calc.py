import numpy as np
import pandas as pd
from scipy.stats import linregress
from typing import Tuple, List, Dict, Union

class TrendIndicators:
    @staticmethod
    def moving_average(data: pd.DataFrame, periods: List[int]=[10, 20, 50, 100, 200], ma_type: str='simple') -> Dict[str, pd.Series]:
        mas = {}
        for period in periods:
            if ma_type == 'simple':
                mas[f'SMA_{period}'] = data['Close'].rolling(window=period).mean()
            elif ma_type == 'exponential':
                mas[f'EMA_{period}'] = data['Close'].ewm(span=period, adjust=False).mean()
            elif ma_type == 'weighted':
                weights = np.arange(1, period + 1)
                mas[f'WMA_{period}'] = data['Close'].rolling(window=period).apply(
                    lambda x: np.dot(x, weights) / weights.sum()
                )
            elif ma_type == 'volume_weighted':
                mas[f'VWMA_{period}'] = (data['Close'] * data['Volume']).rolling(window=period).sum() / \
                                      data['Volume'].rolling(window=period).sum()
        return mas

    @staticmethod
    def bollinger_bands(data: pd.DataFrame, period: int=20, std_dev: float=2.0) -> Tuple[pd.Series, pd.Series, pd.Series]:
        middle = data['Close'].rolling(window=period).mean()
        std = data['Close'].rolling(window=period).std()
        upper = middle + (std * std_dev)
        lower = middle - (std * std_dev)
        return middle, upper, lower

    @staticmethod
    def keltner_channels(data: pd.DataFrame, period: int=20, atr_mult: float=2.0) -> Tuple[pd.Series, pd.Series, pd.Series]:
        typical_price = (data['High'] + data['Low'] + data['Close']) / 3
        atr = VolatilityIndicators.average_true_range(data, period)
        middle = typical_price.rolling(window=period).mean()
        upper = middle + (atr * atr_mult)
        lower = middle - (atr * atr_mult)
        return middle, upper, lower

    @staticmethod
    def donchian_channels(data: pd.DataFrame, period: int=20) -> Tuple[pd.Series, pd.Series, pd.Series]:
        upper = data['High'].rolling(window=period).max()
        lower = data['Low'].rolling(window=period).min()
        middle = (upper + lower) / 2
        return upper, middle, lower

    @staticmethod
    def parabolic_sar(data: pd.DataFrame, af_start: float=0.02, af_max: float=0.2, af_step: float=0.02) -> pd.Series:
        high, low = data['High'].values, data['Low'].values
        sar = np.zeros_like(high)
        trend = np.ones_like(high)
        af = np.ones_like(high) * af_start
        extreme_point = high[0]
        
        for i in range(1, len(high)):
            if trend[i-1] == 1:
                sar[i] = sar[i-1] + af[i-1] * (extreme_point - sar[i-1])
                if low[i] < sar[i]:
                    trend[i] = -1
                    sar[i] = extreme_point
                    extreme_point = low[i]
                    af[i] = af_start
                else:
                    trend[i] = 1
                    if high[i] > extreme_point:
                        extreme_point = high[i]
                        af[i] = min(af[i-1] + af_step, af_max)
                    else:
                        af[i] = af[i-1]
            else:
                sar[i] = sar[i-1] + af[i-1] * (extreme_point - sar[i-1])
                if high[i] > sar[i]:
                    trend[i] = 1
                    sar[i] = extreme_point
                    extreme_point = high[i]
                    af[i] = af_start
                else:
                    trend[i] = -1
                    if low[i] < extreme_point:
                        extreme_point = low[i]
                        af[i] = min(af[i-1] + af_step, af_max)
                    else:
                        af[i] = af[i-1]
        
        return pd.Series(sar, index=data.index)

class Oscillators:
    @staticmethod
    def rsi(data: pd.DataFrame, period: int=14) -> pd.Series:
        delta = data['Close'].diff()
        gain = delta.where(delta > 0, 0).rolling(window=period).mean()
        loss = -delta.where(delta < 0, 0).rolling(window=period).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))

    @staticmethod
    def stochastic(data: pd.DataFrame, k_period: int=14, d_period: int=3) -> Tuple[pd.Series, pd.Series]:
        low_min = data['Low'].rolling(window=k_period).min()
        high_max = data['High'].rolling(window=k_period).max()
        k = 100 * (data['Close'] - low_min) / (high_max - low_min)
        d = k.rolling(window=d_period).mean()
        return k, d

    @staticmethod
    def macd(data: pd.DataFrame, fast: int=12, slow: int=26, signal: int=9) -> Tuple[pd.Series, pd.Series, pd.Series]:
        fast_ema = data['Close'].ewm(span=fast, adjust=False).mean()
        slow_ema = data['Close'].ewm(span=slow, adjust=False).mean()
        macd_line = fast_ema - slow_ema
        signal_line = macd_line.ewm(span=signal, adjust=False).mean()
        histogram = macd_line - signal_line
        return macd_line, signal_line, histogram

    @staticmethod
    def williams_r(data: pd.DataFrame, period: int=14) -> pd.Series:
        highest_high = data['High'].rolling(window=period).max()
        lowest_low = data['Low'].rolling(window=period).min()
        wr = -100 * (highest_high - data['Close']) / (highest_high - lowest_low)
        return wr

    @staticmethod
    def cci(data: pd.DataFrame, period: int=20, constant: float=0.015) -> pd.Series:
        typical_price = (data['High'] + data['Low'] + data['Close']) / 3
        sma = typical_price.rolling(window=period).mean()
        mean_deviation = abs(typical_price - sma).rolling(window=period).mean()
        cci = (typical_price - sma) / (constant * mean_deviation)
        return cci

class VolumeIndicators:
    @staticmethod
    def on_balance_volume(data: pd.DataFrame) -> pd.Series:
        return (data['Volume'] * np.where(data['Close'] > data['Close'].shift(1), 1, -1)).cumsum()

    @staticmethod
    def accumulation_distribution(data: pd.DataFrame) -> pd.Series:
        clv = ((data['Close'] - data['Low']) - (data['High'] - data['Close'])) / (data['High'] - data['Low'])
        return (clv * data['Volume']).cumsum()

    @staticmethod
    def money_flow_index(data: pd.DataFrame, period: int=14) -> pd.Series:
        typical_price = (data['High'] + data['Low'] + data['Close']) / 3
        money_flow = typical_price * data['Volume']
        
        positive_flow = pd.Series(np.where(typical_price > typical_price.shift(1), money_flow, 0))
        negative_flow = pd.Series(np.where(typical_price < typical_price.shift(1), money_flow, 0))
        
        positive_mf = positive_flow.rolling(window=period).sum()
        negative_mf = negative_flow.rolling(window=period).sum()
        
        mfi = 100 - (100 / (1 + positive_mf / negative_mf))
        return mfi

    @staticmethod
    def chaikin_money_flow(data: pd.DataFrame, period: int=20) -> pd.Series:
        mf_multiplier = ((data['Close'] - data['Low']) - (data['High'] - data['Close'])) / (data['High'] - data['Low'])
        mf_volume = mf_multiplier * data['Volume']
        cmf = mf_volume.rolling(window=period).sum() / data['Volume'].rolling(window=period).sum()
        return cmf

    @staticmethod
    def volume_price_trend(data: pd.DataFrame) -> pd.Series:
        vpt = ((data['Close'] - data['Close'].shift(1)) / data['Close'].shift(1)) * data['Volume']
        return vpt.cumsum()

class MomentumIndicators:
    @staticmethod
    def awesome_oscillator(data: pd.DataFrame, fast: int=5, slow: int=34) -> pd.Series:
        median_price = (data['High'] + data['Low']) / 2
        ao = median_price.rolling(window=fast).mean() - median_price.rolling(window=slow).mean()
        return ao

    @staticmethod
    def momentum(data: pd.DataFrame, period: int=14) -> pd.Series:
        return data['Close'] - data['Close'].shift(period)

    @staticmethod
    def rate_of_change(data: pd.DataFrame, period: int=14) -> pd.Series:
        return (data['Close'] - data['Close'].shift(period)) / data['Close'].shift(period) * 100

    @staticmethod
    def relative_vigor_index(data: pd.DataFrame, period: int=10) -> pd.Series:
        close_open = data['Close'] - data['Open']
        high_low = data['High'] - data['Low']
        rvi = close_open.rolling(window=period).mean() / high_low.rolling(window=period).mean()
        return rvi

class VolatilityIndicators:
    @staticmethod
    def average_true_range(data: pd.DataFrame, period: int=14) -> pd.Series:
        high_low = data['High'] - data['Low']
        high_close = np.abs(data['High'] - data['Close'].shift())
        low_close = np.abs(data['Low'] - data['Close'].shift())
        ranges = pd.concat([high_low, high_close, low_close], axis=1)
        true_range = ranges.max(axis=1)
        return true_range.rolling(window=period).mean()

    @staticmethod
    def bollinger_bandwidth(data: pd.DataFrame, period: int=20, std_dev: float=2.0) -> pd.Series:
        middle, upper, lower = TrendIndicators.bollinger_bands(data, period, std_dev)
        return (upper - lower) / middle * 100

    @staticmethod
    def keltner_channel_bandwidth(data: pd.DataFrame, period: int=20, atr_mult: float=2.0) -> pd.Series:
        middle, upper, lower = TrendIndicators.keltner_channels(data, period, atr_mult)
        return (upper - lower) / middle * 100

class VolumeProfileIndicators:
    @staticmethod
    def volume_by_price(data: pd.DataFrame, zones: int=12) -> pd.DataFrame:
        price_range = data['High'].max() - data['Low'].min()
        zone_size = price_range / zones
        
        volume_profile = pd.DataFrame()
        for i in range(zones):
            zone_low = data['Low'].min() + (i * zone_size)
            zone_high = zone_low + zone_size
            mask = (data['Close'] >= zone_low) & (data['Close'] < zone_high)
            volume_profile.loc[i, 'Price_Level'] = (zone_low + zone_high) / 2
            volume_profile.loc[i, 'Volume'] = data.loc[mask, 'Volume'].sum()
            
        return volume_profile

    @staticmethod
    def time_price_opportunity(data: pd.DataFrame, zones: int=12) -> pd.DataFrame:
        price_range = data['High'].max() - data['Low'].min()
        zone_size = price_range / zones
        
        tpo_profile = pd.DataFrame()
        for i in range(zones):
            zone_low = data['Low'].min() + (i * zone_size)
            zone_high = zone_low + zone_size
            mask = (data['Close'] >= zone_low) & (data['Close'] < zone_high)
            tpo_profile.loc[i, 'Price_Level'] = (zone_low + zone_high) / 2
            tpo_profile.loc[i, 'TPO_Count'] = mask.sum()
            
        return tpo_profile

class CustomIndicators:
    @staticmethod
    def elder_ray(data: pd.DataFrame, period: int=13) -> Tuple[pd.Series, pd.Series]:
        ema = data['Close'].ewm(span=period, adjust=False).mean()
        bull_power = data['High'] - ema
        bear_power = data['Low'] - ema
        return bull_power, bear_power

    @staticmethod
    def supertrend(data: pd.DataFrame, period: int=10, multiplier: float=3.0) -> Tuple[pd.Series, pd.Series]:
        atr = VolatilityIndicators.average_true_range(data, period)
        
        basic_upperband = ((data['High'] + data['Low']) / 2) + (multiplier * atr)
        basic_lowerband = ((data['High'] + data['Low']) / 2) - (multiplier * atr)
        
        final_upperband = pd.Series(index=data.index)
        final_lowerband = pd.Series(index=data.index)
        supertrend = pd.Series(index=data.index)
        
        for i in range(period, len(data)):
            if basic_upperband[i] < final_upperband[i-1] or data['Close'][i-1] > final_upperband[i-1]:
                final_upperband[i] = basic_upperband[i]
            else:
                final_upperband[i] = final_upperband[i-1]
                
            if basic_lowerband[i] > final_lowerband[i-1] or data['Close'][i-1] < final_lowerband[i-1]:
                final_lowerband[i] = basic_lowerband[i]
            else:
                final_lowerband[i] = final_lowerband[i-1]
                
            if data['Close'][i] > final_upperband[i]:
                supertrend[i] = final_lowerband[i]
            else:
                supertrend[i] = final_upperband[i]
                
        return supertrend, pd.Series(np.where(data['Close'] > supertrend, 1, -1))

    @staticmethod
    def demark_indicators(data: pd.DataFrame) -> Dict[str, pd.Series]:
        setup_buy = np.zeros(len(data))
        setup_sell = np.zeros(len(data))
        
        for i in range(4, len(data)):
            if data['Close'][i] < data['Close'][i-4]:
                setup_buy[i] += 1
            if data['Close'][i] > data['Close'][i-4]:
                setup_sell[i] += 1
                
        countdown_buy = np.zeros(len(data))
        countdown_sell = np.zeros(len(data))
        
        for i in range(13, len(data)):
            if setup_buy[i-13:i].sum() >= 9:
                countdown_buy[i] = 13
            if setup_sell[i-13:i].sum() >= 9:
                countdown_sell[i] = 13
                
        return {
            'setup_buy': pd.Series(setup_buy, index=data.index),
            'setup_sell': pd.Series(setup_sell, index=data.index),
            'countdown_buy': pd.Series(countdown_buy, index=data.index),
            'countdown_sell': pd.Series(countdown_sell, index=data.index)
        }

class AdvancedVolumeIndicators:
    @staticmethod
    def volume_delta(data: pd.DataFrame, period: int=14) -> pd.Series:
        buying_volume = data['Volume'] * (data['Close'] - data['Low']) / (data['High'] - data['Low'])
        selling_volume = data['Volume'] * (data['High'] - data['Close']) / (data['High'] - data['Low'])
        return (buying_volume - selling_volume).rolling(window=period).sum()

    @staticmethod
    def volume_ratio(data: pd.DataFrame, period: int=14) -> pd.Series:
        up_volume = np.where(data['Close'] > data['Close'].shift(1), data['Volume'], 0)
        down_volume = np.where(data['Close'] < data['Close'].shift(1), data['Volume'], 0)
        return pd.Series(up_volume, index=data.index).rolling(period).sum() / \
               pd.Series(down_volume, index=data.index).rolling(period).sum()

    @staticmethod
    def sma(data: pd.Series, period: int = 20) -> pd.Series:
        return data.rolling(window=period).mean()
    
    @staticmethod
    def ema(data: pd.Series, period: int = 20) -> pd.Series:
        return data.ewm(span=period, adjust=False).mean()
    
    @staticmethod
    def wma(data: pd.Series, period: int = 20) -> pd.Series:
        weights = np.arange(1, period + 1)
        return data.rolling(window=period).apply(lambda x: np.dot(x, weights) / weights.sum())
    
    @staticmethod
    def vwma(data: pd.Series, volume: pd.Series, period: int = 20) -> pd.Series:
        return (data * volume).rolling(window=period).sum() / volume.rolling(window=period).sum()

    @staticmethod
    def volume_price_confirmation(data: pd.DataFrame, period: int=14) -> pd.Series:
        return (data['Volume'] * (data['Close'] - data['Close'].shift(1))).rolling(window=period).mean()

    @staticmethod
    def volume_weighted_metrics(data: pd.DataFrame, period: int=14) -> Dict[str, pd.Series]:
        typical = (data['High'] + data['Low'] + data['Close']) / 3
        weighted = (data['High'] * 0.3 + data['Low'] * 0.3 + data['Close'] * 0.4)
        median = (data['High'] + data['Low']) / 2
        
        vw_typical = (typical * data['Volume']).rolling(window=period).sum() / \
                    data['Volume'].rolling(window=period).sum()
        vw_weighted = (weighted * data['Volume']).rolling(window=period).sum() / \
                     data['Volume'].rolling(window=period).sum()
        vw_median = (median * data['Volume']).rolling(window=period).sum() / \
                   data['Volume'].rolling(window=period).sum()
                   
        return {
            'volume_weighted_typical': vw_typical,
            'volume_weighted_weighted': vw_weighted,
            'volume_weighted_median': vw_median
        }

def calculate_all_indicators(data: pd.DataFrame) -> Dict[str, Union[pd.Series, Dict]]:
    """Calculate all technical indicators for the given data."""
    
    indicators = {}
    
    # Trend Indicators
    indicators['moving_averages'] = TrendIndicators.moving_average(data)
    indicators['bollinger_bands'] = TrendIndicators.bollinger_bands(data)
    indicators['keltner_channels'] = TrendIndicators.keltner_channels(data)
    indicators['donchian_channels'] = TrendIndicators.donchian_channels(data)
    indicators['parabolic_sar'] = TrendIndicators.parabolic_sar(data)
    
    # Oscillators
    indicators['rsi'] = Oscillators.rsi(data)
    indicators['stochastic'] = Oscillators.stochastic(data)
    indicators['macd'] = Oscillators.macd(data)
    indicators['williams_r'] = Oscillators.williams_r(data)
    indicators['cci'] = Oscillators.cci(data)
    
    # Volume Indicators
    indicators['obv'] = VolumeIndicators.on_balance_volume(data)
    indicators['ad_line'] = VolumeIndicators.accumulation_distribution(data)
    indicators['mfi'] = VolumeIndicators.money_flow_index(data)
    indicators['cmf'] = VolumeIndicators.chaikin_money_flow(data)
    indicators['vpt'] = VolumeIndicators.volume_price_trend(data)
    
    # Momentum Indicators
    indicators['awesome_oscillator'] = MomentumIndicators.awesome_oscillator(data)
    indicators['momentum'] = MomentumIndicators.momentum(data)
    indicators['roc'] = MomentumIndicators.rate_of_change(data)
    indicators['rvi'] = MomentumIndicators.relative_vigor_index(data)
    
    # Volatility Indicators
    indicators['atr'] = VolatilityIndicators.average_true_range(data)
    indicators['bbw'] = VolatilityIndicators.bollinger_bandwidth(data)
    indicators['kcw'] = VolatilityIndicators.keltner_channel_bandwidth(data)
    
    # Volume Profile
    indicators['vbp'] = VolumeProfileIndicators.volume_by_price(data)
    indicators['tpo'] = VolumeProfileIndicators.time_price_opportunity(data)
    
    # Custom Indicators
    indicators['elder_ray'] = CustomIndicators.elder_ray(data)
    indicators['supertrend'] = CustomIndicators.supertrend(data)
    indicators['demark'] = CustomIndicators.demark_indicators(data)
    
    # Advanced Volume
    indicators['volume_delta'] = AdvancedVolumeIndicators.volume_delta(data)
    indicators['volume_ratio'] = AdvancedVolumeIndicators.volume_ratio(data)
    indicators['volume_price_conf'] = AdvancedVolumeIndicators.volume_price_confirmation(data)
    indicators['volume_weighted'] = AdvancedVolumeIndicators.volume_weighted_metrics(data)
    
    return indicators

