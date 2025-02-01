import pandas as pd
import numpy as np
from typing import List, Dict, Union, Optional, Tuple
from datetime import datetime
import plotly.graph_objects as go
from dataclasses import dataclass
from plotly.subplots import make_subplots

@dataclass
class LiquidationLevel:
    timestamp: pd.Timestamp
    price: float
    leverage: str
    color: str
    width: int = 3

@dataclass
class ChartStyle:
    col_up: str = '#22ab94'    # Short liquidations color
    col_dn: str = '#f7525f'    # Long liquidations color
    bar_color: str = '#00ff00' # Bar color
    lines_width: int = 3

class LiquidationsSTC:
    def __init__(self,
                 time_period_mean: int = 40,
                 show_5x: bool = True,
                 show_10x: bool = True,
                 show_25x: bool = True,
                 show_50x: bool = False,
                 show_100x: bool = False,
                 pivot_left: int = 3,
                 pivot_right: int = 3,
                 style: ChartStyle = ChartStyle()):
        """
        Initialize Liquidations Strategy based on Pine Script implementation
        
        Args:
            time_period_mean: Lookback period for volume calculations
            show_5x: Show 5x leverage liquidation levels
            show_10x: Show 10x leverage liquidation levels
            show_25x: Show 25x leverage liquidation levels
            show_50x: Show 50x leverage liquidation levels
            show_100x: Show 100x leverage liquidation levels
            pivot_left: Left bars for pivot calculation
            pivot_right: Right bars for pivot calculation
            style: Chart styling options
        """
        self.time_period_mean = time_period_mean
        self.show_5x = show_5x
        self.show_10x = show_10x
        self.show_25x = show_25x
        self.show_50x = show_50x
        self.show_100x = show_100x
        self.pivot_left = pivot_left
        self.pivot_right = pivot_right
        self.style = style
        
        # Maximum number of liquidation lines to show (from Pine Script)
        self.max_lines = 500

    def calculate_pivots(self, df: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
        """
        Calculate pivot points for high and low
        Equivalent to Pine Script's pivothigh and pivotlow functions
        """
        highs = df['high'].values
        lows = df['low'].values
        pivot_highs = np.full_like(highs, np.nan)
        pivot_lows = np.full_like(lows, np.nan)
        
        for i in range(self.pivot_left, len(df) - self.pivot_right):
            # Check for pivot high
            if all(highs[i] > highs[i-self.pivot_left:i]) and \
               all(highs[i] > highs[i+1:i+self.pivot_right+1]):
                pivot_highs[i] = highs[i]
            
            # Check for pivot low
            if all(lows[i] < lows[i-self.pivot_left:i]) and \
               all(lows[i] < lows[i+1:i+self.pivot_right+1]):
                pivot_lows[i] = lows[i]
        
        return pivot_highs, pivot_lows

    def calculate_liquidation_levels(self, volume: np.array, time_period_mean: int) -> Tuple[pd.Series, pd.Series, pd.Series, pd.Series, pd.Series]:
        """
        Calculate liquidation levels based on volume
        Equivalent to Pine Script's liqudation() function
        """
        highest = pd.Series(volume).rolling(window=time_period_mean).max()
        lowest = pd.Series(volume).rolling(window=time_period_mean).min()
        avg = (highest + lowest) / 2
        avg_mean = avg.rolling(window=time_period_mean+10).mean()
        
        _100x = avg >= 1.2 * avg_mean
        _50x = avg >= 1.1 * avg_mean
        _25x = avg >= 1.05 * avg_mean
        _10x = avg >= 1.025 * avg_mean
        _5x = avg > avg_mean
        
        return _100x, _50x, _25x, _10x, _5x

    def calculate_liquidation_price(self, price: float, leverage: int) -> float:
        """
        Calculate liquidation price based on leverage
        """
        percent_risk = {
            5: 0.20,   # 20%
            10: 0.10,  # 10%
            25: 0.04,  # 4%
            50: 0.02,  # 2%
            100: 0.01  # 1%
        }
        return price / (1 + percent_risk[leverage])

    def identify_patterns(self, df: pd.DataFrame) -> Dict[str, List[pd.Timestamp]]:
        """
        Identify candlestick patterns such as doji and engulfing patterns
        """
        patterns = {
            'doji': [],
            'bullish_engulfing': [],
            'bearish_engulfing': []
        }

        for i in range(1, len(df)):
            # Calculate body and shadows
            open_price, close_price = df['open'].iloc[i], df['close'].iloc[i]
            high_price, low_price = df['high'].iloc[i], df['low'].iloc[i]
            prev_open, prev_close = df['open'].iloc[i-1], df['close'].iloc[i-1]

            body = abs(close_price - open_price)
            upper_shadow = high_price - max(open_price, close_price)
            lower_shadow = min(open_price, close_price) - low_price

            # Doji: Small body, long shadows
            if body < 0.1 * (high_price - low_price):
                patterns['doji'].append(df.index[i])

            # Bullish Engulfing
            if prev_close < prev_open and close_price > open_price and close_price > prev_open and open_price < prev_close:
                patterns['bullish_engulfing'].append(df.index[i])

            # Bearish Engulfing
            if prev_close > prev_open and close_price < open_price and close_price < prev_open and open_price > prev_close:
                patterns['bearish_engulfing'].append(df.index[i])

        return patterns

    def analyze(self, df: pd.DataFrame, start_date: str = "2023-01-01") -> Dict:
        """
        Analyze the price data and return liquidation levels and patterns
        """
        # Convert start_date to timestamp for filtering
        start_timestamp = pd.Timestamp(start_date)
        df = df[df.index >= start_timestamp].copy()
        
        # Calculate pivot points
        pivot_highs, pivot_lows = self.calculate_pivots(df)
        
        # Calculate liquidation levels based on volume
        _100x, _50x, _25x, _10x, _5x = self.calculate_liquidation_levels(
            df['volume'].values, 
            self.time_period_mean
        )
        
        liquidation_levels = []
        
        # Process each bar
        for i in range(self.pivot_right, len(df)):
            if pd.notna(pivot_lows[i]):
                price = df['low'].iloc[i]
                timestamp = df.index[i]
                
                # Calculate liquidation levels for each enabled leverage
                levels = []
                if self.show_5x and _5x[i]:
                    levels.append(LiquidationLevel(timestamp, self.calculate_liquidation_price(price, 5), '5x', self.style.col_dn))
                if self.show_10x and _10x[i]:
                    levels.append(LiquidationLevel(timestamp, self.calculate_liquidation_price(price, 10), '10x', self.style.col_dn))
                if self.show_25x and _25x[i]:
                    levels.append(LiquidationLevel(timestamp, self.calculate_liquidation_price(price, 25), '25x', self.style.col_dn))
                if self.show_50x and _50x[i]:
                    levels.append(LiquidationLevel(timestamp, self.calculate_liquidation_price(price, 50), '50x', self.style.col_dn))
                if self.show_100x and _100x[i]:
                    levels.append(LiquidationLevel(timestamp, self.calculate_liquidation_price(price, 100), '100x', self.style.col_dn))
                
                if levels:
                    liquidation_levels.extend(levels)
                    # Keep only the last max_lines levels
                    if len(liquidation_levels) > self.max_lines:
                        liquidation_levels = liquidation_levels[-self.max_lines:]
        
        patterns = self.identify_patterns(df)
        
        return {
            'liquidation_levels': liquidation_levels,
            'pivot_highs': pivot_highs,
            'pivot_lows': pivot_lows,
            'volume_signals': {
                '100x': _100x,
                '50x': _50x,
                '25x': _25x,
                '10x': _10x,
                '5x': _5x
            },
            'patterns': patterns
        }

    def plot_chart(self, df: pd.DataFrame, results: Dict) -> go.Figure:
        """
        Create an interactive chart with all indicators and liquidation levels
        Matches Pine Script's visual output
        """
        # Create figure with secondary y-axis for volume
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                           vertical_spacing=0.03, 
                           row_heights=[0.7, 0.3])

        # Add candlestick chart
        fig.add_trace(
            go.Candlestick(
                x=df.index,
                open=df['open'],
                high=df['high'],
                low=df['low'],
                close=df['close'],
                increasing_line_color=self.style.col_up,
                decreasing_line_color=self.style.col_dn,
                name='Price'
            ),
            row=1, col=1
        )

        # Add volume bars
        colors = [self.style.col_up if close >= open else self.style.col_dn 
                 for close, open in zip(df['close'], df['open'])]
        
        fig.add_trace(
            go.Bar(
                x=df.index,
                y=df['volume'],
                marker_color=colors,
                name='Volume'
            ),
            row=2, col=1
        )

        # Add liquidation levels
        for level in results['liquidation_levels']:
            fig.add_shape(
                type="line",
                x0=level.timestamp,
                x1=df.index[-1],
                y0=level.price,
                y1=level.price,
                line=dict(
                    color=level.color,
                    width=level.width,
                ),
                row=1, col=1
            )
            
            # Add annotations for leverage levels
            fig.add_annotation(
                x=level.timestamp,
                y=level.price,
                text=f"{level.leverage}",
                showarrow=True,
                arrowhead=1,
                row=1, col=1
            )

        # Update layout
        fig.update_layout(
            title='Price Chart with Liquidation Levels',
            xaxis_title='Date',
            yaxis_title='Price',
            template='plotly_dark',
            showlegend=True,
            xaxis_rangeslider_visible=False
        )

        return fig

    def get_active_liquidation_levels(self, df: pd.DataFrame, current_time: pd.Timestamp) -> List[Dict]:
        """
        Get currently active liquidation levels
        
        Args:
            df: DataFrame with OHLCV data
            current_time: Current timestamp
            
        Returns:
            List of active liquidation levels
        """
        results = self.analyze(df)
        active_levels = []
        
        for level in results['liquidation_levels']:
            if level.timestamp <= current_time:
                # Check if price hasn't crossed the liquidation level
                price_slice = df[df.index > level.timestamp]['high']
                if not (price_slice > level.price).any():
                    active_levels.append({
                        'leverage': level.leverage,
                        'price': level.price,
                        'timestamp': level.timestamp
                    })
        
        return active_levels

    def create_html_chart(self, df: pd.DataFrame, filename: str = 'liquidation_chart.html'):
        """
        Create and save an interactive HTML chart
        """
        results = self.analyze(df)
        fig = self.plot_chart(df, results)
        fig.write_html(filename)

# Example usage:
if __name__ == "__main__":
    # Sample data loading
    import yfinance as yf
    
    # Initialize strategy
    strategy = LiquidationsSTC()
    
    # Fetch sample data
    symbol = "BTC-USD"
    df = yf.download(symbol, start="2023-01-01")
    
    # Analyze and create chart
    results = strategy.analyze(df)
    strategy.create_html_chart(df, f"{symbol}_liquidations.html")
