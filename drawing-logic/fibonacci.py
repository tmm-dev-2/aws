import math

def calculate_fib_retracement(start_point, end_point, adjustment_point1=None, adjustment_point2=None):
    """
    Calculates the Fibonacci retracement levels with adjustment points.

    Args:
        start_point (tuple): The (x, y) coordinates of the starting point.
        end_point (tuple): The (x, y) coordinates of the ending point.
        adjustment_point1 (tuple, optional): The (x, y) coordinates of the first adjustment point. Defaults to None.
        adjustment_point2 (tuple, optional): The (x, y) coordinates of the second adjustment point. Defaults to None.

    Returns:
        dict: A dictionary containing the y-coordinates of the Fibonacci retracement levels.
    """
    x1, y1 = start_point
    x2, y2 = end_point

    if adjustment_point1 and adjustment_point2:
        ax1, ay1 = adjustment_point1
        ax2, ay2 = adjustment_point2

        # Calculate the adjusted y-coordinates based on the adjustment points
        y1 = ay1
        y2 = ay2

    levels = [0, 0.236, 0.382, 0.5, 0.618, 0.786, 1]
    
    diff = y2 - y1
    
    retracement_levels = {}
    for level in levels:
        y = y1 + diff * level
        retracement_levels[level] = y
    
    return retracement_levels

def calculate_fib_extension(start_point, middle_point, end_point, adjustment_point1=None, adjustment_point2=None, adjustment_point3=None):
    """
    Calculates the Fibonacci extension levels with adjustment points.

    Args:
        start_point (tuple): The (x, y) coordinates of the starting point.
        middle_point (tuple): The (x, y) coordinates of the middle point.
        end_point (tuple): The (x, y) coordinates of the ending point.
        adjustment_point1 (tuple, optional): The (x, y) coordinates of the first adjustment point. Defaults to None.
        adjustment_point2 (tuple, optional): The (x, y) coordinates of the second adjustment point. Defaults to None.
        adjustment_point3 (tuple, optional): The (x, y) coordinates of the third adjustment point. Defaults to None.

    Returns:
        dict: A dictionary containing the y-coordinates of the Fibonacci extension levels.
    """
    x1, y1 = start_point
    x2, y2 = middle_point
    x3, y3 = end_point

    if adjustment_point1 and adjustment_point2 and adjustment_point3:
        ax1, ay1 = adjustment_point1
        ax2, ay2 = adjustment_point2
        ax3, ay3 = adjustment_point3

        # Calculate the adjusted y-coordinates based on the adjustment points
        y1 = ay1
        y2 = ay2
        y3 = ay3

    levels = [0, 0.236, 0.382, 0.5, 0.618, 0.786, 1, 1.618, 2.618, 3.618, 4.236]

    diff = y2 - y1
    extension_diff = y3 - y2

    extension_levels = {}
    for level in levels:
        if level <= 1:
            y = y1 + diff * level
        else:
            y = y3 + extension_diff * (level - 1)
        extension_levels[level] = y
    
    return extension_levels

def calculate_fib_channel(start_point, end_point, adjustment_point1=None, adjustment_point2=None, channel_width_factor=1):
    """
    Calculates the Fibonacci channel lines with adjustment points.

    Args:
        start_point (tuple): The (x, y) coordinates of the starting point.
        end_point (tuple): The (x, y) coordinates of the ending point.
        adjustment_point1 (tuple, optional): The (x, y) coordinates of the first adjustment point. Defaults to None.
        adjustment_point2 (tuple, optional): The (x, y) coordinates of the second adjustment point. Defaults to None.
        channel_width_factor (float): A factor to adjust the width of the channel.

    Returns:
        dict: A dictionary containing the y-coordinates of the Fibonacci channel lines.
    """
    x1, y1 = start_point
    x2, y2 = end_point

    if adjustment_point1 and adjustment_point2:
        ax1, ay1 = adjustment_point1
        ax2, ay2 = adjustment_point2

        # Calculate the adjusted y-coordinates based on the adjustment points
        y1 = ay1
        y2 = ay2

    levels = [0, 0.236, 0.382, 0.5, 0.618, 0.786, 1, 1.618, 2.618, 3.618, 4.236]

    diff = y2 - y1
    
    channel_lines = {}
    for level in levels:
        y = y1 + diff * level * channel_width_factor
        channel_lines[level] = y
    
    return channel_lines

def calculate_fib_time_zones(start_point, end_point, adjustment_point1=None, adjustment_point2=None):
    """
    Calculates the x-coordinates for Fibonacci time zones with adjustment points.

    Args:
        start_point (tuple): The (x, y) coordinates of the starting point.
        end_point (tuple): The (x, y) coordinates of the ending point.
        adjustment_point1 (tuple, optional): The (x, y) coordinates of the first adjustment point. Defaults to None.
        adjustment_point2 (tuple, optional): The (x, y) coordinates of the second adjustment point. Defaults to None.

    Returns:
        dict: A dictionary containing the x-coordinates of the Fibonacci time zones.
    """
    x1, _ = start_point
    x2, _ = end_point

    if adjustment_point1 and adjustment_point2:
        ax1, _ = adjustment_point1
        ax2, _ = adjustment_point2

        # Calculate the adjusted x-coordinates based on the adjustment points
        x1 = ax1
        x2 = ax2
    
    levels = [0, 0.236, 0.382, 0.5, 0.618, 0.786, 1, 1.618, 2.618, 3.618, 4.236]
    
    diff = x2 - x1
    
    time_zones = {}
    for level in levels:
        x = x1 + diff * level
        time_zones[level] = x
    
    return time_zones

def calculate_fib_resistance_fan(start_point, end_point, adjustment_point1=None, adjustment_point2=None, fan_levels = [0.236, 0.382, 0.5, 0.618, 0.786, 1, 1.618, 2.618,]):
    """
    Calculates the angles for Fibonacci resistance fan lines with adjustment points.

    Args:
        start_point (tuple): The (x, y) coordinates of the starting point.
        end_point (tuple): The (x, y) coordinates of the ending point.
        adjustment_point1 (tuple, optional): The (x, y) coordinates of the first adjustment point. Defaults to None.
        adjustment_point2 (tuple, optional): The (x, y) coordinates of the second adjustment point. Defaults to None.
        fan_levels (list): A list of Fibonacci levels to use for the fan.

    Returns:
        list: A list of ExtendedLine objects representing the Fibonacci resistance fan lines.
    """
    x1, y1 = start_point
    x2, y2 = end_point

    if adjustment_point1 and adjustment_point2:
        ax1, ay1 = adjustment_point1
        ax2, ay2 = adjustment_point2

        # Calculate the adjusted coordinates based on the adjustment points
        x1 = ax1
        y1 = ay1
        x2 = ax2
        y2 = ay2
    
    fan_lines = []
    
    for level in fan_levels:
        diff_x = x2 - x1
        diff_y = y2 - y1
        
        angle = math.atan2(diff_y * level, diff_x)
        
        fan_line = ExtendedLine(x1, y1, angle)
        fan_lines.append(fan_line)
    
    return fan_lines
    import math

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
def calculate_fib_retracement(start_point, end_point, adjustment_point1=None, adjustment_point2=None):
    """
    Calculates the Fibonacci retracement levels with adjustment points.

    Args:
        start_point (tuple): The (x, y) coordinates of the starting point.
        end_point (tuple): The (x, y) coordinates of the ending point.
        adjustment_point1 (tuple, optional): The (x, y) coordinates of the first adjustment point. Defaults to None.
        adjustment_point2 (tuple, optional): The (x, y) coordinates of the second adjustment point. Defaults to None.

    Returns:
        dict: A dictionary containing the y-coordinates of the Fibonacci retracement levels.
    """
    x1, y1 = start_point
    x2, y2 = end_point

    if adjustment_point1 and adjustment_point2:
        ax1, ay1 = adjustment_point1
        ax2, ay2 = adjustment_point2

        # Calculate the adjusted y-coordinates based on the adjustment points
        y1 = ay1
        y2 = ay2

    levels = [0, 0.236, 0.382, 0.5, 0.618, 0.786, 1]
    
    diff = y2 - y1
    
    retracement_levels = {}
    for level in levels:
        y = y1 + diff * level
        retracement_levels[level] = y
    
    return retracement_levels

def calculate_fib_extension(start_point, middle_point, end_point, adjustment_point1=None, adjustment_point2=None, adjustment_point3=None):
    """
    Calculates the Fibonacci extension levels with adjustment points.

    Args:
        start_point (tuple): The (x, y) coordinates of the starting point.
        middle_point (tuple): The (x, y) coordinates of the middle point.
        end_point (tuple): The (x, y) coordinates of the ending point.
        adjustment_point1 (tuple, optional): The (x, y) coordinates of the first adjustment point. Defaults to None.
        adjustment_point2 (tuple, optional): The (x, y) coordinates of the second adjustment point. Defaults to None.
        adjustment_point3 (tuple, optional): The (x, y) coordinates of the third adjustment point. Defaults to None.

    Returns:
        dict: A dictionary containing the y-coordinates of the Fibonacci extension levels.
    """
    x1, y1 = start_point
    x2, y2 = middle_point
    x3, y3 = end_point

    if adjustment_point1 and adjustment_point2 and adjustment_point3:
        ax1, ay1 = adjustment_point1
        ax2, ay2 = adjustment_point2
        ax3, ay3 = adjustment_point3

        # Calculate the adjusted y-coordinates based on the adjustment points
        y1 = ay1
        y2 = ay2
        y3 = ay3

    levels = [0, 0.236, 0.382, 0.5, 0.618, 0.786, 1, 1.618, 2.618, 3.618, 4.236]

    diff = y2 - y1
    extension_diff = y3 - y2

    extension_levels = {}
    for level in levels:
        if level <= 1:
            y = y1 + diff * level
        else:
            y = y3 + extension_diff * (level - 1)
        extension_levels[level] = y
    
    return extension_levels

def calculate_fib_channel(start_point, end_point, adjustment_point1=None, adjustment_point2=None, channel_width_factor=1):
    """
    Calculates the Fibonacci channel lines with adjustment points.

    Args:
        start_point (tuple): The (x, y) coordinates of the starting point.
        end_point (tuple): The (x, y) coordinates of the ending point.
        adjustment_point1 (tuple, optional): The (x, y) coordinates of the first adjustment point. Defaults to None.
        adjustment_point2 (tuple, optional): The (x, y) coordinates of the second adjustment point. Defaults to None.
        channel_width_factor (float): A factor to adjust the width of the channel.

    Returns:
        dict: A dictionary containing the y-coordinates of the Fibonacci channel lines.
    """
    x1, y1 = start_point
    x2, y2 = end_point

    if adjustment_point1 and adjustment_point2:
        ax1, ay1 = adjustment_point1
        ax2, ay2 = adjustment_point2

        # Calculate the adjusted y-coordinates based on the adjustment points
        y1 = ay1
        y2 = ay2

    levels = [0, 0.236, 0.382, 0.5, 0.618, 0.786, 1, 1.618, 2.618, 3.618, 4.236]

    diff = y2 - y1
    
    channel_lines = {}
    for level in levels:
        y = y1 + diff * level * channel_width_factor
        channel_lines[level] = y
    
    return channel_lines

class TrendBasedFibTime:
    def __init__(self, start_point, end_point):
        self.start_point = start_point
        self.end_point = end_point
        self.levels = [0, 0.236, 0.382, 0.5, 0.618, 0.786, 1]

    def calculate_time_levels(self):
        time_diff = self.end_point.x - self.start_point.x
        levels_x = [self.start_point.x + level * time_diff for level in self.levels]
        return levels_x

    def get_adjusters(self):
        return [self.start_point, self.end_point]

class FibCircle:
    def __init__(self, center_point, radius_point):
        self.center_point = center_point
        self.radius_point = radius_point
        self.levels = [0, 0.236, 0.382, 0.5, 0.618, 0.786, 1, 1.5, 2.5, 3.618, 4.236, 4.618]

    def calculate_radii(self):
        radius = math.sqrt((self.radius_point.x - self.center_point.x)**2 + (self.radius_point.y - self.center_point.y)**2)
        radii = [level * radius for level in self.levels]
        return radii

    def get_adjusters(self):
        return [self.center_point, self.radius_point]

class FibSpeedResistanceArcs:
    def __init__(self, start_point, end_point):
        self.start_point = start_point
        self.end_point = end_point
        self.levels = [0, 0.236, 0.382, 0.5, 0.618, 0.786, 1, 1.618, 2.618, 3.618, 4.236, 4.618]

    def calculate_arcs(self):
         radius = math.sqrt((self.end_point.x - self.start_point.x)**2 + (self.end_point.y - self.start_point.y)**2)
         arcs = [level * radius for level in self.levels]
         return arcs

    def get_adjusters(self):
        return [self.start_point, self.end_point]

class FibWedge:
    def __init__(self, start_point, end_point):
        self.start_point = start_point
        self.end_point = end_point
        self.levels = [0, 0.236, 0.382, 0.5, 0.618, 0.786, 1]

    def calculate_wedge_levels(self):
        angle = math.atan2(self.end_point.y - self.start_point.y, self.end_point.x - self.start_point.x)
        wedge_angles = [angle * level for level in self.levels]
        return wedge_angles

    def get_adjusters(self):
        return [self.start_point, self.end_point]

class Pitchfan:
    def __init__(self, start_point, middle_point, end_point):
        self.start_point = start_point
        self.middle_point = middle_point
        self.end_point = end_point
        self.levels = [0, 0.236, 0.382, 0.5, 0.618, 0.786, 1]

    def calculate_fan_lines(self):
        angle1 = math.atan2(self.middle_point.y - self.start_point.y, self.middle_point.x - self.start_point.x)
        angle2 = math.atan2(self.end_point.y - self.start_point.y, self.end_point.x - self.start_point.x)
        fan_angles = [angle1 + (angle2 - angle1) * level for level in self.levels]
        return fan_angles

    def get_adjusters(self):
        return [self.start_point, self.middle_point, self.end_point]
        import math
