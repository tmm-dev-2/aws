import talib
import numpy as np
from typing import Dict, List, Union, Optional, Tuple
import pandas as pd

class PatternsEngine:
    def __init__(self):
        self.patterns = {}
        
    # Candlestick Patterns
    def cdl_2crows(self, open: np.ndarray, high: np.ndarray, low: np.ndarray, close: np.ndarray) -> np.ndarray:
        return talib.CDL2CROWS(open, high, low, close)
    
    def cdl_thrusting(self, open, high, low, close):
        """
        Thrusting pattern: Bearish pattern where second candle opens lower but pushes up into first candle's body
        """
        pattern = np.zeros(len(close))
        for i in range(1, len(close)):
            if (close[i-1] < open[i-1] and  # First candle is bearish
                open[i] < close[i-1] and     # Second opens below first close
                close[i] > open[i] and       # Second is bullish
                close[i] < (open[i-1] + close[i-1])/2):  # Second closes in first body
                pattern[i] = -100
        return pattern

    def cdl_tristar(self, open, high, low, close):
        """
        Tri-Star pattern: Three consecutive doji candles forming reversal pattern
        """
        pattern = np.zeros(len(close))
        for i in range(2, len(close)):
            if (self.is_doji(open[i-2], high[i-2], low[i-2], close[i-2]) and
                self.is_doji(open[i-1], high[i-1], low[i-1], close[i-1]) and
                self.is_doji(open[i], high[i], low[i], close[i])):
                if open[i-1] > open[i-2]:  # Bullish pattern
                    pattern[i] = 100
                else:  # Bearish pattern
                    pattern[i] = -100
        return pattern

    def cdl_unique_three_river(self, open, high, low, close):
        """
        Unique Three River Bottom pattern: Bullish reversal pattern
        """
        pattern = np.zeros(len(close))
        for i in range(2, len(close)):
            if (close[i-2] < open[i-2] and  # First candle bearish
                close[i-1] < open[i-1] and   # Second candle bearish
                low[i-1] < low[i-2] and      # Second low below first
                close[i] > open[i] and       # Third candle bullish
                open[i] < close[i-1]):       # Third opens below second close
                pattern[i] = 100
        return pattern

    def cdl_upside_gap_two_crows(self, open, high, low, close):
        """
        Upside Gap Two Crows pattern: Bearish reversal pattern
        """
        pattern = np.zeros(len(close))
        for i in range(2, len(close)):
            if (close[i-2] > open[i-2] and    # First candle bullish
                open[i-1] > high[i-2] and      # Gap up
                close[i-1] < open[i-1] and     # Second candle bearish
                open[i] > close[i-1] and       # Third opens above second
                close[i] < open[i] and         # Third candle bearish
                close[i] > open[i-1]):         # Third closes above second open
                pattern[i] = -100
        return pattern

    def cdl_xside_gap_three_methods(self, open, high, low, close):
        """
        Upside/Downside Gap Three Methods pattern
        """
        pattern = np.zeros(len(close))
        for i in range(2, len(close)):
            # Bullish pattern
            if (close[i-2] > open[i-2] and     # First candle bullish
                open[i-1] > high[i-2] and       # Gap up
                close[i-1] > open[i-1] and      # Second candle bullish
                open[i] < close[i-1] and        # Third fills gap
                close[i] > open[i]):            # Third candle bullish
                pattern[i] = 100
            # Bearish pattern
            elif (close[i-2] < open[i-2] and    # First candle bearish
                  open[i-1] < low[i-2] and      # Gap down
                  close[i-1] < open[i-1] and    # Second candle bearish
                  open[i] > close[i-1] and      # Third fills gap
                  close[i] < open[i]):          # Third candle bearish
                pattern[i] = -100
        return pattern
    def cdl_3blackcrows(self, open: np.ndarray, high: np.ndarray, low: np.ndarray, close: np.ndarray) -> np.ndarray:
        return talib.CDL3BLACKCROWS(open, high, low, close)
        
    def cdl_3inside(self, open: np.ndarray, high: np.ndarray, low: np.ndarray, close: np.ndarray) -> np.ndarray:
        return talib.CDL3INSIDE(open, high, low, close)
        
    def cdl_3linestrike(self, open: np.ndarray, high: np.ndarray, low: np.ndarray, close: np.ndarray) -> np.ndarray:
        return talib.CDL3LINESTRIKE(open, high, low, close)
        
    def cdl_3outside(self, open: np.ndarray, high: np.ndarray, low: np.ndarray, close: np.ndarray) -> np.ndarray:
        return talib.CDL3OUTSIDE(open, high, low, close)
        
    def cdl_3starsinsouth(self, open: np.ndarray, high: np.ndarray, low: np.ndarray, close: np.ndarray) -> np.ndarray:
        return talib.CDL3STARSINSOUTH(open, high, low, close)
        
    def cdl_3whitesoldiers(self, open: np.ndarray, high: np.ndarray, low: np.ndarray, close: np.ndarray) -> np.ndarray:
        return talib.CDL3WHITESOLDIERS(open, high, low, close)
        
    def cdl_abandonedbaby(self, open: np.ndarray, high: np.ndarray, low: np.ndarray, close: np.ndarray, penetration: float = 0.3) -> np.ndarray:
        return talib.CDLABANDONEDBABY(open, high, low, close, penetration)
        
    def cdl_advanceblock(self, open: np.ndarray, high: np.ndarray, low: np.ndarray, close: np.ndarray) -> np.ndarray:
        return talib.CDLADVANCEBLOCK(open, high, low, close)
        
    def cdl_belthold(self, open: np.ndarray, high: np.ndarray, low: np.ndarray, close: np.ndarray) -> np.ndarray:
        return talib.CDLBELTHOLD(open, high, low, close)
        
    def cdl_breakaway(self, open: np.ndarray, high: np.ndarray, low: np.ndarray, close: np.ndarray) -> np.ndarray:
        return talib.CDLBREAKAWAY(open, high, low, close)
        
    def cdl_closingmarubozu(self, open: np.ndarray, high: np.ndarray, low: np.ndarray, close: np.ndarray) -> np.ndarray:
        return talib.CDLCLOSINGMARUBOZU(open, high, low, close)
        
    def cdl_concealbabyswall(self, open: np.ndarray, high: np.ndarray, low: np.ndarray, close: np.ndarray) -> np.ndarray:
        return talib.CDLCONCEALBABYSWALL(open, high, low, close)
        
    def cdl_counterattack(self, open: np.ndarray, high: np.ndarray, low: np.ndarray, close: np.ndarray) -> np.ndarray:
        return talib.CDLCOUNTERATTACK(open, high, low, close)
        
    def cdl_darkcloudcover(self, open: np.ndarray, high: np.ndarray, low: np.ndarray, close: np.ndarray, penetration: float = 0.5) -> np.ndarray:
        return talib.CDLDARKCLOUDCOVER(open, high, low, close, penetration)
        
    def cdl_doji(self, open: np.ndarray, high: np.ndarray, low: np.ndarray, close: np.ndarray) -> np.ndarray:
        return talib.CDLDOJI(open, high, low, close)
        
    def cdl_dojistar(self, open: np.ndarray, high: np.ndarray, low: np.ndarray, close: np.ndarray) -> np.ndarray:
        return talib.CDLDOJISTAR(open, high, low, close)
        
    def cdl_dragonflydoji(self, open: np.ndarray, high: np.ndarray, low: np.ndarray, close: np.ndarray) -> np.ndarray:
        return talib.CDLDRAGONFLYDOJI(open, high, low, close)
        
    def cdl_engulfing(self, open: np.ndarray, high: np.ndarray, low: np.ndarray, close: np.ndarray) -> np.ndarray:
        return talib.CDLENGULFING(open, high, low, close)
        
    def cdl_eveningdojistar(self, open: np.ndarray, high: np.ndarray, low: np.ndarray, close: np.ndarray, penetration: float = 0.3) -> np.ndarray:
        return talib.CDLEVENINGDOJISTAR(open, high, low, close, penetration)
        
    def cdl_eveningstar(self, open: np.ndarray, high: np.ndarray, low: np.ndarray, close: np.ndarray, penetration: float = 0.3) -> np.ndarray:
        return talib.CDLEVENINGSTAR(open, high, low, close, penetration)
        
    def cdl_gapsidesidewhite(self, open: np.ndarray, high: np.ndarray, low: np.ndarray, close: np.ndarray) -> np.ndarray:
        return talib.CDLGAPSIDESIDEWHITE(open, high, low, close)
        
    def cdl_gravestonedoji(self, open: np.ndarray, high: np.ndarray, low: np.ndarray, close: np.ndarray) -> np.ndarray:
        return talib.CDLGRAVESTONEDOJI(open, high, low, close)
        
    def cdl_hammer(self, open: np.ndarray, high: np.ndarray, low: np.ndarray, close: np.ndarray) -> np.ndarray:
        return talib.CDLHAMMER(open, high, low, close)
        
    def cdl_hangingman(self, open: np.ndarray, high: np.ndarray, low: np.ndarray, close: np.ndarray) -> np.ndarray:
        return talib.CDLHANGINGMAN(open, high, low, close)
        
    def cdl_harami(self, open: np.ndarray, high: np.ndarray, low: np.ndarray, close: np.ndarray) -> np.ndarray:
        return talib.CDLHARAMI(open, high, low, close)
        
    def cdl_haramicross(self, open: np.ndarray, high: np.ndarray, low: np.ndarray, close: np.ndarray) -> np.ndarray:
        return talib.CDLHARAMICROSS(open, high, low, close)
        
    def cdl_highwave(self, open: np.ndarray, high: np.ndarray, low: np.ndarray, close: np.ndarray) -> np.ndarray:
        return talib.CDLHIGHWAVE(open, high, low, close)
        
    def cdl_hikkake(self, open: np.ndarray, high: np.ndarray, low: np.ndarray, close: np.ndarray) -> np.ndarray:
        return talib.CDLHIKKAKE(open, high, low, close)
        
    def cdl_hikkakemod(self, open: np.ndarray, high: np.ndarray, low: np.ndarray, close: np.ndarray) -> np.ndarray:
        return talib.CDLHIKKAKEMOD(open, high, low, close)
        
    def cdl_homingpigeon(self, open: np.ndarray, high: np.ndarray, low: np.ndarray, close: np.ndarray) -> np.ndarray:
        return talib.CDLHOMINGPIGEON(open, high, low, close)
        
    def cdl_identical3crows(self, open: np.ndarray, high: np.ndarray, low: np.ndarray, close: np.ndarray) -> np.ndarray:
        return talib.CDLIDENTICAL3CROWS(open, high, low, close)
        
    def cdl_inneck(self, open: np.ndarray, high: np.ndarray, low: np.ndarray, close: np.ndarray) -> np.ndarray:
        return talib.CDLINNECK(open, high, low, close)
        
    def cdl_invertedhammer(self, open: np.ndarray, high: np.ndarray, low: np.ndarray, close: np.ndarray) -> np.ndarray:
        return talib.CDLINVERTEDHAMMER(open, high, low, close)
        
    def cdl_kicking(self, open: np.ndarray, high: np.ndarray, low: np.ndarray, close: np.ndarray) -> np.ndarray:
        return talib.CDLKICKING(open, high, low, close)
        
    def cdl_kickingbylength(self, open: np.ndarray, high: np.ndarray, low: np.ndarray, close: np.ndarray) -> np.ndarray:
        return talib.CDLKICKINGBYLENGTH(open, high, low, close)
        
    def cdl_ladderbottom(self, open: np.ndarray, high: np.ndarray, low: np.ndarray, close: np.ndarray) -> np.ndarray:
        return talib.CDLLADDERBOTTOM(open, high, low, close)
        
    def cdl_longleggeddoji(self, open: np.ndarray, high: np.ndarray, low: np.ndarray, close: np.ndarray) -> np.ndarray:
        return talib.CDLLONGLEGGEDDOJI(open, high, low, close)
        
    def cdl_longline(self, open: np.ndarray, high: np.ndarray, low: np.ndarray, close: np.ndarray) -> np.ndarray:
        return talib.CDLLONGLINE(open, high, low, close)
        
    def cdl_marubozu(self, open: np.ndarray, high: np.ndarray, low: np.ndarray, close: np.ndarray) -> np.ndarray:
        return talib.CDLMARUBOZU(open, high, low, close)
        
    def cdl_matchinglow(self, open: np.ndarray, high: np.ndarray, low: np.ndarray, close: np.ndarray) -> np.ndarray:
        return talib.CDLMATCHINGLOW(open, high, low, close)
        
    def cdl_mathold(self, open: np.ndarray, high: np.ndarray, low: np.ndarray, close: np.ndarray, penetration: float = 0.5) -> np.ndarray:
        return talib.CDLMATHOLD(open, high, low, close, penetration)
        
    def cdl_morningdojistar(self, open: np.ndarray, high: np.ndarray, low: np.ndarray, close: np.ndarray, penetration: float = 0.3) -> np.ndarray:
        return talib.CDLMORNINGDOJISTAR(open, high, low, close, penetration)
        
    def cdl_morningstar(self, open: np.ndarray, high: np.ndarray, low: np.ndarray, close: np.ndarray, penetration: float = 0.3) -> np.ndarray:
        return talib.CDLMORNINGSTAR(open, high, low, close, penetration)
        
    def cdl_onneck(self, open: np.ndarray, high: np.ndarray, low: np.ndarray, close: np.ndarray) -> np.ndarray:
        return talib.CDLONNECK(open, high, low, close)
        
    def cdl_piercing(self, open: np.ndarray, high: np.ndarray, low: np.ndarray, close: np.ndarray) -> np.ndarray:
        return talib.CDLPIERCING(open, high, low, close)
        
    def cdl_rickshawman(self, open: np.ndarray, high: np.ndarray, low: np.ndarray, close: np.ndarray) -> np.ndarray:
        return talib.CDLRICKSHAWMAN(open, high, low, close)
        
    def cdl_risefall3methods(self, open: np.ndarray, high: np.ndarray, low: np.ndarray, close: np.ndarray) -> np.ndarray:
        return talib.CDLRISEFALL3METHODS(open, high, low, close)
        
    def cdl_separatinglines(self, open: np.ndarray, high: np.ndarray, low: np.ndarray, close: np.ndarray) -> np.ndarray:
        return talib.CDLSEPARATINGLINES(open, high, low, close)
        
    def cdl_shootingstar(self, open: np.ndarray, high: np.ndarray, low: np.ndarray, close: np.ndarray) -> np.ndarray:
        return talib.CDLSHOOTINGSTAR(open, high, low, close)
        
    def cdl_shortline(self, open: np.ndarray, high: np.ndarray, low: np.ndarray, close: np.ndarray) -> np.ndarray:
        return talib.CDLSHORTLINE(open, high, low, close)
        
    def cdl_spinningtop(self, open: np.ndarray, high: np.ndarray, low: np.ndarray, close: np.ndarray) -> np.ndarray:
        return talib.CDLSPINNINGTOP(open, high, low, close)
        
    def cdl_stalledpattern(self, open: np.ndarray, high: np.ndarray, low: np.ndarray, close: np.ndarray) -> np.ndarray:
        return talib.CDLSTALLEDPATTERN(open, high, low, close)
        
    def cdl_sticksandwich(self, open: np.ndarray, high: np.ndarray, low: np.ndarray, close: np.ndarray) -> np.ndarray:
        return talib.CDLSTICKSANDWICH(open, high, low, close)
        
    def cdl_takuri(self, open: np.ndarray, high: np.ndarray, low: np.ndarray, close: np.ndarray) -> np.ndarray:
        return talib.CDLTAKURI(open, high, low, close)

    def cdl_tasukigap(self, open: np.ndarray, high: np.ndarray, low: np.ndarray, close: np.ndarray) -> np.ndarray:
        return talib.CDLTASUKIGAP(open, high, low, close)

    # Chart Formations
    def identify_head_shoulders(self, high: np.ndarray, low: np.ndarray, threshold: float = 0.02) -> Dict[str, Union[bool, float]]:
        # Head and shoulders pattern detection
        peaks = self._find_peaks(high)
        troughs = self._find_peaks(-low)
        
        if len(peaks) >= 3 and len(troughs) >= 2:
            left_shoulder = peaks[0]
            head = peaks[1]
            right_shoulder = peaks[2]
            
            neckline = np.mean([troughs[0], troughs[1]])
            
            if (abs(left_shoulder - right_shoulder) < threshold * head and
                head > left_shoulder and head > right_shoulder):
                return {
                    'pattern': True,
                    'head_level': head,
                    'neckline': neckline,
                    'target': neckline - (head - neckline)
                }
        
        return {'pattern': False}
    def identify_5o(self, data):
        """
        Identifies 5-0 harmonic pattern
        Pattern ratios: XA=1.13, AB=1.618, BC=0.5, CD=1.618, DE=0.5
        """
        pattern = {}
        swings = self.find_swings(data)

        for i in range(len(swings)-4):
            points = swings[i:i+5]
            ratios = self.calculate_ratios(points)

            if (self.is_valid_ratio(ratios['XA'], 1.13, 0.02) and
                self.is_valid_ratio(ratios['AB'], 1.618, 0.02) and
                self.is_valid_ratio(ratios['BC'], 0.5, 0.02) and
                self.is_valid_ratio(ratios['CD'], 1.618, 0.02) and
                self.is_valid_ratio(ratios['DE'], 0.5, 0.02)):
                pattern['points'] = points
                pattern['type'] = 'bullish' if points[0]['price'] < points[-1]['price'] else 'bearish'

        return pattern

    def identify_wolfe_waves(self, data):
        """
        Identifies Wolfe Wave patterns
        Rules: 1-2-3-4-5 wave pattern with specific angle relationships
        """
        pattern = {}
        swings = self.find_swings(data)
        
        for i in range(len(swings)-4):
            points = swings[i:i+5]
            
            # Calculate angles between waves
            angles = self.calculate_wave_angles(points)
            
            # Wolfe Wave rules:
            # 1. Waves 1-2 and 3-4 should be parallel
            # 2. Wave 5 should reach the 1-4 trendline
            # 3. Time between points 3-4 equals time between 4-5
            if (self.are_waves_parallel(angles['1-2'], angles['3-4']) and
                self.point_reaches_trendline(points[4], points[0], points[3]) and
                self.equal_time_waves(points[2:5])):
                pattern['points'] = points
                pattern['type'] = 'bullish' if points[3]['price'] < points[4]['price'] else 'bearish'
            
        return pattern
    def identify_double_top(self, high: np.ndarray, threshold: float = 0.02) -> Dict[str, Union[bool, float]]:
        peaks = self._find_peaks(high)
        
        if len(peaks) >= 2:
            first_top = peaks[0]
            second_top = peaks[1]
            
            if abs(first_top - second_top) < threshold * first_top:
                return {
                    'pattern': True,
                    'resistance': max(first_top, second_top),
                    'target': min(high) + (max(first_top, second_top) - min(high))
                }
                
        return {'pattern': False}

    def identify_double_bottom(self, low: np.ndarray, threshold: float = 0.02) -> Dict[str, Union[bool, float]]:
        troughs = self._find_peaks(-low)
        
        if len(troughs) >= 2:
            first_bottom = troughs[0]
            second_bottom = troughs[1]
            
            if abs(first_bottom - second_bottom) < threshold * first_bottom:
                return {
                    'pattern': True,
                    'support': min(first_bottom, second_bottom),
                    'target': max(low) - (max(low) - min(first_bottom, second_bottom))
                }
                
        return {'pattern': False}

    def identify_triangle(self, high: np.ndarray, low: np.ndarray) -> Dict[str, Union[bool, str, float]]:
        highs = self._linear_regression(high)
        lows = self._linear_regression(low)
        
        high_slope = highs['slope']
        low_slope = lows['slope']
        
        if abs(high_slope) < 0.1 and abs(low_slope) < 0.1:
            return {'pattern': True, 'type': 'rectangle'}
        elif high_slope < -0.1 and low_slope > 0.1:
            return {'pattern': True, 'type': 'converging'}
        elif high_slope > 0.1 and low_slope < -0.1:
            return {'pattern': True, 'type': 'diverging'}
        elif high_slope < -0.1 and low_slope < -0.1:
            return {'pattern': True, 'type': 'descending'}
        elif high_slope > 0.1 and low_slope > 0.1:
            return {'pattern': True, 'type': 'ascending'}
            
        return {'pattern': False}

    # Harmonic Patterns
    def identify_gartley(self, high: np.ndarray, low: np.ndarray) -> Dict[str, Union[bool, float]]:
        swings = self._find_swings(high, low)
        
        if len(swings) >= 5:
            xab = self._measure_move(swings[0], swings[1], swings[2])
            abc = self._measure_move(swings[1], swings[2], swings[3])
            bcd = self._measure_move(swings[2], swings[3], swings[4])
            
            if (0.618 <= xab <= 0.618 and
                0.382 <= abc <= 0.886 and
                1.272 <= bcd <= 1.618):
                return {
                    'pattern': True,
                    'target': swings[4],
                    'stop': swings[0]
                }
                
        return {'pattern': False}

    def identify_butterfly(self, high: np.ndarray, low: np.ndarray) -> Dict[str, Union[bool, float]]:
        swings = self._find_swings(high, low)
        
        if len(swings) >= 5:
            xab = self._measure_move(swings[0], swings[1], swings[2])
            abc = self._measure_move(swings[1], swings[2], swings[3])
            bcd = self._measure_move(swings[2], swings[3], swings[4])
            
            if (0.786 <= xab <= 0.786 and
                0.382 <= abc <= 0.886 and
                1.618 <= bcd <= 2.618):
                return {
                    'pattern': True,
                    'target': swings[4],
                    'stop': swings[0]
                }
                
        return {'pattern': False}

    def identify_bat(self, high: np.ndarray, low: np.ndarray) -> Dict[str, Union[bool, float]]:
        swings = self._find_swings(high, low)
        
        if len(swings) >= 5:
            xab = self._measure_move(swings[0], swings[1], swings[2])
            abc = self._measure_move(swings[1], swings[2], swings[3])
            bcd = self._measure_move(swings[2], swings[3], swings[4])
            
            if (0.382 <= xab <= 0.5 and
                0.382 <= abc <= 0.886 and
                1.618 <= bcd <= 2.618):
                return {
                    'pattern': True,
                    'target': swings[4],
                    'stop': swings[0]
                }
                
        return {'pattern': False}

    def identify_crab(self, high: np.ndarray, low: np.ndarray) -> Dict[str, Union[bool, float]]:
        swings = self._find_swings(high, low)
        
        if len(swings) >= 5:
            xab = self._measure_move(swings[0], swings[1], swings[2])
            abc = self._measure_move(swings[1], swings[2], swings[3])
            bcd = self._measure_move(swings[2], swings[3], swings[4])
            
            if (0.382 <= xab <= 0.618 and
                0.382 <= abc <= 0.886 and
                2.618 <= bcd <= 3.618):
                return {
                    'pattern': True, 
                    'target': swings[4],
                    'stop': swings[0]
                }
                
        return {'pattern': False}

    # Helper Methods
    def _find_peaks(self, data: np.ndarray, order: int = 5) -> np.ndarray:
        peaks = []
        for i in range(order, len(data)-order):
            if all(data[i] > data[i-order:i]) and all(data[i] > data[i+1:i+order+1]):
                peaks.append(data[i])
        return np.array(peaks)

    def _find_swings(self, high: np.ndarray, low: np.ndarray) -> np.ndarray:
        peaks = self._find_peaks(high)
        troughs = self._find_peaks(-low)
        swings = np.sort(np.concatenate([peaks, troughs]))
        return swings

    def _measure_move(self, point1: float, point2: float, point3: float) -> float:
        return abs(point3 - point2) / abs(point2 - point1)

    def _linear_regression(self, data: np.ndarray) -> Dict[str, float]:
        x = np.arange(len(data))
        slope, intercept = np.polyfit(x, data, 1)
        return {'slope': slope, 'intercept': intercept}

    # Elliott Wave Functions
    def identify_impulse_wave(self, high: np.ndarray, low: np.ndarray) -> Dict[str, Union[bool, List[float]]]:
        swings = self._find_swings(high, low)
        
        if len(swings) >= 5:
            wave1 = swings[1] - swings[0]
            wave2 = swings[2] - swings[1]
            wave3 = swings[3] - swings[2]
            wave4 = swings[4] - swings[3]
            wave5 = swings[5] - swings[4]
            
            if (wave2 < wave1 and
                wave3 > wave1 and
                wave4 < wave3 and
                wave5 < wave3):
                return {
                    'pattern': True,
                    'waves': [wave1, wave2, wave3, wave4, wave5]
                }
                
        return {'pattern': False}

    def identify_corrective_wave(self, high: np.ndarray, low: np.ndarray) -> Dict[str, Union[bool, List[float]]]:
        swings = self._find_swings(high, low)
        
        if len(swings) >= 3:
            waveA = swings[1] - swings[0]
            waveB = swings[2] - swings[1]
            waveC = swings[3] - swings[2]
            
            if (waveB < waveA and waveC > waveB):
                return {
                    'pattern': True,
                    'waves': [waveA, waveB, waveC]
                }
                
        return {'pattern': False}
class ElliottWaveEngine:
    def __init__(self):
        self.wave_data = {}

    def determine_wave_degree(self, data: np.ndarray) -> Dict[str, float]:
        wave_length = len(data)
        if wave_length > 200:
            return {'degree': 'Grand Supercycle'}
        elif wave_length > 100:
            return {'degree': 'Supercycle'}
        elif wave_length > 50:
            return {'degree': 'Cycle'}
        else:
            return {'degree': 'Primary'}

    def determine_wave_position(self, data: np.ndarray) -> Dict[str, int]:
        peaks = self._find_peaks(data)
        troughs = self._find_troughs(data)
        wave_points = sorted(peaks + troughs, key=lambda x: x[0])
        return {'position': len(wave_points)}

    def count_waves(self, data: np.ndarray) -> Dict[str, int]:
        peaks = self._find_peaks(data)
        troughs = self._find_troughs(data)
        return {'count': len(peaks) + len(troughs)}

    def identify_wave_pattern(self, data: np.ndarray) -> Dict[str, str]:
        if self._is_impulse_wave(data):
            return {'pattern': 'Impulse'}
        elif self._is_corrective_wave(data):
            return {'pattern': 'Corrective'}
        else:
            return {'pattern': 'Unknown'}

    def validate_wave_structure(self, data: np.ndarray) -> Dict[str, bool]:
        return {
            'valid': self._check_wave_rules(data),
            'alternation': self._check_alternation(data),
            'proportion': self._check_proportion(data)
        }

    def project_next_wave(self, data: np.ndarray) -> Dict[str, float]:
        wave_pattern = self.identify_wave_pattern(data)
        if wave_pattern['pattern'] == 'Impulse':
            return self._project_impulse_wave(data)
        else:
            return self._project_corrective_wave(data)

    def calculate_retracement_levels(self, data: np.ndarray) -> Dict[str, float]:
        return {
            '0.236': self._calculate_retracement(data, 0.236),
            '0.382': self._calculate_retracement(data, 0.382),
            '0.500': self._calculate_retracement(data, 0.500),
            '0.618': self._calculate_retracement(data, 0.618),
            '0.786': self._calculate_retracement(data, 0.786)
        }

    def calculate_extension_levels(self, data: np.ndarray) -> Dict[str, float]:
        return {
            '1.618': self._calculate_extension(data, 1.618),
            '2.618': self._calculate_extension(data, 2.618),
            '4.236': self._calculate_extension(data, 4.236)
        }

class HarmonicEngine:
    def __init__(self):
        self.patterns = {}

    def identify_gartley(self, data: np.ndarray) -> Dict[str, Union[bool, float]]:
        xab = self._measure_move(data, 0, 1, 2)
        abc = self._measure_move(data, 1, 2, 3)
        bcd = self._measure_move(data, 2, 3, 4)
        
        if (0.618 <= xab <= 0.618 and
            0.382 <= abc <= 0.886 and
            1.272 <= bcd <= 1.618):
            return {'pattern': True, 'completion_point': data[4]}
        return {'pattern': False}

    def identify_butterfly(self, data: np.ndarray) -> Dict[str, Union[bool, float]]:
        xab = self._measure_move(data, 0, 1, 2)
        abc = self._measure_move(data, 1, 2, 3)
        bcd = self._measure_move(data, 2, 3, 4)
        
        if (0.786 <= xab <= 0.786 and
            0.382 <= abc <= 0.886 and
            1.618 <= bcd <= 2.618):
            return {'pattern': True, 'completion_point': data[4]}
        return {'pattern': False}
    def identify_5o(self, data):
        """
        Identifies 5-0 harmonic pattern
        Pattern ratios: XA=1.13, AB=1.618, BC=0.5, CD=1.618, DE=0.5
        """
        pattern = {}
        swings = self.find_swings(data)
        
        for i in range(len(swings)-4):
            points = swings[i:i+5]
            ratios = self.calculate_ratios(points)
            
            if (self.is_valid_ratio(ratios['XA'], 1.13, 0.02) and
                self.is_valid_ratio(ratios['AB'], 1.618, 0.02) and
                self.is_valid_ratio(ratios['BC'], 0.5, 0.02) and
                self.is_valid_ratio(ratios['CD'], 1.618, 0.02) and
                self.is_valid_ratio(ratios['DE'], 0.5, 0.02)):
                pattern['points'] = points
                pattern['type'] = 'bullish' if points[0]['price'] < points[-1]['price'] else 'bearish'
                
        return pattern
    
    def identify_wolfe_waves(self, data):
        """
        Identifies Wolfe Wave patterns
        Rules: 1-2-3-4-5 wave pattern with specific angle relationships
        """
        pattern = {}
        swings = self.find_swings(data)
        
        for i in range(len(swings)-4):
            points = swings[i:i+5]
            
            # Calculate angles between waves
            angles = self.calculate_wave_angles(points)
            
            # Wolfe Wave rules:
            # 1. Waves 1-2 and 3-4 should be parallel
            # 2. Wave 5 should reach the 1-4 trendline
            # 3. Time between points 3-4 equals time between 4-5
            if (self.are_waves_parallel(angles['1-2'], angles['3-4']) and
                self.point_reaches_trendline(points[4], points[0], points[3]) and
                self.equal_time_waves(points[2:5])):
                pattern['points'] = points
                pattern['type'] = 'bullish' if points[3]['price'] < points[4]['price'] else 'bearish'
                
        return pattern
    def identify_bat(self, data: np.ndarray) -> Dict[str, Union[bool, float]]:
        xab = self._measure_move(data, 0, 1, 2)
        abc = self._measure_move(data, 1, 2, 3)
        bcd = self._measure_move(data, 2, 3, 4)
        
        if (0.382 <= xab <= 0.5 and
            0.382 <= abc <= 0.886 and
            1.618 <= bcd <= 2.618):
            return {'pattern': True, 'completion_point': data[4]}
        return {'pattern': False}

    def identify_crab(self, data: np.ndarray) -> Dict[str, Union[bool, float]]:
        xab = self._measure_move(data, 0, 1, 2)
        abc = self._measure_move(data, 1, 2, 3)
        bcd = self._measure_move(data, 2, 3, 4)
        
        if (0.382 <= xab <= 0.618 and
            0.382 <= abc <= 0.886 and
            2.618 <= bcd <= 3.618):
            return {'pattern': True, 'completion_point': data[4]}
        return {'pattern': False}

    def identify_shark(self, data: np.ndarray) -> Dict[str, Union[bool, float]]:
        xab = self._measure_move(data, 0, 1, 2)
        abc = self._measure_move(data, 1, 2, 3)
        bcd = self._measure_move(data, 2, 3, 4)
        
        if (0.446 <= xab <= 0.618 and
            1.13 <= abc <= 1.618 and
            1.618 <= bcd <= 2.236):
            return {'pattern': True, 'completion_point': data[4]}
        return {'pattern': False}

    def identify_cypher(self, data: np.ndarray) -> Dict[str, Union[bool, float]]:
        xab = self._measure_move(data, 0, 1, 2)
        abc = self._measure_move(data, 1, 2, 3)
        bcd = self._measure_move(data, 2, 3, 4)
        
        if (0.382 <= xab <= 0.618 and
            1.13 <= abc <= 1.414 and
            1.272 <= bcd <= 2.000):
            return {'pattern': True, 'completion_point': data[4]}
        return {'pattern': False}

class FibonacciEngine:
    def __init__(self):
        self.fib_ratios = [0, 0.236, 0.382, 0.500, 0.618, 0.786, 1.0, 1.618, 2.618, 4.236]

    def calculate_retracement_levels(self, high: float, low: float) -> Dict[str, float]:
        diff = high - low
        return {
            str(ratio): high - (diff * ratio) 
            for ratio in self.fib_ratios
        }

    def calculate_extension_levels(self, high: float, low: float) -> Dict[str, float]:
        diff = high - low
        return {
            str(ratio): high + (diff * ratio)
            for ratio in [1.618, 2.618, 4.236]
        }

    def calculate_projection_levels(self, swing1: float, swing2: float) -> Dict[str, float]:
        diff = abs(swing2 - swing1)
        direction = 1 if swing2 > swing1 else -1
        return {
            str(ratio): swing2 + (diff * ratio * direction)
            for ratio in [0.618, 1.0, 1.618]
        }

    def generate_fibonacci_circles(self, center: Tuple[float, float], radius: float) -> Dict[str, List[Tuple[float, float]]]:
        circles = {}
        for ratio in self.fib_ratios:
            r = radius * ratio
            circles[str(ratio)] = self._generate_circle_points(center, r)
        return circles

    def generate_fibonacci_spirals(self, center: Tuple[float, float], start_radius: float) -> Dict[str, List[Tuple[float, float]]]:
        spirals = {}
        for ratio in self.fib_ratios[1:]:
            spirals[str(ratio)] = self._generate_spiral_points(center, start_radius, ratio)
        return spirals

    def calculate_time_zones(self, start_time: float) -> Dict[str, float]:
        fib_sequence = [1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
        return {
            str(i): start_time + (i * 86400)  # Converting days to seconds
            for i in fib_sequence
        }

    def generate_channels(self, data: np.ndarray) -> Dict[str, List[float]]:
        trend_line = self._calculate_trend_line(data)
        channels = {}
        for ratio in [0.618, 1.0, 1.618]:
            channels[str(ratio)] = self._parallel_channel(trend_line, ratio)
        return channels

    def calculate_expansion_levels(self, data: np.ndarray) -> Dict[str, float]:
        range_size = np.max(data) - np.min(data)
        return {
            str(ratio): np.max(data) + (range_size * ratio)
            for ratio in [0.618, 1.0, 1.618, 2.618]
        }


class PatternSyntax:
    def __init__(self):
        self.pattern_engine = PatternsEngine()
        self.elliott_engine = ElliottWaveEngine()
        self.harmonic_engine = HarmonicEngine()
        self.fibonacci_engine = FibonacciEngine()

        self.syntax_mappings = {
            # Single Candle Patterns
            'CDL_DOJI': lambda open, high, low, close: self.pattern_engine.cdl_doji(open, high, low, close),
            'CDL_DOJI_STAR': lambda open, high, low, close: self.pattern_engine.cdl_dojistar(open, high, low, close),
            'CDL_DRAGONFLY_DOJI': lambda open, high, low, close: self.pattern_engine.cdl_dragonflydoji(open, high, low, close),
            'CDL_GRAVESTONE_DOJI': lambda open, high, low, close: self.pattern_engine.cdl_gravestonedoji(open, high, low, close),
            'CDL_HAMMER': lambda open, high, low, close: self.pattern_engine.cdl_hammer(open, high, low, close),
            'CDL_HANGING_MAN': lambda open, high, low, close: self.pattern_engine.cdl_hangingman(open, high, low, close),
            'CDL_INVERTED_HAMMER': lambda open, high, low, close: self.pattern_engine.cdl_invertedhammer(open, high, low, close),
            'CDL_SHOOTING_STAR': lambda open, high, low, close: self.pattern_engine.cdl_shootingstar(open, high, low, close),
            'CDL_SPINNING_TOP': lambda open, high, low, close: self.pattern_engine.cdl_spinningtop(open, high, low, close),
            'CDL_MARUBOZU': lambda open, high, low, close: self.pattern_engine.cdl_marubozu(open, high, low, close),
            'CDL_LONG_LINE': lambda open, high, low, close: self.pattern_engine.cdl_longline(open, high, low, close),
            'CDL_SHORT_LINE': lambda open, high, low, close: self.pattern_engine.cdl_shortline(open, high, low, close),

            # Double Candle Patterns
            'CDL_ENGULFING': lambda open, high, low, close: self.pattern_engine.cdl_engulfing(open, high, low, close),
            'CDL_HARAMI': lambda open, high, low, close: self.pattern_engine.cdl_harami(open, high, low, close),
            'CDL_HARAMI_CROSS': lambda open, high, low, close: self.pattern_engine.cdl_haramicross(open, high, low, close),
            'CDL_PIERCING': lambda open, high, low, close: self.pattern_engine.cdl_piercing(open, high, low, close),
            'CDL_DARK_CLOUD_COVER': lambda open, high, low, close: self.pattern_engine.cdl_darkcloudcover(open, high, low, close),
            'CDL_KICKING': lambda open, high, low, close: self.pattern_engine.cdl_kicking(open, high, low, close),
            'CDL_MEETING_LINES': lambda open, high, low, close: self.pattern_engine.cdl_meetinglines(open, high, low, close),
            'CDL_MATCHING_LOW': lambda open, high, low, close: self.pattern_engine.cdl_matchinglow(open, high, low, close),
            'CDL_COUNTERATTACK': lambda open, high, low, close: self.pattern_engine.cdl_counterattack(open, high, low, close),
            'CDL_SEPARATING_LINES': lambda open, high, low, close: self.pattern_engine.cdl_separatinglines(open, high, low, close),

            # Triple Candle Patterns
            'CDL_MORNING_STAR': lambda open, high, low, close: self.pattern_engine.cdl_morningstar(open, high, low, close),
            'CDL_EVENING_STAR': lambda open, high, low, close: self.pattern_engine.cdl_eveningstar(open, high, low, close),
            'CDL_MORNING_DOJI_STAR': lambda open, high, low, close: self.pattern_engine.cdl_morningdojistar(open, high, low, close),
            'CDL_EVENING_DOJI_STAR': lambda open, high, low, close: self.pattern_engine.cdl_eveningdojistar(open, high, low, close),
            'CDL_THREE_WHITE_SOLDIERS': lambda open, high, low, close: self.pattern_engine.cdl_3whitesoldiers(open, high, low, close),
            'CDL_THREE_BLACK_CROWS': lambda open, high, low, close: self.pattern_engine.cdl_3blackcrows(open, high, low, close),
            'CDL_THREE_INSIDE': lambda open, high, low, close: self.pattern_engine.cdl_3inside(open, high, low, close),
            'CDL_THREE_OUTSIDE': lambda open, high, low, close: self.pattern_engine.cdl_3outside(open, high, low, close),
            'CDL_THREE_LINE_STRIKE': lambda open, high, low, close: self.pattern_engine.cdl_3linestrike(open, high, low, close),
            'CDL_THREE_STARS_IN_SOUTH': lambda open, high, low, close: self.pattern_engine.cdl_3starsinsouth(open, high, low, close),

            # Multi Candle Patterns
            'CDL_ABANDONED_BABY': lambda open, high, low, close: self.pattern_engine.cdl_abandonedbaby(open, high, low, close),
            'CDL_ADVANCE_BLOCK': lambda open, high, low, close: self.pattern_engine.cdl_advanceblock(open, high, low, close),
            'CDL_BELT_HOLD': lambda open, high, low, close: self.pattern_engine.cdl_belthold(open, high, low, close),
            'CDL_BREAKAWAY': lambda open, high, low, close: self.pattern_engine.cdl_breakaway(open, high, low, close),
            'CDL_CONCEALING_BABY_SWALLOW': lambda open, high, low, close: self.pattern_engine.cdl_concealbabyswall(open, high, low, close),
            'CDL_HIKKAKE': lambda open, high, low, close: self.pattern_engine.cdl_hikkake(open, high, low, close),
            'CDL_HIKKAKE_MOD': lambda open, high, low, close: self.pattern_engine.cdl_hikkakemod(open, high, low, close),
            'CDL_IDENTICAL_THREE_CROWS': lambda open, high, low, close: self.pattern_engine.cdl_identical3crows(open, high, low, close),
            'CDL_IN_NECK': lambda open, high, low, close: self.pattern_engine.cdl_inneck(open, high, low, close),
            'CDL_LADDER_BOTTOM': lambda open, high, low, close: self.pattern_engine.cdl_ladderbottom(open, high, low, close),
            'CDL_MAT_HOLD': lambda open, high, low, close: self.pattern_engine.cdl_mathold(open, high, low, close),
            'CDL_ON_NECK': lambda open, high, low, close: self.pattern_engine.cdl_onneck(open, high, low, close),
            'CDL_RICKSHAW_MAN': lambda open, high, low, close: self.pattern_engine.cdl_rickshawman(open, high, low, close),
            'CDL_RISE_FALL_THREE_METHODS': lambda open, high, low, close: self.pattern_engine.cdl_risefall3methods(open, high, low, close),
            'CDL_STICK_SANDWICH': lambda open, high, low, close: self.pattern_engine.cdl_sticksandwich(open, high, low, close),
            'CDL_TAKURI': lambda open, high, low, close: self.pattern_engine.cdl_takuri(open, high, low, close),
            'CDL_TASUKI_GAP': lambda open, high, low, close: self.pattern_engine.cdl_tasukigap(open, high, low, close),
            'CDL_THRUSTING': lambda open, high, low, close: self.pattern_engine.cdl_thrusting(open, high, low, close),
            'CDL_TRISTAR': lambda open, high, low, close: self.pattern_engine.cdl_tristar(open, high, low, close),
            'CDL_UNIQUE_THREE_RIVER': lambda open, high, low, close: self.pattern_engine.cdl_unique_three_river(open, high, low, close),
            'CDL_UPSIDE_GAP_TWO_CROWS': lambda open, high, low, close: self.pattern_engine.cdl_upside_gap_two_crows(open, high, low, close),
            'CDL_XSIDE_GAP_THREE_METHODS': lambda open, high, low, close: self.pattern_engine.cdl_xside_gap_three_methods(open, high, low, close),

            # Elliott Wave Mappings
            'wave_degree': lambda data: self.elliott_engine.determine_wave_degree(data),
            'wave_position': lambda data: self.elliott_engine.determine_wave_position(data),
            'wave_count': lambda data: self.elliott_engine.count_waves(data),
            'wave_pattern': lambda data: self.elliott_engine.identify_wave_pattern(data),
            'wave_validation': lambda data: self.elliott_engine.validate_wave_structure(data),
            'wave_projection': lambda data: self.elliott_engine.project_next_wave(data),
            'wave_retracement': lambda data: self.elliott_engine.calculate_retracement_levels(data),
            'wave_extension': lambda data: self.elliott_engine.calculate_extension_levels(data),

            # Harmonic Pattern Mappings
            'pattern_gartley': lambda data: self.harmonic_engine.identify_gartley(data),
            'pattern_butterfly': lambda data: self.harmonic_engine.identify_butterfly(data),
            'pattern_bat': lambda data: self.harmonic_engine.identify_bat(data),
            'pattern_crab': lambda data: self.harmonic_engine.identify_crab(data),
            'pattern_shark': lambda data: self.harmonic_engine.identify_shark(data),
            'pattern_cypher': lambda data: self.harmonic_engine.identify_cypher(data),
            'pattern_5o': lambda data: self.harmonic_engine.identify_5o(data),
            'pattern_wolfe_waves': lambda data: self.harmonic_engine.identify_wolfe_waves(data),

            # Fibonacci Analysis Mappings
            'fib_retracement': lambda high, low: self.fibonacci_engine.calculate_retracement_levels(high, low),
            'fib_extension': lambda high, low: self.fibonacci_engine.calculate_extension_levels(high, low),
            'fib_projection': lambda swing1, swing2: self.fibonacci_engine.calculate_projection_levels(swing1, swing2),
            'fib_circles': lambda center, radius: self.fibonacci_engine.generate_fibonacci_circles(center, radius),
            'fib_spirals': lambda center, start: self.fibonacci_engine.generate_fibonacci_spirals(center, start),
            'fib_timezones': lambda start_time: self.fibonacci_engine.calculate_time_zones(start_time),
            'fib_channels': lambda data: self.fibonacci_engine.generate_channels(data),
            'fib_expansion': lambda data: self.fibonacci_engine.calculate_expansion_levels(data)
        }
