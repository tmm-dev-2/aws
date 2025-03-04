import numpy as np
import pandas as pd
from typing import Dict, List, Tuple
from indicators_calc import (TrendIndicators, Oscillators, VolumeIndicators, 
                           MomentumIndicators, VolatilityIndicators, CustomIndicators, AdvancedVolumeIndicators)
from candle_pattern_calc import CandlePatterns
from drawing_pattern_calc import DrawingTools, ChartPatterns, VolumeProfile, FibonacciTools, GannTools
from drawing_pattern_calc import Point

def organize_all_data() -> pd.DataFrame:
    df = pd.read_csv('../../public/aapl ohlcv data.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    df['Volume'] = df['Volume'].str.replace(',', '').astype(float)
    for col in ['Open', 'High', 'Low', 'Close']:
        df[col] = df[col].astype(float)
    organized_data = {}

    # Get high and low points for Fibonacci tools
    high_point = Point(df['High'].idxmax(), df['High'].max())
    low_point = Point(df['Low'].idxmin(), df['Low'].min())

    def process_result(result, length=len(df)):
        if isinstance(result, (pd.Series, np.ndarray)):
            arr = result.tolist() if len(result.shape) == 1 else result.flatten().tolist()
        elif isinstance(result, (list, tuple)):
            arr = list(result)
        else:
            arr = [result]
        
        # Pad or truncate to match length
        if len(arr) < length:
            arr.extend([np.nan] * (length - len(arr)))
        return arr[:length]

    # Process each pattern and indicator
    for pattern in [
        'bullish_engulfing', 'bearish_engulfing', 'hammer', 'shooting_star',
        'doji', 'morning_star', 'evening_star', 'three_white_soldiers',
        'three_black_crows', 'harami', 'piercing_line', 'dark_cloud_cover',
        'abandoned_baby'
    ]:
        organized_data[pattern] = process_result(getattr(CandlePatterns, pattern)(df))

    # Trend Indicators
    organized_data['moving_averages'] = process_result(TrendIndicators.moving_average(df))
    organized_data['bollinger_bands'] = process_result(TrendIndicators.bollinger_bands(df))
    organized_data['keltner_channels'] = process_result(TrendIndicators.keltner_channels(df))
    organized_data['donchian_channels'] = process_result(TrendIndicators.donchian_channels(df))
    organized_data['parabolic_sar'] = process_result(TrendIndicators.parabolic_sar(df))

    # Oscillators
    organized_data['rsi'] = process_result(Oscillators.rsi(df))
    organized_data['stochastic'] = process_result(Oscillators.stochastic(df))
    organized_data['macd'] = process_result(Oscillators.macd(df))
    organized_data['williams_r'] = process_result(Oscillators.williams_r(df))
    organized_data['cci'] = process_result(Oscillators.cci(df))


    organized_data['moving_averages'] = process_result(TrendIndicators.moving_average(df))
    organized_data['bollinger_bands'] = process_result(TrendIndicators.bollinger_bands(df))
    organized_data['keltner_channels'] = process_result(TrendIndicators.keltner_channels(df))
    organized_data['donchian_channels'] = process_result(TrendIndicators.donchian_channels(df))
    organized_data['parabolic_sar'] = process_result(TrendIndicators.parabolic_sar(df))
    
    # Oscillators
    organized_data['rsi'] = process_result(Oscillators.rsi(df))
    organized_data['stochastic'] = process_result(Oscillators.stochastic(df))
    organized_data['macd'] = process_result(Oscillators.macd(df))
    organized_data['williams_r'] = process_result(Oscillators.williams_r(df))
    organized_data['cci'] = process_result(Oscillators.cci(df))
        
    # Volume Indicators
    organized_data['obv'] = process_result(VolumeIndicators.on_balance_volume(df))
    organized_data['ad_line'] = process_result(VolumeIndicators.accumulation_distribution(df))
    organized_data['mfi'] = process_result(VolumeIndicators.money_flow_index(df))
    organized_data['cmf'] = process_result(VolumeIndicators.chaikin_money_flow(df))
    organized_data['vpt'] = process_result(VolumeIndicators.volume_price_trend(df))
    
    # Momentum Indicators
    organized_data['awesome_oscillator'] = process_result(MomentumIndicators.awesome_oscillator(df))
    organized_data['momentum'] = process_result(MomentumIndicators.momentum(df))
    organized_data['roc'] = process_result(MomentumIndicators.rate_of_change(df))
    organized_data['rvi'] = process_result(MomentumIndicators.relative_vigor_index(df))
        
    # Volatility Indicators
    organized_data['atr'] =process_result(VolatilityIndicators.average_true_range(df))
    organized_data['bbw'] = process_result(VolatilityIndicators.bollinger_bandwidth(df))
    organized_data['kcw'] = process_result(VolatilityIndicators.keltner_channel_bandwidth(df))

    # Custom Indicators
    organized_data['elder_ray'] = process_result(CustomIndicators.elder_ray(df))
    organized_data['supertrend'] = process_result(CustomIndicators.supertrend(df))
    organized_data['demark'] = process_result(CustomIndicators.demark_indicators(df))
        
    # Advanced Volume
    organized_data['volume_delta'] = process_result(AdvancedVolumeIndicators.volume_delta(df))
    organized_data['volume_ratio'] = process_result(AdvancedVolumeIndicators.volume_ratio(df))
    organized_data['volume_price_conf'] = process_result(AdvancedVolumeIndicators.volume_price_confirmation(df))
    organized_data['volume_weighted'] = process_result(AdvancedVolumeIndicators.volume_weighted_metrics(df))
    
    # Volume Indicators
    organized_data['obv'] = process_result(VolumeIndicators.on_balance_volume(df))
    organized_data['ad_line'] = process_result(VolumeIndicators.accumulation_distribution(df))
    organized_data['mfi'] = process_result(VolumeIndicators.money_flow_index(df))
    organized_data['cmf'] = process_result(VolumeIndicators.chaikin_money_flow(df))
    organized_data['vpt'] = process_result(VolumeIndicators.volume_price_trend(df))

    # Momentum Indicators
    organized_data['awesome_oscillator'] = process_result(MomentumIndicators.awesome_oscillator(df))
    organized_data['momentum'] = process_result(MomentumIndicators.momentum(df))
    organized_data['roc'] = process_result(MomentumIndicators.rate_of_change(df))
    organized_data['rvi'] = process_result(MomentumIndicators.relative_vigor_index(df))

    # Volatility Indicators
    organized_data['atr'] = process_result(VolatilityIndicators.average_true_range(df))
    organized_data['bbw'] = process_result(VolatilityIndicators.bollinger_bandwidth(df))
    organized_data['kcw'] = process_result(VolatilityIndicators.keltner_channel_bandwidth(df))

    # Chart Patterns
    organized_data['head_and_shoulders'] = process_result(ChartPatterns.head_and_shoulders(df))
    organized_data['double_patterns'] = process_result(ChartPatterns.double_top_bottom(df))

    # Volume Profile
    organized_data['volume_profile'] = process_result(VolumeProfile.calculate(df))

    # Custom Indicators
    organized_data['elder_ray'] = process_result(CustomIndicators.elder_ray(df))
    organized_data['supertrend'] = process_result(CustomIndicators.supertrend(df))
    organized_data['demark'] = process_result(CustomIndicators.demark_indicators(df))

    # Advanced Volume Indicators
    organized_data['volume_delta'] = process_result(AdvancedVolumeIndicators.volume_delta(df))
    organized_data['volume_ratio'] = process_result(AdvancedVolumeIndicators.volume_ratio(df))
    organized_data['volume_price_conf'] = process_result(AdvancedVolumeIndicators.volume_price_confirmation(df))
    organized_data['volume_weighted'] = process_result(AdvancedVolumeIndicators.volume_weighted_metrics(df))

    # Drawing Tools
    organized_data['fibonacci_tools'] = process_result(FibonacciTools.retracements(high_point, low_point))
    organized_data['gann_tools'] = process_result(GannTools.fan(Point(0, df['Close'].iloc[0]), len(df)))

    # Convert to DataFrame and save
    organized_df = pd.DataFrame(organized_data)
    organized_df.to_csv('organized_training_data.csv', index=False)
    print(f"Successfully organized {len(organized_df)} samples with all patterns and indicators")
    return organized_df

if __name__ == "__main__":
    df = organize_all_data()
