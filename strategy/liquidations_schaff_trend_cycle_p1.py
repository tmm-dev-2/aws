import numpy as np
import pandas as pd
import ta

class LiquidationStrategy:
    def __init__(self):
        # User inputs (matching PineScript inputs)
        self.time_period_mean = 40
        self.show_5x = True
        self.show_10x = True
        self.show_25x = True
        self.show_50x = False
        self.show_100x = False
        self.lines_width = 3
        self.col_up = '#22ab94'  # Short liquidations color
        self.col_dn = '#f7525f'  # Long liquidations color
        self.bar_color = '#00FF00'  # Lime color
        
        # Volatility Bands parameters
        self.mult = 2.0
        self.reduction_factor = 6.0
        self.malen = 93  # Trend Period
        self.malen1 = 50  # Fast Length
        self.green_color = '#00ffbb'
        self.red_color = '#ff1100'

    def hull_ma(self, data, length):
        """Calculate Hull Moving Average"""
        half_length = length // 2
        sqrt_length = int(np.sqrt(length))
        
        # WMA of half length
        wmaf = data.rolling(window=half_length).mean()
        # WMA of full length
        wmas = data.rolling(window=length).mean()
        
        # HMA calculation
        return (2 * wmaf - wmas).rolling(window=sqrt_length).mean()

    def calculate_liquidation(self, df, time_period_mean):
        """Calculate liquidation levels based on volume"""
        volume = df['Volume']
        highest = volume.rolling(window=time_period_mean).max()
        lowest = volume.rolling(window=time_period_mean).min()
        avg = (highest + lowest) / 2
        avg_mean = avg.rolling(window=time_period_mean + 10).mean()

        _100x = avg >= 1.2 * avg_mean
        _50x = avg >= 1.1 * avg_mean
        _25x = avg >= 1.05 * avg_mean
        _10x = avg >= 1.025 * avg_mean
        _5x = avg > avg_mean

        return _100x, _50x, _25x, _10x, _5x

    def calculate_pivot_points(self, df, pivot_left=3, pivot_right=3):
        """Calculate pivot high and low points"""
        high = df['High']
        low = df['Low']
        
        pivot_highs = pd.Series(index=df.index, dtype=float)
        pivot_lows = pd.Series(index=df.index, dtype=float)

        for i in range(pivot_left, len(df) - pivot_right):
            # Pivot High
            if all(high.iloc[i] > high.iloc[i-pivot_left:i]) and \
               all(high.iloc[i] > high.iloc[i+1:i+pivot_right+1]):
                pivot_highs.iloc[i] = high.iloc[i]

            # Pivot Low
            if all(low.iloc[i] < low.iloc[i-pivot_left:i]) and \
               all(low.iloc[i] < low.iloc[i+1:i+pivot_right+1]):
                pivot_lows.iloc[i] = low.iloc[i]

        return pivot_highs, pivot_lows

    def calculate_liquidation_levels(self, df, leverage, pivot_high, pivot_low):
        """Calculate liquidation levels for different leverages"""
        percent_risk = {
            5: 0.20,   # 20%
            10: 0.10,  # 10%
            25: 0.04,  # 4%
            50: 0.02,  # 2%
            100: 0.01  # 1%
        }[leverage]

        long_liq = pd.Series(index=df.index)
        short_liq = pd.Series(index=df.index)

        # Calculate liquidation levels
        long_liq[~pivot_low.isna()] = pivot_low[~pivot_low.isna()] / (1 + percent_risk)
        short_liq[~pivot_high.isna()] = pivot_high[~pivot_high.isna()] * (1 + percent_risk)

        return long_liq, short_liq

    def calculate_volatility_bands(self, df):
        """Calculate all volatility bands and indicators"""
        # Basic calculations
        df['hl2'] = (df['High'] + df['Low']) / 2
        df['v1'] = self.hull_ma(df['hl2'], self.malen)
        df['v2'] = self.hull_ma(df['Close'], self.malen1)

        # Main bands
        df['dev'] = self.mult * df['hl2'].rolling(window=self.malen).std()
        df['upper'] = df['v1'] + df['dev']
        df['lower'] = df['v1'] - df['dev']

        # Upper bands
        df['dev1'] = (self.mult/self.reduction_factor) * df['upper'].rolling(window=self.malen).std()
        df['upperu'] = df['upper'] + df['dev1']
        df['loweru'] = df['upper'] - df['dev1']

        # Lower bands
        df['dev2'] = (self.mult/self.reduction_factor) * df['lower'].rolling(window=self.malen).std()
        df['upperl'] = df['lower'] + df['dev2']
        df['lowerl'] = df['lower'] - df['dev2']

        # Trend conditions
        df['uptrend'] = df['v1'] > df['v1'].shift(1)
        df['downtrend'] = df['v1'] < df['v1'].shift(1)
        df['neutral'] = ((df['uptrend'] & (df['v2'] < df['v1'])) | 
                        (df['downtrend'] & (df['v2'] > df['v1'])))

        # Signal conditions
        df['bullish_continuation'] = (df['uptrend'] & 
                                    df['Close'].shift(1).lt(df['v2'].shift(1)) & 
                                    df['Close'].gt(df['v2']))
        df['bearish_continuation'] = (df['downtrend'] & 
                                    df['Close'].shift(1).gt(df['v2'].shift(1)) & 
                                    df['Close'].lt(df['v2']))

        # Trend signals
        df['bullish_trend'] = df['v1'].gt(df['v1'].shift(1))
        df['bearish_trend'] = df['v1'].lt(df['v1'].shift(1))

        return df

    def apply_strategy(self, df):
        """Main strategy application"""
        # Ensure datetime index
        if not isinstance(df.index, pd.DatetimeIndex):
            df.index = pd.to_datetime(df.index)

        # Calculate volume-based liquidations
        _100x, _50x, _25x, _10x, _5x = self.calculate_liquidation(df, self.time_period_mean)

        # Calculate pivot points
        pivot_highs, pivot_lows = self.calculate_pivot_points(df)

        # Calculate volatility bands and indicators
        df = self.calculate_volatility_bands(df)

        # Calculate liquidation levels for each leverage
        leverages = [(5, self.show_5x), (10, self.show_10x), 
                    (25, self.show_25x), (50, self.show_50x), 
                    (100, self.show_100x)]

        for leverage, show in leverages:
            if show:
                long_liq, short_liq = self.calculate_liquidation_levels(
                    df, leverage, pivot_highs, pivot_lows)
                df[f'long_liq_{leverage}x'] = long_liq
                df[f'short_liq_{leverage}x'] = short_liq

        return df

    def process_data(self, df: pd.DataFrame) -> dict:
        """
        Process data and return all visual elements
        """
        # Calculate all indicators
        df = self.calculate_volatility_bands(df)
        
        # Format the response with all visual elements
        response = {
            'candles': [],
            'bands': {
                'upper': [],
                'lower': [],
                'upperBand1': [],
                'upperBand2': [],
                'lowerBand1': [],
                'lowerBand2': [],
            },
            'backgrounds': [],
            'signals': [],
            'liquidationLevels': []
        }

        for index, row in df.iterrows():
            timestamp = int(index.timestamp())
            
            # Format candle data
            response['candles'].append({
                'time': timestamp,
                'open': row['open'],
                'high': row['high'],
                'low': row['low'],
                'close': row['close'],
                'volume': row['volume']
            })
            
            # Format bands data
            for band in ['upper', 'lower', 'upperu', 'loweru', 'upperl', 'lowerl']:
                if not np.isnan(row[band]):
                    response['bands'][band].append({
                        'time': timestamp,
                        'value': row[band]
                    })
            
            # Add background colors for trends
            if row['uptrend']:
                response['backgrounds'].append({
                    'time': timestamp,
                    'color': 'rgba(0, 255, 187, 0.1)'  # Light green
                })
            elif row['downtrend']:
                response['backgrounds'].append({
                    'time': timestamp,
                    'color': 'rgba(255, 17, 0, 0.1)'  # Light red
                })
            
            # Add signals
            if row['bullish_continuation']:
                response['signals'].append({
                    'time': timestamp,
                    'position': 'belowbar',
                    'color': '#00ffbb',
                    'shape': 'arrowUp',
                    'text': 'BUY'
                })
            elif row['bearish_continuation']:
                response['signals'].append({
                    'time': timestamp,
                    'position': 'abovebar',
                    'color': '#ff1100',
                    'shape': 'arrowDown',
                    'text': 'SELL'
                })

        return response
