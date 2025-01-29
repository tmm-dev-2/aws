import math
import numpy as np

def rectangle(start_x, start_y, end_x, end_y):
    """
    Generates points for a rectangle and its adjustment points.
    """
    shape_points = [(start_x, start_y), (end_x, start_y), (end_x, end_y), (start_x, end_y), (start_x, start_y)]
    adjust_points = [
        (start_x, start_y),  # Top-left
        (end_x, start_y),    # Top-right
        (end_x, end_y),      # Bottom-right
        (start_x, end_y),    # Bottom-left
        ((start_x + end_x) / 2, start_y), # Top-center
        ((start_x + end_x) / 2, end_y), # Bottom-center
        (start_x, (start_y + end_y) / 2), # Left-center
        (end_x, (start_y + end_y) / 2), # Right-center
        ((start_x + end_x) / 2, (start_y + end_y) / 2) # Center
    ]
    return shape_points, adjust_points

def rotated_rectangle(start_x, start_y, end_x, end_y, angle):
    """
    Generates points for a rotated rectangle and its adjustment points.
    """
    center_x = (start_x + end_x) / 2
    center_y = (start_y + end_y) / 2
    
    points = [
        (start_x, start_y),
        (end_x, start_y),
        (end_x, end_y),
        (start_x, end_y)
    ]
    
    rotated_points = []
    for x, y in points:
        rotated_x = center_x + (x - center_x) * math.cos(angle) - (y - center_y) * math.sin(angle)
        rotated_y = center_y + (x - center_x) * math.sin(angle) + (y - center_y) * math.cos(angle)
        rotated_points.append((rotated_x, rotated_y))
    
    rotated_points.append(rotated_points[0])
    
    adjust_points = []
    for x, y in [
        (start_x, start_y),  # Top-left
        (end_x, start_y),    # Top-right
        (end_x, end_y),      # Bottom-right
        (start_x, end_y),    # Bottom-left
        ((start_x + end_x) / 2, start_y), # Top-center
        ((start_x + end_x) / 2, end_y), # Bottom-center
        (start_x, (start_y + end_y) / 2), # Left-center
        (end_x, (start_y + end_y) / 2), # Right-center
        ((start_x + end_x) / 2, (start_y + end_y) / 2) # Center
    ]:
        rotated_x = center_x + (x - center_x) * math.cos(angle) - (y - center_y) * math.sin(angle)
        rotated_y = center_y + (x - center_x) * math.sin(angle) + (y - center_y) * math.cos(angle)
        adjust_points.append((rotated_x, rotated_y))
    
    return rotated_points, adjust_points

def circle(center_x, center_y, radius, num_points=100):
    """
    Generates points for a circle and its adjustment points.
    """
    shape_points = []
    for i in range(num_points):
        angle = 2 * math.pi * i / num_points
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        shape_points.append((x, y))
    adjust_points = [
        (center_x + radius, center_y),  # Right
        (center_x - radius, center_y),  # Left
        (center_x, center_y + radius),  # Top
        (center_x, center_y - radius),  # Bottom
        (center_x, center_y) # Center
    ]
    return shape_points, adjust_points

def ellipse(center_x, center_y, radius_x, radius_y, num_points=100):
    """
    Generates points for an ellipse and its adjustment points.
    """
    shape_points = []
    for i in range(num_points):
        angle = 2 * math.pi * i / num_points
        x = center_x + radius_x * math.cos(angle)
        y = center_y + radius_y * math.sin(angle)
        shape_points.append((x, y))
    adjust_points = [
        (center_x + radius_x, center_y),  # Right
        (center_x - radius_x, center_y),  # Left
        (center_x, center_y + radius_y),  # Top
        (center_x, center_y - radius_y),  # Bottom
        (center_x, center_y) # Center
    ]
    return shape_points, adjust_points

def triangle(start_x, start_y, end_x, end_y):
    """
    Generates points for a triangle and its adjustment points.
    """
    mid_x = (start_x + end_x) / 2
    shape_points = [(start_x, end_y), (mid_x, start_y), (end_x, end_y), (start_x, end_y)]
    adjust_points = [
        (start_x, end_y),  # Bottom-left
        (mid_x, start_y),    # Top
        (end_x, end_y),      # Bottom-right
        ((start_x + mid_x) / 2, (start_y + end_y) / 2), # Left-center
        ((mid_x + end_x) / 2, (start_y + end_y) / 2), # Right-center
        ((start_x + end_x) / 2, end_y), # Bottom-center
        (mid_x, (start_y + end_y) / 2) # Center
    ]
    return shape_points, adjust_points

def arc(center_x, center_y, radius, start_angle, end_angle, num_points=100):
    """
    Generates points for an arc and its adjustment points.
    """
    shape_points = []
    angle_range = end_angle - start_angle
    for i in range(num_points):
        angle = start_angle + angle_range * i / num_points
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        shape_points.append((x, y))
    
    adjust_points = [
        (center_x + radius * math.cos(start_angle), center_y + radius * math.sin(start_angle)), # Start point
        (center_x + radius * math.cos(end_angle), center_y + radius * math.sin(end_angle)), # End point
        (center_x, center_y) # Center
    ]
    return shape_points, adjust_points

def curve(start_x, start_y, control_x, control_y, end_x, end_y, num_points=100):
    """
    Generates points for a quadratic Bezier curve and its adjustment points.
    """
    shape_points = []
    for i in range(num_points + 1):
        t = i / num_points
        x = (1 - t) * (1 - t) * start_x + 2 * (1 - t) * t * control_x + t * t * end_x
        y = (1 - t) * (1 - t) * start_y + 2 * (1 - t) * t * control_y + t * t * end_y
        shape_points.append((x, y))
    adjust_points = [
        (start_x, start_y),
        (control_x, control_y),
        (end_x, end_y)
    ]
    return shape_points, adjust_points

def double_curve(start_x, start_y, control1_x, control1_y, control2_x, control2_y, end_x, end_y, num_points=100):
    """
    Generates points for a cubic Bezier curve and its adjustment points.
    """
    shape_points = []
    for i in range(num_points + 1):
        t = i / num_points
        x = (1 - t)**3 * start_x + 3 * (1 - t)**2 * t * control1_x + 3 * (1 - t) * t**2 * control2_x + t**3 * end_x
        y = (1 - t)**3 * start_y + 3 * (1 - t)**2 * t * control1_y + 3 * (1 - t) * t**2 * control2_y + t**3 * end_y
        shape_points.append((x, y))
    adjust_points = [
        (start_x, start_y),
        (control1_x, control1_y),
        (control2_x, control2_y),
        (end_x, end_y)
    ]
    return shape_points, adjust_points