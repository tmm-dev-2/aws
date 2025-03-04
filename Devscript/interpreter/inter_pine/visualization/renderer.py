from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass
from enum import Enum
import numpy as np

class ChartStyle(Enum):
    LINE = "line"
    STEPLINE = "stepline"
    HISTOGRAM = "histogram"
    CROSS = "cross"
    CIRCLES = "circles"
    AREA = "area"
    COLUMNS = "columns"
    BARS = "bars"
    CANDLESTICKS = "candlesticks"
    RENKO = "renko"
    KAGI = "kagi"
    POINTFIGURE = "pointfigure"
    LINEBREAK = "linebreak"

@dataclass
class VisualElement:
    id: str
    type: str
    style: str
    color: str
    data: Any
    properties: Dict[str, Any]

class ChartEngine:
    def __init__(self):
        self.elements: Dict[str, VisualElement] = {}
        self.colors = {
            'aqua': '#00FFFF',
            'black': '#000000',
            'blue': '#0000FF',
            'fuchsia': '#FF00FF',
            'gray': '#808080',
            'green': '#008000',
            'lime': '#00FF00',
            'maroon': '#800000',
            'navy': '#000080',
            'olive': '#808000',
            'orange': '#FFA500',
            'purple': '#800080',
            'red': '#FF0000',
            'silver': '#C0C0C0',
            'teal': '#008080',
            'white': '#FFFFFF',
            'yellow': '#FFFF00'
        }
        
    def set_style(self, element_id: str, style: str) -> bool:
        if element_id in self.elements:
            self.elements[element_id].style = style
            return True
        return False
        
    def get_color(self, color_name: str) -> str:
        return self.colors.get(color_name, '#000000')
        
    def create_gradient_color(self, start_color: str, end_color: str, percent: float) -> str:
        start_rgb = self._hex_to_rgb(start_color)
        end_rgb = self._hex_to_rgb(end_color)
        
        r = int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * percent)
        g = int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * percent)
        b = int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * percent)
        
        return f'#{r:02x}{g:02x}{b:02x}'
        
    def _hex_to_rgb(self, hex_color: str) -> Tuple[int, int, int]:
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

class DrawingEngine:
    def __init__(self):
        self.elements: Dict[str, VisualElement] = {}
        self.next_id = 1
        
    def create_line(self, x1: float, y1: float, x2: float, y2: float) -> str:
        element_id = f"line_{self.next_id}"
        self.next_id += 1
        
        self.elements[element_id] = VisualElement(
            id=element_id,
            type='line',
            style='solid',
            color='#000000',
            data={'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2},
            properties={'width': 1}
        )
        return element_id
        
    def delete_line(self, line_id: str) -> bool:
        if line_id in self.elements:
            del self.elements[line_id]
            return True
        return False
        
    def set_line_start(self, line_id: str, x: float, y: float) -> bool:
        if line_id in self.elements:
            self.elements[line_id].data['x1'] = x
            self.elements[line_id].data['y1'] = y
            return True
        return False
        
    def set_line_end(self, line_id: str, x: float, y: float) -> bool:
        if line_id in self.elements:
            self.elements[line_id].data['x2'] = x
            self.elements[line_id].data['y2'] = y
            return True
        return False
        
    def set_line_color(self, line_id: str, color: str) -> bool:
        if line_id in self.elements:
            self.elements[line_id].color = color
            return True
        return False
        
    def set_line_width(self, line_id: str, width: float) -> bool:
        if line_id in self.elements:
            self.elements[line_id].properties['width'] = width
            return True
        return False
        
    def set_line_style(self, line_id: str, style: str) -> bool:
        if line_id in self.elements:
            self.elements[line_id].style = style
            return True
        return False
        
    def create_box(self, left: float, top: float, right: float, bottom: float) -> str:
        element_id = f"box_{self.next_id}"
        self.next_id += 1
        
        self.elements[element_id] = VisualElement(
            id=element_id,
            type='box',
            style='solid',
            color='#000000',
            data={'left': left, 'top': top, 'right': right, 'bottom': bottom},
            properties={'bgcolor': '#FFFFFF', 'border_width': 1}
        )
        return element_id
        
    def delete_box(self, box_id: str) -> bool:
        if box_id in self.elements:
            del self.elements[box_id]
            return True
        return False
        
    def set_box_bounds(self, box_id: str, left: float, top: float, right: float, bottom: float) -> bool:
        if box_id in self.elements:
            self.elements[box_id].data.update({
                'left': left,
                'top': top,
                'right': right,
                'bottom': bottom
            })
            return True
        return False
        
    def set_box_bgcolor(self, box_id: str, color: str) -> bool:
        if box_id in self.elements:
            self.elements[box_id].properties['bgcolor'] = color
            return True
        return False
        
    def set_box_border_color(self, box_id: str, color: str) -> bool:
        if box_id in self.elements:
            self.elements[box_id].color = color
            return True
        return False
        
    def set_box_border_width(self, box_id: str, width: float) -> bool:
        if box_id in self.elements:
            self.elements[box_id].properties['border_width'] = width
            return True
        return False
        
    def create_label(self, x: float, y: float, text: str) -> str:
        element_id = f"label_{self.next_id}"
        self.next_id += 1
        
        self.elements[element_id] = VisualElement(
            id=element_id,
            type='label',
            style='normal',
            color='#000000',
            data={'x': x, 'y': y, 'text': text},
            properties={'size': 12, 'font': 'Arial'}
        )
        return element_id
        
    def delete_label(self, label_id: str) -> bool:
        if label_id in self.elements:
            del self.elements[label_id]
            return True
        return False
        
    def set_label_text(self, label_id: str, text: str) -> bool:
        if label_id in self.elements:
            self.elements[label_id].data['text'] = text
            return True
        return False
        
    def set_label_position(self, label_id: str, x: float, y: float) -> bool:
        if label_id in self.elements:
            self.elements[label_id].data.update({'x': x, 'y': y})
            return True
        return False
        
    def set_label_color(self, label_id: str, color: str) -> bool:
        if label_id in self.elements:
            self.elements[label_id].color = color
            return True
        return False
        
    def set_label_style(self, label_id: str, style: str) -> bool:
        if label_id in self.elements:
            self.elements[label_id].style = style
            return True
        return False
        
    def create_table(self, rows: int, cols: int) -> str:
        element_id = f"table_{self.next_id}"
        self.next_id += 1
        
        data = [['' for _ in range(cols)] for _ in range(rows)]
        self.elements[element_id] = VisualElement(
            id=element_id,
            type='table',
            style='default',
            color='#000000',
            data=data,
            properties={'rows': rows, 'cols': cols}
        )
        return element_id
        
    def delete_table(self, table_id: str) -> bool:
        if table_id in self.elements:
            del self.elements[table_id]
            return True
        return False
        
    def set_table_cell(self, table_id: str, row: int, col: int, value: Any) -> bool:
        if table_id in self.elements:
            table = self.elements[table_id]
            if 0 <= row < table.properties['rows'] and 0 <= col < table.properties['cols']:
                table.data[row][col] = value
                return True
        return False
        
    def get_table_cell(self, table_id: str, row: int, col: int) -> Any:
        if table_id in self.elements:
            table = self.elements[table_id]
            if 0 <= row < table.properties['rows'] and 0 <= col < table.properties['cols']:
                return table.data[row][col]
        return None

class IndicatorEngine:
    def __init__(self):
        self.indicators: Dict[str, VisualElement] = {}
        
    def set_buffers(self, indicator_id: str, count: int) -> bool:
        if indicator_id in self.indicators:
            self.indicators[indicator_id].properties['buffer_count'] = count
            return True
        return False
        
    def set_color(self, indicator_id: str, color: str) -> bool:
        if indicator_id in self.indicators:
            self.indicators[indicator_id].color = color
            return True
        return False
        
    def set_width(self, indicator_id: str, width: float) -> bool:
        if indicator_id in self.indicators:
            self.indicators[indicator_id].properties['width'] = width
            return True
        return False
        
    def set_style(self, indicator_id: str, style: str) -> bool:
        if indicator_id in self.indicators:
            self.indicators[indicator_id].style = style
            return True
        return False
        
    def set_maximum(self, indicator_id: str, value: float) -> bool:
        if indicator_id in self.indicators:
            self.indicators[indicator_id].properties['maximum'] = value
            return True
        return False
        
    def set_minimum(self, indicator_id: str, value: float) -> bool:
        if indicator_id in self.indicators:
            self.indicators[indicator_id].properties['minimum'] = value
            return True
        return False
        
    def set_overlay(self, indicator_id: str) -> bool:
        if indicator_id in self.indicators:
            self.indicators[indicator_id].properties['overlay'] = True
            return True
        return False
        
    def set_separate(self, indicator_id: str) -> bool:
        if indicator_id in self.indicators:
            self.indicators[indicator_id].properties['overlay'] = False
            return True
        return False

import numpy as np
from typing import Any, Dict, List, Optional, Tuple, Union
from dataclasses import dataclass

@dataclass
class PlotStyle:
    SOLID = "solid"
    DOTTED = "dotted" 
    DASHED = "dashed"
    ARROW = "arrow"
    CIRCLE = "circle"
    CROSS = "cross"
    DIAMOND = "diamond"
    SQUARE = "square"
    TRIANGLE_UP = "triangle_up"
    TRIANGLE_DOWN = "triangle_down"
    FLAG = "flag"
    LABEL = "label"
    TEXT = "text"
    HISTOGRAM = "histogram"

@dataclass 
class Position:
    TOP_LEFT = "top_left"
    TOP_CENTER = "top_center"
    TOP_RIGHT = "top_right"
    MIDDLE_LEFT = "middle_left"
    MIDDLE_CENTER = "middle_center"
    MIDDLE_RIGHT = "middle_right"
    BOTTOM_LEFT = "bottom_left"
    BOTTOM_CENTER = "bottom_center"
    BOTTOM_RIGHT = "bottom_right"

class PlotEngine:
    def __init__(self):
        self.plots = {}
        self.plot_id = 0
        self.overlay_plots = []
        self.separate_plots = []
        self.tables = {}
        self.labels = {}
        self.shapes = {}
        self.chart_settings = {}
        
    def _get_new_id(self) -> int:
        self.plot_id += 1
        return self.plot_id

    # Basic Plots
    def plot(self, series: np.ndarray, title: str = "", color: str = "", 
             width: int = 1, style: str = PlotStyle.SOLID, transp: float = 0) -> int:
        plot_id = self._get_new_id()
        self.plots[plot_id] = {
            "type": "line",
            "data": series,
            "title": title,
            "color": color,
            "width": width,
            "style": style,
            "transparency": transp
        }
        return plot_id

    def plotshape(self, series: np.ndarray, shape: str = "circle", 
                  size: str = "normal", location: str = "abovebar",
                  color: str = "", title: str = "") -> int:
        plot_id = self._get_new_id()
        self.plots[plot_id] = {
            "type": "shape",
            "data": series,
            "shape": shape,
            "size": size,
            "location": location,
            "color": color,
            "title": title
        }
        return plot_id

    def plotchar(self, series: np.ndarray, char: str = "•", 
                 size: str = "normal", location: str = "abovebar",
                 color: str = "", title: str = "") -> int:
        plot_id = self._get_new_id()
        self.plots[plot_id] = {
            "type": "char",
            "data": series,
            "char": char,
            "size": size,
            "location": location,
            "color": color,
            "title": title
        }
        return plot_id

    def plotarrow(self, series: np.ndarray, direction: str = "up",
                  size: str = "normal", color: str = "", title: str = "") -> int:
        plot_id = self._get_new_id()
        self.plots[plot_id] = {
            "type": "arrow",
            "data": series,
            "direction": direction,
            "size": size,
            "color": color,
            "title": title
        }
        return plot_id

    def plotcandle(self, open: np.ndarray, high: np.ndarray, 
                   low: np.ndarray, close: np.ndarray,
                   bull_color: str = "green", bear_color: str = "red",
                   wickcolor: str = "") -> int:
        plot_id = self._get_new_id()
        self.plots[plot_id] = {
            "type": "candle",
            "data": {
                "open": open,
                "high": high,
                "low": low,
                "close": close
            },
            "bull_color": bull_color,
            "bear_color": bear_color,
            "wick_color": wickcolor
        }
        return plot_id

    def plotbar(self, open: np.ndarray, high: np.ndarray,
                low: np.ndarray, close: np.ndarray,
                color: str = "", width: int = 1) -> int:
        plot_id = self._get_new_id()
        self.plots[plot_id] = {
            "type": "bar",
            "data": {
                "open": open,
                "high": high,
                "low": low,
                "close": close
            },
            "color": color,
            "width": width
        }
        return plot_id

    def plothistogram(self, series: np.ndarray, title: str = "",
                     color: str = "", style: str = "histogram") -> int:
        plot_id = self._get_new_id()
        self.plots[plot_id] = {
            "type": "histogram",
            "data": series,
            "title": title,
            "color": color,
            "style": style
        }
        return plot_id

    def plotscatter(self, x: np.ndarray, y: np.ndarray,
                    color: str = "", size: int = 5,
                    style: str = "circle") -> int:
        plot_id = self._get_new_id()
        self.plots[plot_id] = {
            "type": "scatter",
            "data": {
                "x": x,
                "y": y
            },
            "color": color,
            "size": size,
            "style": style
        }
        return plot_id

    def plotarea(self, series: np.ndarray, base: float = 0,
                 color: str = "", transp: float = 0) -> int:
        plot_id = self._get_new_id()
        self.plots[plot_id] = {
            "type": "area",
            "data": series,
            "base": base,
            "color": color,
            "transparency": transp
        }
        return plot_id

    def plotbubble(self, x: np.ndarray, y: np.ndarray,
                   size: np.ndarray, color: str = "") -> int:
        plot_id = self._get_new_id()
        self.plots[plot_id] = {
            "type": "bubble",
            "data": {
                "x": x,
                "y": y,
                "size": size
            },
            "color": color
        }
        return plot_id

    def plotmap(self, matrix: np.ndarray,
                color_scheme: str = "viridis") -> int:
        plot_id = self._get_new_id()
        self.plots[plot_id] = {
            "type": "map",
            "data": matrix,
            "color_scheme": color_scheme
        }
        return plot_id

    def plotcandlestick(self, open: np.ndarray, high: np.ndarray,
                        low: np.ndarray, close: np.ndarray,
                        title: str = "") -> int:
        plot_id = self._get_new_id()
        self.plots[plot_id] = {
            "type": "candlestick",
            "data": {
                "open": open,
                "high": high,
                "low": low,
                "close": close
            },
            "title": title
        }
        return plot_id

    def plotvolume(self, volume: np.ndarray, color: str = "",
                   up_color: str = "", down_color: str = "") -> int:
        plot_id = self._get_new_id()
        self.plots[plot_id] = {
            "type": "volume",
            "data": volume,
            "color": color,
            "up_color": up_color,
            "down_color": down_color
        }
        return plot_id

    def plotprofile(self, price: np.ndarray, volume: np.ndarray,
                    bins: int = 100, color: str = "") -> int:
        hist, bins = np.histogram(price, bins=bins, weights=volume)
        plot_id = self._get_new_id()
        self.plots[plot_id] = {
            "type": "profile",
            "data": {
                "histogram": hist,
                "bins": bins
            },
            "color": color
        }
        return plot_id

    def plotheatmap(self, matrix: np.ndarray,
                    colormap: str = "viridis",
                    min_value: float = None,
                    max_value: float = None) -> int:
        plot_id = self._get_new_id()
        self.plots[plot_id] = {
            "type": "heatmap",
            "data": matrix,
            "colormap": colormap,
            "min_value": min_value or np.min(matrix),
            "max_value": max_value or np.max(matrix)
        }
        return plot_id

    def plotzig(self, series: np.ndarray,
                deviation: float = 5,
                color: str = "") -> int:
        # Calculate zigzag points
        plot_id = self._get_new_id()
        self.plots[plot_id] = {
            "type": "zigzag",
            "data": series,
            "deviation": deviation,
            "color": color
        }
        return plot_id

    def plotchart(self, data: Dict,
                  type: str = "line",
                  color: str = "") -> int:
        plot_id = self._get_new_id()
        self.plots[plot_id] = {
            "type": "chart",
            "data": data,
            "chart_type": type,
            "color": color
        }
        return plot_id

    # Lines
    def line(self, x1: float, y1: float,
             x2: float, y2: float,
             color: str = "",
             width: int = 1) -> int:
        plot_id = self._get_new_id()
        self.plots[plot_id] = {
            "type": "line_segment",
            "data": {
                "x1": x1,
                "y1": y1,
                "x2": x2,
                "y2": y2
            },
            "color": color,
            "width": width
        }
        return plot_id

    def hline(self, price: float,
              color: str = "",
              width: int = 1,
              style: str = PlotStyle.SOLID,
              title: str = "") -> int:
        plot_id = self._get_new_id()
        self.plots[plot_id] = {
            "type": "hline",
            "data": price,
            "color": color,
            "width": width,
            "style": style,
            "title": title
        }
        return plot_id

    def vline(self, time: int,
              color: str = "",
              width: int = 1,
              style: str = PlotStyle.SOLID) -> int:
        plot_id = self._get_new_id()
        self.plots[plot_id] = {
            "type": "vline",
            "data": time,
            "color": color,
            "width": width,
            "style": style
        }
        return plot_id

    def trendline(self, points: List[Tuple[float, float]],
                  color: str = "",
                  width: int = 1) -> int:
        plot_id = self._get_new_id()
        self.plots[plot_id] = {
            "type": "trendline",
            "data": points,
            "color": color,
            "width": width
        }
        return plot_id

    def rayline(self, x: float, y: float,
                angle: float,
                color: str = "") -> int:
        plot_id = self._get_new_id()
        self.plots[plot_id] = {
            "type": "rayline",
            "data": {
                "x": x,
                "y": y,
                "angle": angle
            },
            "color": color
        }
        return plot_id

    def polyline(self, points: List[Tuple[float, float]],
                 color: str = "",
                 width: int = 1) -> int:
        plot_id = self._get_new_id()
        self.plots[plot_id] = {
            "type": "polyline",
            "data": points,
            "color": color,
            "width": width
        }
        return plot_id

    # Shapes
    def box(self, left: float, top: float,
            right: float, bottom: float,
            color: str = "") -> int:
        plot_id = self._get_new_id()
        self.plots[plot_id] = {
            "type": "box",
            "data": {
                "left": left,
                "top": top,
                "right": right,
                "bottom": bottom
            },
            "color": color
        }
        return plot_id

    def rectangle(self, x: float, y: float,
                 width: float, height: float,
                 color: str = "") -> int:
        return self.box(x, y, x + width, y + height, color)

    def circle(self, x: float, y: float,
               radius: float,
               color: str = "") -> int:
        plot_id = self._get_new_id()
        self.plots[plot_id] = {
            "type": "circle",
            "data": {
                "x": x,
                "y": y,
                "radius": radius
            },
            "color": color
        }
        return plot_id

    def triangle(self, x1: float, y1: float,
                 x2: float, y2: float,
                 x3: float, y3: float,
                 color: str = "") -> int:
        plot_id = self._get_new_id()
        self.plots[plot_id] = {
            "type": "triangle",
            "data": {
                "x1": x1, "y1": y1,
                "x2": x2, "y2": y2,
                "x3": x3, "y3": y3
            },
            "color": color
        }
        return plot_id

    # Tables
    def table_new(self, position: str = Position.TOP_RIGHT,
                  rows: int = 1,
                  cols: int = 1) -> int:
        table_id = self._get_new_id()
        self.tables[table_id] = {
            "position": position,
            "rows": rows,
            "cols": cols,
            "cells": [[None for _ in range(cols)] for _ in range(rows)]
        }
        return table_id

    def table_set(self, table_id: int,
                  row: int, col: int,
                  text: str = "") -> bool:
        if table_id in self.tables:
            self.tables[table_id]["cells"][row][col] = {
                "text": text,
                "bgcolor": "",
                "text_color": "",
                "text_halign": "center",
                "text_valign": "center"
            }
            return True
        return False

    def table_cell(self, table_id: int, row: int, col: int) -> Dict:
        if table_id in self.tables:
            return self.tables[table_id]["cells"][row][col]
        return None

    def table_merge(self, table_id: int, from_row: int, from_col: int,
                    to_row: int, to_col: int) -> bool:
        if table_id in self.tables:
            self.tables[table_id]["merged_cells"] = {
                "from_row": from_row,
                "from_col": from_col,
                "to_row": to_row,
                "to_col": to_col
            }
            return True
        return False

    def table_style(self, table_id: int, style: Dict) -> bool:
        if table_id in self.tables:
            self.tables[table_id].update(style)
            return True
        return False

    # Labels
    def label_new(self, x: float, y: float, text: str, color: str = "") -> int:
        label_id = self._get_new_id()
        self.labels[label_id] = {
            "x": x,
            "y": y,
            "text": text,
            "color": color,
            "style": "label",
            "size": "normal",
            "align": "center"
        }
        return label_id

    def label_set(self, label_id: int, text: str) -> bool:
        if label_id in self.labels:
            self.labels[label_id]["text"] = text
            return True
        return False

    def label_delete(self, label_id: int) -> bool:
        if label_id in self.labels:
            del self.labels[label_id]
            return True
        return False

    # Colors
    def colorrgb(self, r: int, g: int, b: int) -> str:
        return f"rgb({r},{g},{b})"

    def colorhsl(self, h: float, s: float, l: float) -> str:
        return f"hsl({h},{s}%,{l}%)"

    def colorfade(self, color: str, fade: float) -> str:
        return f"rgba({color},{1-fade})"

    def colormix(self, colors: List[str], weights: List[float]) -> str:
        # Weighted color mixing implementation
        return colors[0]  # Placeholder

    # Chart Settings
    def chart_theme(self, theme: str) -> None:
        self.chart_settings["theme"] = theme

    def chart_style(self, style: str) -> None:
        self.chart_settings["style"] = style

    def chart_grid(self, show: bool = True) -> None:
        self.chart_settings["show_grid"] = show

    def chart_background(self, color: str) -> None:
        self.chart_settings["background"] = color

    def chart_selection(self, mode: str) -> None:
        self.chart_settings["selection_mode"] = mode

    def chart_zoom(self, level: float) -> None:
        self.chart_settings["zoom_level"] = level

    def chart_time_scale(self, scale: str) -> None:
        self.chart_settings["time_scale"] = scale

    # Utility Methods
    def get_plot_data(self, plot_id: int) -> Dict:
        return self.plots.get(plot_id, None)

    def get_all_plots(self) -> Dict:
        return {
            "plots": self.plots,
            "tables": self.tables,
            "labels": self.labels,
            "chart_settings": self.chart_settings
        }

    def clear_all(self) -> None:
        self.plots = {}
        self.tables = {}
        self.labels = {}
        self.plot_id = 0
        self.chart_settings = {}

    def table_col(self, table_id: int, col: int) -> List:
        if table_id in self.tables:
            return [row[col] for row in self.tables[table_id]["cells"]]
        return []

    def table_row(self, table_id: int, row: int) -> List:
        if table_id in self.tables:
            return self.tables[table_id]["cells"][row]
        return []

    def table_delete(self, table_id: int) -> bool:
        if table_id in self.tables:
            del self.tables[table_id]
            return True
        return False

    def table_clear(self, table_id: int) -> bool:
        if table_id in self.tables:
            rows = self.tables[table_id]["rows"]
            cols = self.tables[table_id]["cols"]
            self.tables[table_id]["cells"] = [[None for _ in range(cols)] for _ in range(rows)]
            return True
        return False

    def label_text(self, label_id: int) -> str:
        return self.labels.get(label_id, {}).get("text", "")

    def label_style(self, label_id: int, style: str) -> bool:
        if label_id in self.labels:
            self.labels[label_id]["style"] = style
            return True
        return False

    def label_color(self, label_id: int, color: str) -> bool:
        if label_id in self.labels:
            self.labels[label_id]["color"] = color
            return True
        return False

    def label_size(self, label_id: int, size: str) -> bool:
        if label_id in self.labels:
            self.labels[label_id]["size"] = size
            return True
        return False

    def label_align(self, label_id: int, align: str) -> bool:
        if label_id in self.labels:
            self.labels[label_id]["align"] = align
            return True
        return False

    def label_position(self, label_id: int, x: float, y: float) -> bool:
        if label_id in self.labels:
            self.labels[label_id].update({"x": x, "y": y})
            return True
        return False

    def label_tooltip(self, label_id: int, tooltip: str) -> bool:
        if label_id in self.labels:
            self.labels[label_id]["tooltip"] = tooltip
            return True
        return False

    def label_format(self, label_id: int, format_str: str) -> bool:
        if label_id in self.labels:
            self.labels[label_id]["format"] = format_str
            return True
        return False

    def bgcolor(self, color: str, transp: float = 0) -> None:
        self.chart_settings["bgcolor"] = {"color": color, "transparency": transp}

    def barcolor(self, color: str) -> None:
        self.chart_settings["barcolor"] = color

    def textcolor(self, color: str) -> None:
        self.chart_settings["textcolor"] = color

    def fillcolor(self, color: str, transp: float = 0) -> None:
        self.chart_settings["fillcolor"] = {"color": color, "transparency": transp}

    def bordercolor(self, color: str) -> None:
        self.chart_settings["bordercolor"] = color

    def gradientcolor(self, color1: str, color2: str) -> Dict:
        return {"type": "gradient", "color1": color1, "color2": color2}

    def transparencycolor(self, color: str, transp: float) -> str:
        return f"rgba({color},{1-transp})"

    def colorblend(self, color1: str, color2: str, weight: float) -> str:
        return f"blend({color1},{color2},{weight})"

    def chart_overlay(self, value: bool = True) -> None:
        self.chart_settings["overlay"] = value

    def chart_separate(self, value: bool = True) -> None:
        self.chart_settings["separate"] = value

    def chart_same_scale(self, value: bool = True) -> None:
        self.chart_settings["same_scale"] = value

    def get_chart_settings(self) -> Dict:
        return self.chart_settings

    def get_table_data(self, table_id: int) -> Dict:
        return self.tables.get(table_id, None)

    def get_label_data(self, label_id: int) -> Dict:
        return self.labels.get(label_id, None)

    def update_plot_style(self, plot_id: int, style: Dict) -> bool:
        if plot_id in self.plots:
            self.plots[plot_id].update(style)
            return True
        return False

    def merge_plots(self, plot_ids: List[int]) -> int:
        new_plot_id = self._get_new_id()
        merged_data = []
        for pid in plot_ids:
            if pid in self.plots:
                merged_data.append(self.plots[pid])
        self.plots[new_plot_id] = {
            "type": "merged",
            "data": merged_data
        }
        return new_plot_id

    def export_plot_data(self, format: str = "json") -> Dict:
        return {
            "plots": self.plots,
            "tables": self.tables,
            "labels": self.labels,
            "chart_settings": self.chart_settings,
            "format": format
        }

    def import_plot_data(self, data: Dict) -> bool:
        try:
            self.plots.update(data.get("plots", {}))
            self.tables.update(data.get("tables", {}))
            self.labels.update(data.get("labels", {}))
            self.chart_settings.update(data.get("chart_settings", {}))
            return True
        except:
            return False

    def reset(self) -> None:
        self.__init__()

    def linefill(self, line1_id: int, line2_id: int, color: str = "") -> int:
        plot_id = self._get_new_id()
        self.plots[plot_id] = {
            "type": "linefill",
            "data": {
                "line1": self.plots.get(line1_id),
                "line2": self.plots.get(line2_id)
            },
            "color": color
        }
        return plot_id

    def linebreak(self, series: np.ndarray, color: str = "") -> int:
        plot_id = self._get_new_id()
        self.plots[plot_id] = {
            "type": "linebreak",
            "data": series,
            "color": color
        }
        return plot_id

    def linestyle(self, line_id: int, style: str = PlotStyle.SOLID) -> bool:
        if line_id in self.plots:
            self.plots[line_id]["style"] = style
            return True
        return False

    def linewidth(self, line_id: int, width: int = 1) -> bool:
        if line_id in self.plots:
            self.plots[line_id]["width"] = width
            return True
        return False

    def linecolor(self, line_id: int, color: str) -> bool:
        if line_id in self.plots:
            self.plots[line_id]["color"] = color
            return True
        return False

    def table_border(self, table_id: int, width: int = 1, color: str = "") -> bool:
        if table_id in self.tables:
            self.tables[table_id].update({
                "border_width": width,
                "border_color": color
            })
            return True
        return False

    def table_align(self, table_id: int, align: str = "center") -> bool:
        if table_id in self.tables:
            self.tables[table_id]["align"] = align
            return True
        return False

    def table_format(self, table_id: int, format_str: str) -> bool:
        if table_id in self.tables:
            self.tables[table_id]["format"] = format_str
            return True
        return False

    def diamond(self, x: float, y: float, size: float, color: str = "") -> int:
        plot_id = self._get_new_id()
        self.plots[plot_id] = {
            "type": "diamond",
            "data": {"x": x, "y": y, "size": size},
            "color": color
        }
        return plot_id

    def cross(self, x: float, y: float, size: float, color: str = "") -> int:
        plot_id = self._get_new_id()
        self.plots[plot_id] = {
            "type": "cross",
            "data": {"x": x, "y": y, "size": size},
            "color": color
        }
        return plot_id

    def arrowup(self, x: float, y: float, size: float, color: str = "") -> int:
        plot_id = self._get_new_id()
        self.plots[plot_id] = {
            "type": "arrowup",
            "data": {"x": x, "y": y, "size": size},
            "color": color
        }
        return plot_id

    def arrowdown(self, x: float, y: float, size: float, color: str = "") -> int:
        plot_id = self._get_new_id()
        self.plots[plot_id] = {
            "type": "arrowdown",
            "data": {"x": x, "y": y, "size": size},
            "color": color
        }
        return plot_id

    def flag(self, x: float, y: float, size: float, color: str = "") -> int:
        plot_id = self._get_new_id()
        self.plots[plot_id] = {
            "type": "flag",
            "data": {"x": x, "y": y, "size": size},
            "color": color
        }
        return plot_id

    def square(self, x: float, y: float, size: float, color: str = "") -> int:
        plot_id = self._get_new_id()
        self.plots[plot_id] = {
            "type": "square",
            "data": {"x": x, "y": y, "size": size},
            "color": color
        }
        return plot_id

    def star(self, x: float, y: float, size: float, color: str = "") -> int:
        plot_id = self._get_new_id()
        self.plots[plot_id] = {
            "type": "star",
            "data": {"x": x, "y": y, "size": size},
            "color": color
        }
        return plot_id

    def pentagon(self, x: float, y: float, size: float, color: str = "") -> int:
        plot_id = self._get_new_id()
        self.plots[plot_id] = {
            "type": "pentagon",
            "data": {"x": x, "y": y, "size": size},
            "color": color
        }
        return plot_id

    def hexagon(self, x: float, y: float, size: float, color: str = "") -> int:
        plot_id = self._get_new_id()
        self.plots[plot_id] = {
            "type": "hexagon",
            "data": {"x": x, "y": y, "size": size},
            "color": color
        }
        return plot_id

    def ellipse(self, x: float, y: float, width: float, height: float, color: str = "") -> int:
        plot_id = self._get_new_id()
        self.plots[plot_id] = {
            "type": "ellipse",
            "data": {
                "x": x,
                "y": y,
                "width": width,
                "height": height
            },
            "color": color
        }
        return plot_id
    
    def get_shape_data(self, shape_id: int) -> Dict:
        return self.shapes.get(shape_id, None)

    def calculate_shape_bounds(self, shape_type: str, data: Dict) -> Dict:
        bounds = {
            "min_x": float('inf'),
            "max_x": float('-inf'),
            "min_y": float('inf'),
            "max_y": float('-inf')
        }
        
        if shape_type in ["diamond", "cross", "arrowup", "arrowdown", "flag", "square", "star", "pentagon", "hexagon"]:
            size = data["size"] / 2
            bounds.update({
                "min_x": data["x"] - size,
                "max_x": data["x"] + size,
                "min_y": data["y"] - size,
                "max_y": data["y"] + size
            })
        elif shape_type == "ellipse":
            bounds.update({
                "min_x": data["x"] - data["width"] / 2,
                "max_x": data["x"] + data["width"] / 2,
                "min_y": data["y"] - data["height"] / 2,
                "max_y": data["y"] + data["height"] / 2
            })
            
        return bounds

    def update_shape_position(self, shape_id: int, x: float, y: float) -> bool:
        if shape_id in self.plots:
            self.plots[shape_id]["data"].update({"x": x, "y": y})
            return True
        return False

    def update_shape_size(self, shape_id: int, size: float) -> bool:
        if shape_id in self.plots:
            self.plots[shape_id]["data"]["size"] = size
            return True
        return False

    def update_shape_color(self, shape_id: int, color: str) -> bool:
        if shape_id in self.plots:
            self.plots[shape_id]["color"] = color
            return True
        return False

    def get_plot_statistics(self) -> Dict:
        return {
            "total_plots": len(self.plots),
            "total_tables": len(self.tables),
            "total_labels": len(self.labels),
            "plot_types": self._count_plot_types()
        }

    def _count_plot_types(self) -> Dict:
        type_counts = {}
        for plot in self.plots.values():
            plot_type = plot["type"]
            type_counts[plot_type] = type_counts.get(plot_type, 0) + 1
        return type_counts




class RenderEngine:
    def __init__(self):
        self.chart_engine = ChartEngine()
        self.drawing_engine = DrawingEngine()
        self.indicator_engine = IndicatorEngine()
        
    def get_registry(self) -> Dict[str, Any]:
        return {
            # Chart Styles
            'style_line': lambda id: self.chart_engine.set_style(id, 'line'),
            'style_stepline': lambda id: self.chart_engine.set_style(id, 'stepline'),
            'style_histogram': lambda id: self.chart_engine.set_style(id, 'histogram'),
            'style_cross': lambda id: self.chart_engine.set_style(id, 'cross'),
            'style_circles': lambda id: self.chart_engine.set_style(id, 'circles'),
            'style_area': lambda id: self.chart_engine.set_style(id, 'area'),
            'style_columns': lambda id: self.chart_engine.set_style(id, 'columns'),
            'style_bars': lambda id: self.chart_engine.set_style(id, 'bars'),
            'style_candlesticks': lambda id: self.chart_engine.set_style(id, 'candlesticks'),
            'style_renko': lambda id: self.chart_engine.set_style(id, 'renko'),
            'style_kagi': lambda id: self.chart_engine.set_style(id, 'kagi'),
            'style_pointfigure': lambda id: self.chart_engine.set_style(id, 'pointfigure'),
            'style_linebreak': lambda id: self.chart_engine.set_style(id, 'linebreak'),

            # Chart Colors
            'color_aqua': lambda: self.chart_engine.get_color('aqua'),
            'color_black': lambda: self.chart_engine.get_color('black'),
            'color_blue': lambda: self.chart_engine.get_color('blue'),
            'color_fuchsia': lambda: self.chart_engine.get_color('fuchsia'),
            'color_gray': lambda: self.chart_engine.get_color('gray'),
            'color_green': lambda: self.chart_engine.get_color('green'),
            'color_lime': lambda: self.chart_engine.get_color('lime'),
            'color_maroon': lambda: self.chart_engine.get_color('maroon'),
            'color_navy': lambda: self.chart_engine.get_color('navy'),
            'color_olive': lambda: self.chart_engine.get_color('olive'),
            'color_orange': lambda: self.chart_engine.get_color('orange'),
            'color_purple': lambda: self.chart_engine.get_color('purple'),
            'color_red': lambda: self.chart_engine.get_color('red'),
            'color_silver': lambda: self.chart_engine.get_color('silver'),
            'color_teal': lambda: self.chart_engine.get_color('teal'),
            'color_white': lambda: self.chart_engine.get_color('white'),
            'color_yellow': lambda: self.chart_engine.get_color('yellow'),
            'color_from_gradient': lambda start, end, percent: self.chart_engine.create_gradient_color(start, end, percent),

            # Drawing Tools
            'line_new': lambda x1, y1, x2, y2: self.drawing_engine.create_line(x1, y1, x2, y2),
            'line_delete': lambda id: self.drawing_engine.delete_line(id),
            'line_set_xy1': lambda id, x, y: self.drawing_engine.set_line_start(id, x, y),
            'line_set_xy2': lambda id, x, y: self.drawing_engine.set_line_end(id, x, y),
            'line_set_color': lambda id, color: self.drawing_engine.set_line_color(id, color),
            'line_set_width': lambda id, width: self.drawing_engine.set_line_width(id, width),
            'line_set_style': lambda id, style: self.drawing_engine.set_line_style(id, style),
            'box_new': lambda left, top, right, bottom: self.drawing_engine.create_box(left, top, right, bottom),
            'box_delete': lambda id: self.drawing_engine.delete_box(id),
            'box_set_bounds': lambda id, left, top, right, bottom: self.drawing_engine.set_box_bounds(id, left, top, right, bottom),
            'box_set_bgcolor': lambda id, color: self.drawing_engine.set_box_bgcolor(id, color),
            'box_set_border_color': lambda id, color: self.drawing_engine.set_box_border_color(id, color),
            'box_set_border_width': lambda id, width: self.drawing_engine.set_box_border_width(id, width),
            'label_new': lambda x, y, text: self.drawing_engine.create_label(x, y, text),
            'label_delete': lambda id: self.drawing_engine.delete_label(id),
            'label_set_text': lambda id, text: self.drawing_engine.set_label_text(id, text),
            'label_set_xy': lambda id, x, y: self.drawing_engine.set_label_position(id, x, y),
            'label_set_color': lambda id, color: self.drawing_engine.set_label_color(id, color),
            'label_set_style': lambda id, style: self.drawing_engine.set_label_style(id, style),
            'table_new': lambda rows, cols: self.drawing_engine.create_table(rows, cols),
            'table_delete': lambda id: self.drawing_engine.delete_table(id),
            'table_cell_set': lambda id, row, col, value: self.drawing_engine.set_table_cell(id, row, col, value),
            'table_cell_get': lambda id, row, col: self.drawing_engine.get_table_cell(id, row, col),

            # Indicator Display
            'indicator_buffers': lambda id, count: self.indicator_engine.set_buffers(id, count),
            'indicator_color': lambda id, color: self.indicator_engine.set_color(id, color),
            'indicator_width': lambda id, width: self.indicator_engine.set_width(id, width),
            'indicator_style': lambda id, style: self.indicator_engine.set_style(id, style),
            'indicator_maximum': lambda id, value: self.indicator_engine.set_maximum(id, value),
            'indicator_minimum': lambda id, value: self.indicator_engine.set_minimum(id, value),
            'indicator_overlay': lambda id: self.indicator_engine.set_overlay(id),
            'indicator_separate': lambda id: self.indicator_engine.set_separate(id),

            'plot': lambda series, title="", color="", width=1, style="line", transp=0: PlotEngine().plot(series, title, color, width, style, transp),
            'plotshape': lambda series, shape="circle", size="normal", location="abovebar", color="", title="": PlotEngine().plotshape(series, shape, size, location, color, title),
            'plotchar': lambda series, char="•", size="normal", location="abovebar", color="", title="": PlotEngine().plotchar(series, char, size, location, color, title),
            'plotarrow': lambda series, direction="up", size="normal", color="", title="": PlotEngine().plotarrow(series, direction, size, color, title),
            'plotcandle': lambda o, h, l, c, bull="green", bear="red", wick="": PlotEngine().plotcandle(o, h, l, c, bull, bear, wick),
            'plotbar': lambda o, h, l, c, color="", width=1: PlotEngine().plotbar(o, h, l, c, color, width),
            'plothistogram': lambda series, title="", color="", style="histogram": PlotEngine().plothistogram(series, title, color, style),
            'plotscatter': lambda x, y, color="", size=5, style="circle": PlotEngine().plotscatter(x, y, color, size, style),
            'plotarea': lambda series, base=0, color="", transp=0: PlotEngine().plotarea(series, base, color, transp),
            'plotbubble': lambda x, y, size, color="": PlotEngine().plotbubble(x, y, size, color),
            'plotmap': lambda matrix, color_scheme="viridis": PlotEngine().plotmap(matrix, color_scheme),
            'plotcandlestick': lambda o, h, l, c, title="": PlotEngine().plotcandlestick(o, h, l, c, title),
            'plotvolume': lambda vol, color="", up="", down="": PlotEngine().plotvolume(vol, color, up, down),
            'plotprofile': lambda price, vol, bins=100, color="": PlotEngine().plotprofile(price, vol, bins, color),
            'plotheatmap': lambda matrix, cmap="viridis", min_val=None, max_val=None: PlotEngine().plotheatmap(matrix, cmap, min_val, max_val),
            'plotzig': lambda series, deviation=5, color="": PlotEngine().plotzig(series, deviation, color),
            'plotchart': lambda data, type="line", color="": PlotEngine().plotchart(data, type, color),

            # Lines
            'hline': lambda price, color="", width=1, style="solid", title="": PlotEngine().hline(price, color, width, style, title),
            'vline': lambda time, color="", width=1, style="solid": PlotEngine().vline(time, color, width, style),
            'line': lambda x1, y1, x2, y2, color="", width=1: PlotEngine().line(x1, y1, x2, y2, color, width),
            'trendline': lambda points, color="", width=1: PlotEngine().trendline(points, color, width),
            'rayline': lambda x, y, angle, color="": PlotEngine().rayline(x, y, angle, color),
            'polyline': lambda points, color="", width=1: PlotEngine().polyline(points, color, width),
            'linefill': lambda line1, line2, color="": PlotEngine().linefill(line1, line2, color),
            'linebreak': lambda series, color="": PlotEngine().linebreak(series, color),
            'linestyle': lambda id, style="solid": PlotEngine().linestyle(id, style),
            'linewidth': lambda id, width=1: PlotEngine().linewidth(id, width),
            'linecolor': lambda id, color="": PlotEngine().linecolor(id, color),

            # Shapes
            'box': lambda left, top, right, bottom, color="": PlotEngine().box(left, top, right, bottom, color),
            'rectangle': lambda x, y, width, height, color="": PlotEngine().rectangle(x, y, width, height, color),
            'circle': lambda x, y, radius, color="": PlotEngine().circle(x, y, radius, color),
            'triangle': lambda x1, y1, x2, y2, x3, y3, color="": PlotEngine().triangle(x1, y1, x2, y2, x3, y3, color),
            'diamond': lambda x, y, size, color="": PlotEngine().diamond(x, y, size, color),
            'cross': lambda x, y, size, color="": PlotEngine().cross(x, y, size, color),
            'arrowup': lambda x, y, size, color="": PlotEngine().arrowup(x, y, size, color),
            'arrowdown': lambda x, y, size, color="": PlotEngine().arrowdown(x, y, size, color),
            'flag': lambda x, y, size, color="": PlotEngine().flag(x, y, size, color),
            'square': lambda x, y, size, color="": PlotEngine().square(x, y, size, color),
            'star': lambda x, y, size, color="": PlotEngine().star(x, y, size, color),
            'pentagon': lambda x, y, size, color="": PlotEngine().pentagon(x, y, size, color),
            'hexagon': lambda x, y, size, color="": PlotEngine().hexagon(x, y, size, color),
            'ellipse': lambda x, y, width, height, color="": PlotEngine().ellipse(x, y, width, height, color),

            # Tables
            'table.new': lambda pos="top_right", rows=1, cols=1: PlotEngine().table_new(pos, rows, cols),
            'table.set': lambda id, row, col, text="": PlotEngine().table_set(id, row, col, text),
            'table.cell': lambda id, row, col: PlotEngine().table_cell(id, row, col),
            'table.col': lambda id, col: PlotEngine().table_col(id, col),
            'table.row': lambda id, row: PlotEngine().table_row(id, row),
            'table.merge': lambda id, from_row, from_col, to_row, to_col: PlotEngine().table_merge(id, from_row, from_col, to_row, to_col),
            'table.delete': lambda id: PlotEngine().table_delete(id),
            'table.clear': lambda id: PlotEngine().table_clear(id),
            'table.style': lambda id, style: PlotEngine().table_style(id, style),
            'table.border': lambda id, width=1, color="": PlotEngine().table_border(id, width, color),
            'table.align': lambda id, align="center": PlotEngine().table_align(id, align),
            'table.format': lambda id, format="": PlotEngine().table_format(id, format),

            # Labels
            'label.new': lambda x, y, text, color="": PlotEngine().label_new(x, y, text, color),
            'label.set': lambda id, text="": PlotEngine().label_set(id, text),
            'label.delete': lambda id: PlotEngine().label_delete(id),
            'label.text': lambda id: PlotEngine().label_text(id),
            'label.style': lambda id, style: PlotEngine().label_style(id, style),
            'label.color': lambda id, color: PlotEngine().label_color(id, color),
            'label.size': lambda id, size: PlotEngine().label_size(id, size),
            'label.align': lambda id, align: PlotEngine().label_align(id, align),
            'label.position': lambda id, pos: PlotEngine().label_position(id, pos),
            'label.tooltip': lambda id, text: PlotEngine().label_tooltip(id, text),
            'label.format': lambda id, format: PlotEngine().label_format(id, format),

            # Colors
            'bgcolor': lambda color, transp=0: PlotEngine().bgcolor(color, transp),
            'barcolor': lambda color: PlotEngine().barcolor(color),
            'textcolor': lambda color: PlotEngine().textcolor(color),
            'fillcolor': lambda color, transp=0: PlotEngine().fillcolor(color, transp),
            'bordercolor': lambda color: PlotEngine().bordercolor(color),
            'gradientcolor': lambda color1, color2: PlotEngine().gradientcolor(color1, color2),
            'transparencycolor': lambda color, transp: PlotEngine().transparencycolor(color, transp),
            'colorblend': lambda color1, color2, weight: PlotEngine().colorblend(color1, color2, weight),
            'colorrgb': lambda r, g, b: PlotEngine().colorrgb(r, g, b),
            'colorhsl': lambda h, s, l: PlotEngine().colorhsl(h, s, l),
            'colorfade': lambda color, fade: PlotEngine().colorfade(color, fade),
            'colormix': lambda colors, weights: PlotEngine().colormix(colors, weights),

            # Chart Settings
            'chart.overlay': lambda value=True: PlotEngine().chart_overlay(value),
            'chart.separate': lambda value=True: PlotEngine().chart_separate(value),
            'chart.same_scale': lambda value=True: PlotEngine().chart_same_scale(value),
            'chart.style': lambda style: PlotEngine().chart_style(style),
            'chart.theme': lambda theme: PlotEngine().chart_theme(theme),
            'chart.grid': lambda show=True: PlotEngine().chart_grid(show),
            'chart.background': lambda color: PlotEngine().chart_background(color),
            'chart.selection': lambda mode: PlotEngine().chart_selection(mode),
            'chart.zoom': lambda level: PlotEngine().chart_zoom(level),
            'chart.time_scale': lambda scale: PlotEngine().chart_time_scale(scale)
        }
