import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Union, Optional
from dataclasses import dataclass
from scipy.stats import linregress
import talib

@dataclass
class Point:
    x: float
    y: float

class DrawingTools:
    @staticmethod
    def line(start: Point, end: Point) -> np.ndarray:
        x = np.array([start.x, end.x])
        y = np.array([start.y, end.y])
        return np.column_stack((x, y))

    @staticmethod
    def horizontal_line(y_level: float, x_range: Tuple[float, float]) -> np.ndarray:
        x = np.array(x_range)
        y = np.full_like(x, y_level)
        return np.column_stack((x, y))

    @staticmethod
    def vertical_line(x_level: float, y_range: Tuple[float, float]) -> np.ndarray:
        y = np.array(y_range)
        x = np.full_like(y, x_level)
        return np.column_stack((x, y))

    @staticmethod
    def ray(start: Point, angle: float, length: float) -> np.ndarray:
        end_x = start.x + length * np.cos(np.radians(angle))
        end_y = start.y + length * np.sin(np.radians(angle))
        return DrawingTools.line(start, Point(end_x, end_y))

    @staticmethod
    def circle(center: Point, radius: float, points: int=100) -> np.ndarray:
        theta = np.linspace(0, 2*np.pi, points)
        x = center.x + radius * np.cos(theta)
        y = center.y + radius * np.sin(theta)
        return np.column_stack((x, y))

    @staticmethod
    def rectangle(top_left: Point, bottom_right: Point) -> np.ndarray:
        x = [top_left.x, bottom_right.x, bottom_right.x, top_left.x, top_left.x]
        y = [top_left.y, top_left.y, bottom_right.y, bottom_right.y, top_left.y]
        return np.column_stack((x, y))

    @staticmethod
    def triangle(p1: Point, p2: Point, p3: Point) -> np.ndarray:
        x = [p1.x, p2.x, p3.x, p1.x]
        y = [p1.y, p2.y, p3.y, p1.y]
        return np.column_stack((x, y))

class FibonacciTools:
    FIBONACCI_LEVELS = [0, 0.236, 0.382, 0.5, 0.618, 0.786, 1, 1.618, 2.618, 4.236]
    
    @staticmethod
    def retracements(high: Point, low: Point) -> Dict[float, np.ndarray]:
        retracements = {}
        price_range = high.y - low.y
        
        for level in FibonacciTools.FIBONACCI_LEVELS:
            y_level = high.y - (price_range * level)
            retracements[level] = DrawingTools.horizontal_line(
                y_level, 
                (min(high.x, low.x), max(high.x, low.x))
            )
        return retracements

    @staticmethod
    def extensions(start: Point, end: Point, pullback: Point) -> Dict[float, np.ndarray]:
        extensions = {}
        price_range = end.y - start.y
        
        for level in FibonacciTools.FIBONACCI_LEVELS:
            y_level = pullback.y + (price_range * level)
            extensions[level] = DrawingTools.horizontal_line(
                y_level,
                (pullback.x, pullback.x + (end.x - start.x))
            )
        return extensions

    @staticmethod
    def time_zones(start_x: float, period: float, num_zones: int) -> List[np.ndarray]:
        zones = []
        for i in range(1, num_zones + 1):
            x = start_x + period * FibonacciTools.FIBONACCI_LEVELS[i]
            zones.append(x)
        return zones

class GannTools:
    GANN_ANGLES = {
        '1x8': 82.5,
        '1x4': 75,
        '1x3': 71.25,
        '1x2': 63.75,
        '1x1': 45,
        '2x1': 26.25,
        '3x1': 18.75,
        '4x1': 15,
        '8x1': 7.5
    }

    @staticmethod
    def fan(start: Point, length: float) -> Dict[str, np.ndarray]:
        fan_lines = {}
        for name, angle in GannTools.GANN_ANGLES.items():
            fan_lines[name] = DrawingTools.ray(start, angle, length)
        return fan_lines

    @staticmethod
    def square(center: Point, size: float) -> Dict[str, np.ndarray]:
        lines = {}
        for i in range(-4, 5):
            lines[f'h_{i}'] = DrawingTools.horizontal_line(
                center.y + (i * size),
                (center.x - 4*size, center.x + 4*size)
            )
            lines[f'v_{i}'] = DrawingTools.vertical_line(
                center.x + (i * size),
                (center.y - 4*size, center.y + 4*size)
            )
        return lines

class ChartPatterns:
    @staticmethod
    def head_and_shoulders(data: pd.DataFrame, window: int=20) -> Dict[str, np.ndarray]:
        pattern = {}
        peaks = []
        
        for i in range(window, len(data)-window):
            if data['High'][i] == data['High'][i-window:i+window].max():
                peaks.append(Point(i, data['High'][i]))
                
        for i in range(len(peaks)-2):
            left_shoulder = peaks[i]
            head = peaks[i+1]
            right_shoulder = peaks[i+2]
            
            if (head.y > left_shoulder.y and 
                head.y > right_shoulder.y and 
                abs(left_shoulder.y - right_shoulder.y) / head.y < 0.1):
                
                neckline_start = Point(
                    left_shoulder.x,
                    data['Low'][int(left_shoulder.x):int(head.x)].min()
                )
                neckline_end = Point(
                    right_shoulder.x,
                    data['Low'][int(head.x):int(right_shoulder.x)].min()
                )
                
                pattern['neckline'] = DrawingTools.line(neckline_start, neckline_end)
                pattern['left_shoulder'] = left_shoulder
                pattern['head'] = head
                pattern['right_shoulder'] = right_shoulder
                
        return pattern

    @staticmethod
    def double_top_bottom(data: pd.DataFrame, window: int=20) -> Dict[str, Dict[str, Point]]:
        patterns = {'tops': {}, 'bottoms': {}}
        
        for i in range(window, len(data)-window):
            # Double Tops
            if data['High'][i] == data['High'][i-window:i+window].max():
                for j in range(i+window, len(data)-window):
                    if (abs(data['High'][j] - data['High'][i]) / data['High'][i] < 0.02 and
                        data['High'][j] == data['High'][j-window:j+window].max()):
                        patterns['tops'][f'top_{i}_{j}'] = {
                            'first': Point(i, data['High'][i]),
                            'second': Point(j, data['High'][j])
                        }
            
            # Double Bottoms
            if data['Low'][i] == data['Low'][i-window:i+window].min():
                for j in range(i+window, len(data)-window):
                    if (abs(data['Low'][j] - data['Low'][i]) / data['Low'][i] < 0.02 and
                        data['Low'][j] == data['Low'][j-window:j+window].min()):
                        patterns['bottoms'][f'bottom_{i}_{j}'] = {
                            'first': Point(i, data['Low'][i]),
                            'second': Point(j, data['Low'][j])
                        }
        
        return patterns

class VolumeProfile:
    @staticmethod
    def calculate(data: pd.DataFrame, price_levels: int=12) -> np.ndarray:
        price_range = data['High'].max() - data['Low'].min()
        level_height = price_range / price_levels
        
        profile = np.zeros((price_levels, 2))
        for i in range(price_levels):
            price_level = data['Low'].min() + (i * level_height)
            volume = data[
                (data['Low'] <= price_level) & 
                (data['High'] > price_level)
            ]['Volume'].sum()
            
            profile[i] = [price_level, volume]
            
        return profile

    @staticmethod
    def time_distribution(data: pd.DataFrame, time_periods: int=24) -> np.ndarray:
        period_length = len(data) // time_periods
        distribution = np.zeros((time_periods, 2))
        
        for i in range(time_periods):
            start_idx = i * period_length
            end_idx = start_idx + period_length
            period_data = data.iloc[start_idx:end_idx]
            
            distribution[i] = [
                period_data.index[0],
                period_data['Volume'].sum()
            ]
            
        return distribution

class DrawingManager:
    def __init__(self):
        self.drawings: Dict[str, Union[np.ndarray, Dict]] = {}
        
    def add(self, name: str, drawing: Union[np.ndarray, Dict]):
        self.drawings[name] = drawing
        
    def remove(self, name: str):
        if name in self.drawings:
            del self.drawings[name]
            
    def clear(self):
        self.drawings.clear()
        
    def get(self, name: str) -> Optional[Union[np.ndarray, Dict]]:
        return self.drawings.get(name)
        
    def get_all(self) -> Dict[str, Union[np.ndarray, Dict]]:
        return self.drawings

def calculate_all_drawings(data: pd.DataFrame) -> Dict[str, Union[np.ndarray, Dict]]:
    """Calculate all chart patterns and drawings for the given data."""
    
    drawings = {}
    
    # Chart Patterns
    drawings['head_and_shoulders'] = ChartPatterns.head_and_shoulders(data)
    drawings['double_patterns'] = ChartPatterns.double_top_bottom(data)
    
    # Fibonacci Analysis
    high_point = Point(data['High'].idxmax(), data['High'].max())
    low_point = Point(data['Low'].idxmin(), data['Low'].min())
    drawings['fibonacci_retracements'] = FibonacciTools.retracements(high_point, low_point)
    
    # Gann Analysis
    center_point = Point(len(data)//2, data['Close'].mean())
    drawings['gann_fan'] = GannTools.fan(center_point, len(data)//4)
    drawings['gann_square'] = GannTools.square(center_point, data['Close'].std())
    
    # Volume Analysis
    drawings['volume_profile'] = VolumeProfile.calculate(data)
    drawings['volume_time_distribution'] = VolumeProfile.time_distribution(data)
    
    return drawings
