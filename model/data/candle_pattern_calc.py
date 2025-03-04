import numpy as np
import pandas as pd
from typing import Dict, Tuple, List

class CandlePatterns:
    @staticmethod
    def bullish_engulfing(data: pd.DataFrame) -> pd.Series:
        pattern = np.zeros(len(data))
        for i in range(1, len(data)):
            if (data['Close'][i] > data['Open'][i] and  # Current candle bullish
                data['Close'][i-1] < data['Open'][i-1] and  # Previous candle bearish
                data['Close'][i] > data['Open'][i-1] and  # Current close > Previous open
                data['Open'][i] < data['Close'][i-1]):  # Current open < Previous close
                pattern[i] = 1
        return pd.Series(pattern, index=data.index)

    @staticmethod
    def bearish_engulfing(data: pd.DataFrame) -> pd.Series:
        pattern = np.zeros(len(data))
        for i in range(1, len(data)):
            if (data['Close'][i] < data['Open'][i] and  # Current candle bearish
                data['Close'][i-1] > data['Open'][i-1] and  # Previous candle bullish
                data['Close'][i] < data['Open'][i-1] and  # Current close < Previous open
                data['Open'][i] > data['Close'][i-1]):  # Current open > Previous close
                pattern[i] = 1
        return pd.Series(pattern, index=data.index)

    @staticmethod
    def hammer(data: pd.DataFrame, shadow_ratio: float=2.0) -> pd.Series:
        pattern = np.zeros(len(data))
        for i in range(len(data)):
            body = abs(data['Close'][i] - data['Open'][i])
            lower_shadow = min(data['Close'][i], data['Open'][i]) - data['Low'][i]
            upper_shadow = data['High'][i] - max(data['Close'][i], data['Open'][i])
            
            if (lower_shadow > body * shadow_ratio and  # Long lower shadow
                upper_shadow < body * 0.1):  # Minimal upper shadow
                pattern[i] = 1
        return pd.Series(pattern, index=data.index)

    @staticmethod
    def shooting_star(data: pd.DataFrame, shadow_ratio: float=2.0) -> pd.Series:
        pattern = np.zeros(len(data))
        for i in range(len(data)):
            body = abs(data['Close'][i] - data['Open'][i])
            upper_shadow = data['High'][i] - max(data['Close'][i], data['Open'][i])
            lower_shadow = min(data['Close'][i], data['Open'][i]) - data['Low'][i]
            
            if (upper_shadow > body * shadow_ratio and  # Long upper shadow
                lower_shadow < body * 0.1):  # Minimal lower shadow
                pattern[i] = 1
        return pd.Series(pattern, index=data.index)

    @staticmethod
    def doji(data: pd.DataFrame, doji_ratio: float=0.1) -> pd.Series:
        pattern = np.zeros(len(data))
        for i in range(len(data)):
            body = abs(data['Close'][i] - data['Open'][i])
            total_length = data['High'][i] - data['Low'][i]
            
            if total_length > 0 and body / total_length < doji_ratio:
                pattern[i] = 1
        return pd.Series(pattern, index=data.index)

    @staticmethod
    def morning_star(data: pd.DataFrame, doji_ratio: float=0.1) -> pd.Series:
        pattern = np.zeros(len(data))
        for i in range(2, len(data)):
            first_body = data['Close'][i-2] - data['Open'][i-2]
            second_body = abs(data['Close'][i-1] - data['Open'][i-1])
            third_body = data['Close'][i] - data['Open'][i]
            
            second_total_length = data['High'][i-1] - data['Low'][i-1]
            
            if (first_body < 0 and  # First bearish
                second_total_length > 0 and second_body / second_total_length < doji_ratio and  # Middle doji
                third_body > 0 and  # Third bullish
                data['Close'][i] > (data['Open'][i-2] + data['Close'][i-2]) / 2):  # Close above first midpoint
                pattern[i] = 1
        return pd.Series(pattern, index=data.index)

    @staticmethod
    def evening_star(data: pd.DataFrame, doji_ratio: float=0.1) -> pd.Series:
        pattern = np.zeros(len(data))
        for i in range(2, len(data)):
            first_body = data['Close'][i-2] - data['Open'][i-2]
            second_body = abs(data['Close'][i-1] - data['Open'][i-1])
            third_body = data['Close'][i] - data['Open'][i]
            
            second_total_length = data['High'][i-1] - data['Low'][i-1]
            
            if (first_body > 0 and  # First bullish
                second_total_length > 0 and second_body / second_total_length < doji_ratio and  # Middle doji
                third_body < 0 and  # Third bearish
                data['Close'][i] < (data['Open'][i-2] + data['Close'][i-2]) / 2):  # Close below first midpoint
                pattern[i] = 1
        return pd.Series(pattern, index=data.index)

    @staticmethod
    def three_white_soldiers(data: pd.DataFrame, tolerance: float=0.1) -> pd.Series:
        pattern = np.zeros(len(data))
        for i in range(2, len(data)):
            if (data['Close'][i] > data['Open'][i] and
                data['Close'][i-1] > data['Open'][i-1] and
                data['Close'][i-2] > data['Open'][i-2] and
                data['Open'][i] > data['Open'][i-1] and
                data['Open'][i-1] > data['Open'][i-2] and
                data['Close'][i] > data['Close'][i-1] and
                data['Close'][i-1] > data['Close'][i-2]):
                pattern[i] = 1
        return pd.Series(pattern, index=data.index)

    @staticmethod
    def three_black_crows(data: pd.DataFrame, tolerance: float=0.1) -> pd.Series:
        pattern = np.zeros(len(data))
        for i in range(2, len(data)):
            if (data['Close'][i] < data['Open'][i] and
                data['Close'][i-1] < data['Open'][i-1] and
                data['Close'][i-2] < data['Open'][i-2] and
                data['Open'][i] < data['Open'][i-1] and
                data['Open'][i-1] < data['Open'][i-2] and
                data['Close'][i] < data['Close'][i-1] and
                data['Close'][i-1] < data['Close'][i-2]):
                pattern[i] = 1
        return pd.Series(pattern, index=data.index)

    @staticmethod
    def harami(data: pd.DataFrame) -> Tuple[pd.Series, pd.Series]:
        bullish = np.zeros(len(data))
        bearish = np.zeros(len(data))
        
        for i in range(1, len(data)):
            prev_body = abs(data['Close'][i-1] - data['Open'][i-1])
            curr_body = abs(data['Close'][i] - data['Open'][i])
            
            if (prev_body > curr_body and
                max(data['Open'][i], data['Close'][i]) < max(data['Open'][i-1], data['Close'][i-1]) and
                min(data['Open'][i], data['Close'][i]) > min(data['Open'][i-1], data['Close'][i-1])):
                
                if data['Close'][i-1] < data['Open'][i-1]:  # Previous bearish
                    bullish[i] = 1
                else:  # Previous bullish
                    bearish[i] = 1
                    
        return pd.Series(bullish, index=data.index), pd.Series(bearish, index=data.index)

    @staticmethod
    def piercing_line(data: pd.DataFrame) -> pd.Series:
        pattern = np.zeros(len(data))
        for i in range(1, len(data)):
            if (data['Close'][i-1] < data['Open'][i-1] and  # Previous bearish
                data['Close'][i] > data['Open'][i] and  # Current bullish
                data['Open'][i] < data['Low'][i-1] and  # Open below previous low
                data['Close'][i] > (data['Open'][i-1] + data['Close'][i-1])/2):  # Close above previous midpoint
                pattern[i] = 1
        return pd.Series(pattern, index=data.index)

    @staticmethod
    def dark_cloud_cover(data: pd.DataFrame) -> pd.Series:
        pattern = np.zeros(len(data))
        for i in range(1, len(data)):
            if (data['Close'][i-1] > data['Open'][i-1] and  # Previous bullish
                data['Close'][i] < data['Open'][i] and  # Current bearish
                data['Open'][i] > data['High'][i-1] and  # Open above previous high
                data['Close'][i] < (data['Open'][i-1] + data['Close'][i-1])/2):  # Close below previous midpoint
                pattern[i] = 1
        return pd.Series(pattern, index=data.index)

    @staticmethod
    def abandoned_baby(data: pd.DataFrame, doji_ratio: float=0.1) -> Tuple[pd.Series, pd.Series]:
        bullish = np.zeros(len(data))
        bearish = np.zeros(len(data))
        
        for i in range(2, len(data)):
            middle_body = abs(data['Close'][i-1] - data['Open'][i-1])
            middle_length = data['High'][i-1] - data['Low'][i-1]
            
            # Check for middle doji
            if middle_length > 0 and middle_body / middle_length < doji_ratio:
                # Bullish pattern
                if (data['Close'][i-2] < data['Open'][i-2] and  # First bearish
                    data['Low'][i-1] > data['High'][i-2] and  # Gap down
                    data['Close'][i] > data['Open'][i] and  # Last bullish
                    data['Low'][i] > data['High'][i-1]):  # Gap up
                    bullish[i] = 1
                
                # Bearish pattern
                if (data['Close'][i-2] > data['Open'][i-2] and  # First bullish
                    data['High'][i-1] < data['Low'][i-2] and  # Gap up
                    data['Close'][i] < data['Open'][i] and  # Last bearish
                    data['High'][i] < data['Low'][i-1]):  # Gap down
                    bearish[i] = 1
                    
        return pd.Series(bullish, index=data.index), pd.Series(bearish, index=data.index)

    def calculate_all_patterns(data: pd.DataFrame) -> Dict[str, pd.Series]:
        """Calculate all candlestick patterns for the given data."""

        patterns = {}

        # Single candlestick patterns
        patterns['hammer'] = CandlePatterns.hammer(data)
        patterns['shooting_star'] = CandlePatterns.shooting_star(data)
        patterns['doji'] = CandlePatterns.doji(data)

        # Double candlestick patterns
        patterns['bullish_engulfing'] = CandlePatterns.bullish_engulfing(data)
        patterns['bearish_engulfing'] = CandlePatterns.bearish_engulfing(data)
        patterns['harami'] = CandlePatterns.harami(data)
        patterns['piercing_line'] = CandlePatterns.piercing_line(data)
        patterns['dark_cloud_cover'] = CandlePatterns.dark_cloud_cover(data)

        # Triple candlestick patterns
        patterns['morning_star'] = CandlePatterns.morning_star(data)
        patterns['evening_star'] = CandlePatterns.evening_star(data)
        patterns['three_white_soldiers'] = CandlePatterns.three_white_soldiers(data)
        patterns['three_black_crows'] = CandlePatterns.three_black_crows(data)
        patterns['abandoned_baby'] = CandlePatterns.abandoned_baby(data)

        return patterns
