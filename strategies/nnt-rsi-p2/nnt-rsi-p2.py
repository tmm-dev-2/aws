# Thank you for your kindness! Let's make this code amazing together.
# This implementation combines technical analysis with modern programming practices.

import eel
import numpy as np
import pandas as pd
import requests
from typing import Dict, List, Tuple, Any

eel.init('web')

class NNTRSI_P2:
    def __init__(self):
        # Main Settings
        self.len_filter = 20
        self.filter_thresh = 2.0
        self.ema_len1 = 10
        self.ema_len2 = 21
        self.ema_len3 = 50
        self.wickratio_cutoff = 10
        self.wicktobody_cutoff = 10
        self.mult = 8  # TimeFrame Multiplier

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

    def calculate_ema(self, data: np.ndarray, length: int) -> np.ndarray:
        """Calculate Exponential Moving Average"""
        alpha = 2 / (length + 1)
        ema = np.zeros_like(data)
        ema[0] = data[0]
        for i in range(1, len(data)):
            ema[i] = data[i] * alpha + ema[i-1] * (1 - alpha)
        return ema

    def calculate_candle_properties(self, opens: np.ndarray, highs: np.ndarray, 
                                  lows: np.ndarray, closes: np.ndarray) -> Dict[str, np.ndarray]:
        """Calculate basic candle properties"""
        body_len = np.abs(closes - opens)
        candle_range = highs - lows
        range_mid = (highs + lows) / 2
        candle_mid = (closes + opens) / 2
        
        upper_wicks = np.array([h - max(o, c) for h, o, c in zip(highs, opens, closes)])
        lower_wicks = np.array([min(o, c) - l for l, o, c in zip(lows, opens, closes)])
        
        bullish_wick_ratio = lower_wicks / upper_wicks
        bearish_wick_ratio = upper_wicks / lower_wicks
        wick_body_ratio = candle_range / body_len
        
        return {
            'body_len': body_len,
            'candle_range': candle_range,
            'range_mid': range_mid,
            'candle_mid': candle_mid,
            'upper_wicks': upper_wicks,
            'lower_wicks': lower_wicks,
            'bullish_wick_ratio': bullish_wick_ratio,
            'bearish_wick_ratio': bearish_wick_ratio,
            'wick_body_ratio': wick_body_ratio
        }

    def calculate_relative_metrics(self, volumes: np.ndarray, body_len: np.ndarray) -> Dict[str, np.ndarray]:
        """Calculate relative volume and candle size metrics"""
        vol_sma = pd.Series(volumes).rolling(window=self.len_filter).mean().values
        rel_vol = volumes / vol_sma
        
        body_len_sma = pd.Series(body_len).rolling(window=self.len_filter).mean().values
        rel_size = body_len / body_len_sma
        
        return {'rel_vol': rel_vol, 'rel_size': rel_size}

    def identify_swing_points(self, prices: List[float], lookback: int = 5) -> Tuple[List[bool], List[bool]]:
        """Identify swing high and low points"""
        swing_highs = []
        swing_lows = []

        for i in range(len(prices)):
            is_swing_high = all(prices[i] > prices[j] 
                              for j in range(max(0, i-lookback), i)) and \
                           all(prices[i] > prices[j] 
                              for j in range(i+1, min(len(prices), i+lookback+1)))
            swing_highs.append(is_swing_high)

            is_swing_low = all(prices[i] < prices[j] 
                             for j in range(max(0, i-lookback), i)) and \
                          all(prices[i] < prices[j] 
                             for j in range(i+1, min(len(prices), i+lookback+1)))
            swing_lows.append(is_swing_low)
            
        return swing_highs, swing_lows

    def detect_candlestick_patterns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate all candlestick patterns"""
        # Basic candle properties
        df['white_body'] = df['open'] < df['close']
        df['black_body'] = df['open'] > df['close']
        df['body_high'] = df[['open', 'close']].max(axis=1)
        df['body_low'] = df[['open', 'close']].min(axis=1)
        
        # Engulfing patterns
        df['bullish_engulfing'] = (
            (df['body_len'] > df['body_len'].shift(1)) &
            (np.sign(df['close'] - df['open']) != np.sign(df['close'].shift(1) - df['open'].shift(1))) &
            (df['close'] > df['open']) &
            (df['rel_size'] > self.filter_thresh)
        )
        
        df['bearish_engulfing'] = (
            (df['body_len'] > df['body_len'].shift(1)) &
            (np.sign(df['close'] - df['open']) != np.sign(df['close'].shift(1) - df['open'].shift(1))) &
            (df['close'] < df['open']) &
            (df['rel_size'] > self.filter_thresh)
        )
        
        # Doji patterns
        df['grnfly_doji'] = (
            (df['bullish_wick_ratio'] > self.wickratio_cutoff) & 
            (df['wick_body_ratio'] > self.wicktobody_cutoff)
        )
        
        df['grvstne_doji'] = (
            (df['bearish_wick_ratio'] > self.wickratio_cutoff) & 
            (df['wick_body_ratio'] > self.wicktobody_cutoff)
        )
        
        # Harami patterns
        df['bull_harami'] = (
            df['white_body'] & 
            df['black_body'].shift(1) &
            (df['high'] <= df['body_high'].shift(1)) &
            (df['low'] >= df['body_low'].shift(1))
        )
        
        df['bear_harami'] = (
            df['white_body'].shift(1) &
            df['black_body'] &
            (df['high'] <= df['body_high'].shift(1)) &
            (df['low'] >= df['body_low'].shift(1))
        )
        
        # Piercing Line and Dark Cloud Cover
        df['piercing_line'] = (
            (np.sign(df['close'] - df['open']) != np.sign(df['close'].shift(1) - df['open'].shift(1))) &
            (df['close'] > df['open']) &
            (df['close'] > ((df['open'].shift(1) + df['close'].shift(1))/2)) &
            (~df['bullish_engulfing'])
        )
        
        df['dark_cloud_cover'] = (
            (np.sign(df['close'] - df['open']) != np.sign(df['close'].shift(1) - df['open'].shift(1))) &
            (df['close'] < df['open']) &
            (df['close'] < ((df['open'].shift(1) + df['close'].shift(1))/2)) &
            (~df['bearish_engulfing'])
        )
        
        # Morning Star and Evening Star
        df['morning_star'] = (
            (np.sign(df['close'] - df['open']) != np.sign(df['close'].shift(2) - df['open'].shift(2))) &
            (df['close'] > df['open']) &
            (df['body_len'].shift(1) < (df['body_len'].shift(2)/3)) &
            (df['close'] > ((df['open'].shift(2) + df['close'].shift(2))/2))
        )
        
        df['evening_star'] = (
            (np.sign(df['close'] - df['open']) != np.sign(df['close'].shift(2) - df['open'].shift(2))) &
            (df['close'] < df['open']) &
            (df['body_len'].shift(1) < (df['body_len'].shift(2)/3)) &
            (df['close'] < ((df['open'].shift(2) + df['close'].shift(2))/2))
        )
        
        return df

    def calculate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate final trading signals"""
        # Calculate trend signals using the actual EMAs
        df['trend_bullish'] = df['ema2'] > df['ema3']
        df['trend_bearish'] = df['ema2'] < df['ema3']
        
        # Calculate swing levels using actual high/low values
        df['peak'] = (df['high'] > df['high'].shift(1)) & (df['high'] > df['high'].shift(-1))
        df['valley'] = (df['low'] < df['low'].shift(1)) & (df['low'] < df['low'].shift(-1))
        
        # Calculate final signals using pattern recognition
        df['long_signal'] = (
            df['bullish_engulfing'] |
            df['grnfly_doji'] |
            df['bull_harami'] |
            df['piercing_line'] |
            df['morning_star'] |
            df['valley']
        )
        
        df['short_signal'] = (
            df['bearish_engulfing'] |
            df['grvstne_doji'] |
            df['bear_harami'] |
            df['dark_cloud_cover'] |
            df['evening_star'] |
            df['peak']
        )
        
        return df

    def calculate_nnt_rsi_p2(self, data: Dict[str, List[float]]) -> Dict[str, Any]:
        """Main calculation function"""
        # Create DataFrame from the fetched data
        df = pd.DataFrame({
            'open': data['open'],
            'high': data['high'],
            'low': data['low'],
            'close': data['close'],
            'volume': data['volume']
        })
        
        # Convert to numpy arrays for faster computation
        opens = np.array(data['open'])
        highs = np.array(data['high'])
        lows = np.array(data['low'])
        closes = np.array(data['close'])
        volumes = np.array(data['volume'])
        
        # Calculate all properties
        candle_props = self.calculate_candle_properties(opens, highs, lows, closes)
        df = df.assign(**candle_props)
        
        # Calculate relative metrics
        rel_metrics = self.calculate_relative_metrics(volumes, candle_props['body_len'])
        df = df.assign(**rel_metrics)
        
        # Calculate EMAs
        df['ema1'] = self.calculate_ema(closes, self.ema_len1)
        df['ema2'] = self.calculate_ema(closes, self.ema_len2)
        df['ema3'] = self.calculate_ema(closes, self.ema_len3)
        
        # Calculate ATR
        df['atr'] = (highs - lows).rolling(window=14).mean()
        
        # Detect patterns and calculate signals
        df = self.detect_candlestick_patterns(df)
        df = self.calculate_signals(df)
        
        # Calculate additional EMAs for crossover signals
        df['white'] = pd.Series(closes).ewm(span=10, adjust=False).mean()
        df['black'] = pd.Series(closes).ewm(span=20, adjust=False).mean()
        df['long_crossover'] = (df['white'] > df['black']) & (df['white'].shift(1) <= df['black'].shift(1))
        df['short_crossover'] = (df['white'] < df['black']) & (df['white'].shift(1) >= df['black'].shift(1))
        
        # Calculate swing points
        swing_highs, swing_lows = self.identify_swing_points(closes.tolist())
        df['peak'] = swing_highs
        df['valley'] = swing_lows
        
        return {
            'ema1': df['ema1'].tolist(),
            'ema2': df['ema2'].tolist(),
            'ema3': df['ema3'].tolist(),
            'white': df['white'].tolist(),
            'black': df['black'].tolist(),
            'long_signals': df['long_signal'].tolist(),
            'short_signals': df['short_signal'].tolist(),
            'long_crossovers': df['long_crossover'].tolist(),
            'short_crossovers': df['short_crossover'].tolist(),
            'peaks': df['peak'].tolist(),
            'valleys': df['valley'].tolist(),
            'atr': df['atr'].tolist(),
            'rel_vol': df['rel_vol'].tolist(),
            'rel_size': df['rel_size'].tolist(),
            'timestamps': data.get('time', [])  # Include timestamps if available
        }

@eel.expose
async def calculate_indicators(symbol: str, timeframe: str) -> Dict[str, Any]:
    """Main calculation function exposed to JavaScript"""
    nnt_rsi = NNTRSI_P2()
    
    # Fetch candle data
    data = await nnt_rsi.fetch_candle_data(symbol, timeframe)
    if not data['close']:
        return {
            'ema1': [],
            'ema2': [],
            'ema3': [],
            'white': [],
            'black': [],
            'long_signals': [],
            'short_signals': [],
            'long_crossovers': [],
            'short_crossovers': [],
            'peaks': [],
            'valleys': [],
            'atr': [],
            'rel_vol': [],
            'rel_size': []
        }
    
    # Calculate indicators using the fetched data
    result = nnt_rsi.calculate_nnt_rsi_p2(data)
    result['timestamps'] = data['time']  # Add timestamps to the result
    return result

if __name__ == "__main__":
    eel.start('index.html')