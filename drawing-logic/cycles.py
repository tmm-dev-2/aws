import numpy as np
import math

def draw_cyclic_lines(start_x, end_x, y_min, y_max, period_adjust=1):
    """
    Draws cyclic vertical lines with adjustable period.

    Args:
        start_x (float): The x-coordinate of the first point.
        end_x (float): The x-coordinate of the second point.
        y_min (float): The minimum y-coordinate.
        y_max (float): The maximum y-coordinate.
        period_adjust (float): A multiplier to adjust the period.

    Returns:
        list: A list of tuples, where each tuple represents a line segment (x1, y1, x2, y2).
    """
    base_period = abs(end_x - start_x)
    period = base_period * period_adjust
    lines = []
    x = start_x
    while x <= end_x:
        lines.append((x, y_min, x, y_max))
        x += period
    return lines


def draw_time_cycles(start_x, end_x, y_min, y_max, period_adjust=1):
    """
    Draws time cycle vertical lines with adjustable period.

    Args:
        start_x (float): The x-coordinate of the first point.
        end_x (float): The x-coordinate of the second point.
        y_min (float): The minimum y-coordinate.
        y_max (float): The maximum y-coordinate.
        period_adjust (float): A multiplier to adjust the period.

    Returns:
        list: A list of tuples, where each tuple represents a line segment (x1, y1, x2, y2).
    """
    base_period = abs(end_x - start_x)
    period = base_period * period_adjust
    lines = []
    x = start_x
    while x <= end_x:
        lines.append((x, y_min, x, y_max))
        x += period
    return lines


def draw_sine_line(start_x, start_y, end_x, end_y, amplitude_adjust=1, period_adjust=1, num_points=100):
    """
    Draws a sine wave between two points with adjustable amplitude and period.

    Args:
        start_x (float): The x-coordinate of the first point.
        start_y (float): The y-coordinate of the first point.
        end_x (float): The x-coordinate of the second point.
        end_y (float): The y-coordinate of the second point.
        amplitude_adjust (float): A multiplier to adjust the amplitude.
        period_adjust (float): A multiplier to adjust the period.
        num_points (int): The number of points to use for drawing the sine wave.

    Returns:
        list: A list of tuples, where each tuple represents a point (x, y).
    """
    base_amplitude = abs(end_y - start_y) / 2
    amplitude = base_amplitude * amplitude_adjust
    mid_y = (start_y + end_y) / 2
    base_period = abs(end_x - start_x)
    period = base_period * period_adjust
    x_values = np.linspace(start_x, end_x, num_points)
    y_values = amplitude * np.sin(2 * np.pi * (x_values - start_x) / period) + mid_y
    return list(zip(x_values, y_values))