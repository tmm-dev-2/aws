import math

class VerticalLine:
    """Represents a vertical line that extends infinitely in both directions."""
    def __init__(self, x):
        self.x = x

    def draw(self):
        print(f"Drawing vertical line at x = {self.x}")

    def move_x(self, new_x):
        self.x = new_x

class CrossLine:
    """Represents a cross line that extends infinitely in all directions."""
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        print(f"Drawing cross line at ({self.x}, {self.y})")

    def move_x(self, new_x):
        self.x = new_x

    def move_y(self, new_y):
        self.y = new_y

class ParallelChannel:
    def __init__(self, top_left_x, top_left_y, top_right_x, top_right_y, bottom_left_x, bottom_left_y, bottom_right_x, bottom_right_y):
        self.top_left_x = top_left_x
        self.top_left_y = top_left_y
        self.top_right_x = top_right_x
        self.top_right_y = top_right_y
        self.bottom_left_x = bottom_left_x
        self.bottom_left_y = bottom_left_y
        self.bottom_right_x = bottom_right_x
        self.bottom_right_y = bottom_right_y

    def draw(self):
        return f"M{self.top_left_x},{self.top_left_y} L{self.top_right_x},{self.top_right_y} L{self.bottom_right_x},{self.bottom_right_y} L{self.bottom_left_x},{self.bottom_left_y} Z"

    def move_top_left(self, new_x, new_y):
        self.top_left_x = new_x
        self.top_left_y = new_y

    def move_top_right(self, new_x, new_y):
        self.top_right_x = new_x
        self.top_right_y = new_y

    def move_bottom_left(self, new_x, new_y):
        self.bottom_left_x = new_x
        self.bottom_left_y = new_y

    def move_bottom_right(self, new_x, new_y):
        self.bottom_right_x = new_x
        self.bottom_right_y = new_y
    
    def move_horizontal(self, delta_x):
        self.top_left_x += delta_x
        self.top_right_x += delta_x
        self.bottom_left_x += delta_x
        self.bottom_right_x += delta_x

    def move_vertical(self, delta_y):
        self.top_left_y += delta_y
        self.top_right_y += delta_y
        self.bottom_left_y += delta_y
        self.bottom_right_y += delta_y
    
    def adjust_angle(self, new_top_right_x, new_top_right_y):
        # Adjust the angle by moving the top right point, keeping the top left point fixed
        self.top_right_x = new_top_right_x
        self.top_right_y = new_top_right_y
        
        # Calculate the angle of the top line
        top_dx = self.top_right_x - self.top_left_x
        top_dy = self.top_right_y - self.top_left_y
        top_angle = math.atan2(top_dy, top_dx)
        
        # Calculate the length of the top line
        top_length = math.sqrt(top_dx**2 + top_dy**2)
        
        # Calculate the new bottom right point based on the new angle and length
        bottom_dx = self.bottom_right_x - self.bottom_left_x
        bottom_dy = self.bottom_right_y - self.bottom_left_y
        bottom_length = math.sqrt(bottom_dx**2 + bottom_dy**2)
        
        self.bottom_right_x = self.bottom_left_x + top_length * math.cos(top_angle)
        self.bottom_right_y = self.bottom_left_y + top_length * math.sin(top_angle)


class FlatTopBottomChannel:
    def __init__(self, top_left_x, top_left_y, top_right_x, top_right_y, bottom_left_x, bottom_left_y, bottom_right_x, bottom_right_y):
        self.top_left_x = top_left_x
        self.top_left_y = top_left_y
        self.top_right_x = top_right_x
        self.top_right_y = top_right_y
        self.bottom_left_x = bottom_left_x
        self.bottom_left_y = bottom_left_y
        self.bottom_right_x = bottom_right_x
        self.bottom_right_y = bottom_right_y

    def draw(self):
        return f"M{self.top_left_x},{self.top_left_y} L{self.top_right_x},{self.top_right_y} L{self.bottom_right_x},{self.bottom_right_y} L{self.bottom_left_x},{self.bottom_left_y} Z"

    def move_top_left(self, new_x, new_y):
        self.top_left_x = new_x
        self.top_left_y = new_y

    def move_top_right(self, new_x, new_y):
        self.top_right_x = new_x
        self.top_right_y = new_y
    
    def move_bottom_left(self, new_x, new_y):
        self.bottom_left_x = new_x
        self.bottom_left_y = new_y

    def move_bottom_right(self, new_x, new_y):
        self.bottom_right_x = new_x
        self.bottom_right_y = new_y
    
    def adjust_height(self, new_top_left_y, new_top_right_y):
        self.top_left_y = new_top_left_y
        self.top_right_y = new_top_right_y

    def adjust_width(self, new_top_left_x, new_top_right_x):
        self.top_left_x = new_top_left_x
        self.top_right_x = new_top_right_x
    
    def adjust_bottom_shape(self, new_bottom_right_x, new_bottom_right_y):
        # Adjust the bottom shape by moving the bottom right point, pivoting on the bottom left point
        self.bottom_right_x = new_bottom_right_x
        self.bottom_right_y = new_bottom_right_y

class DisjointedChannel:
    def __init__(self, top_left_x, top_left_y, top_right_x, top_right_y, bottom_left_x, bottom_left_y, bottom_right_x, bottom_right_y):
        self.top_left_x = top_left_x
        self.top_left_y = top_left_y
        self.top_right_x = top_right_x
        self.top_right_y = top_right_y
        self.bottom_left_x = bottom_left_x
        self.bottom_left_y = bottom_left_y
        self.bottom_right_x = bottom_right_x
        self.bottom_right_y = bottom_right_y

    def draw(self):
        return f"M{self.top_left_x},{self.top_left_y} L{self.top_right_x},{self.top_right_y} L{self.bottom_right_x},{self.bottom_right_y} L{self.bottom_left_x},{self.bottom_left_y} Z"

    def move_top_left(self, new_x, new_y):
        self.top_left_x = new_x
        self.top_left_y = new_y

    def move_top_right(self, new_x, new_y):
        self.top_right_x = new_x
        self.top_right_y = new_y

    def move_bottom_left(self, new_x, new_y):
        self.bottom_left_x = new_x
        self.bottom_left_y = new_y

    def move_bottom_right(self, new_x, new_y):
        self.bottom_right_x = new_x
        self.bottom_right_y = new_y
    
    def move_horizontal(self, delta_x):
        self.top_left_x += delta_x
        self.top_right_x += delta_x
        self.bottom_left_x += delta_x
        self.bottom_right_x += delta_x

    def move_vertical(self, delta_y):
        self.top_left_y += delta_y
        self.top_right_y += delta_y
        self.bottom_left_y += delta_y
        self.bottom_right_y += delta_y

class Pitchfork:
    def __init__(self, start_x, start_y, middle_x, middle_y, end_x, end_y):
        self.start_x = start_x
        self.start_y = start_y
        self.middle_x = middle_x
        self.middle_y = middle_y
        self.end_x = end_x
        self.end_y = end_y
        self.lines = self._calculate_lines()

    def _calculate_lines(self):
        # Calculate the lines of the pitchfork
        start_x, start_y = self.start_x, self.start_y
        middle_x, middle_y = self.middle_x, self.middle_y
        end_x, end_y = self.end_x, self.end_y

        lines = []
        lines.append(TrendLine(start_x, start_y, middle_x, middle_y))
        
        # Calculate the median line
        median_x = (start_x + end_x) / 2
        median_y = (start_y + end_y) / 2
        lines.append(TrendLine(middle_x, middle_y, median_x, median_y))

        # Calculate the top and bottom lines
        dx = end_x - start_x
        dy = end_y - start_y
        
        lines.append(TrendLine(middle_x + dx, middle_y + dy, end_x, end_y))
        
        return lines

    def draw(self):
        # Draw all the lines of the pitchfork
        path = ""
        for line in self.lines:
            path += f"M{line.start_x},{line.start_y} L{line.end_x},{line.end_y} "
        return path

    def move_start(self, new_x, new_y):
        # Move the start point of the pitchfork
        dx = new_x - self.start_x
        dy = new_y - self.start_y
        self.start_x = new_x
        self.start_y = new_y
        self.move_all(dx, dy)

    def move_middle(self, new_x, new_y):
        # Move the middle point of the pitchfork
        dx = new_x - self.middle_x
        dy = new_y - self.middle_y
        self.middle_x = new_x
        self.middle_y = new_y
        self.move_all(dx, dy)

    def move_end(self, new_x, new_y):
        # Move the end point of the pitchfork
        dx = new_x - self.end_x
        dy = new_y - self.end_y
        self.end_x = new_x
        self.end_y = new_y
        self.move_all(dx, dy)

    def move_all(self, dx, dy):
        # Move all the lines of the pitchfork
        for line in self.lines:
            line.start_x += dx
            line.start_y += dy
            line.end_x += dx
            line.end_y += dy

    def adjust_angle(self, new_end_x, new_end_y):
        # Adjust the angle of the entire pitchfork
        
        # Calculate the angle of the base line
        dx = self.end_x - self.start_x
        dy = self.end_y - self.start_y
        base_angle = math.atan2(dy, dx)
        
        # Calculate the length of the base line
        base_length = math.sqrt(dx**2 + dy**2)
        
        # Calculate the new angle
        new_dx = new_end_x - self.start_x
        new_dy = new_end_y - self.start_y
        new_angle = math.atan2(new_dy, new_dx)
        
        # Calculate the rotation angle
        rotation_angle = new_angle - base_angle
        
        # Rotate the middle and end points
        self.middle_x, self.middle_y = self._rotate_point(self.start_x, self.start_y, self.middle_x, self.middle_y, rotation_angle)
        self.end_x, self.end_y = self._rotate_point(self.start_x, self.start_y, new_end_x, new_end_y, rotation_angle)
        
        # Recalculate the lines
        self.lines = self._calculate_lines()

    def _rotate_point(self, center_x, center_y, x, y, angle):
        # Rotate a point around a center
        dx = x - center_x
        dy = y - center_y
        new_x = center_x + dx * math.cos(angle) - dy * math.sin(angle)
        new_y = center_y + dx * math.sin(angle) + dy * math.cos(angle)
        return new_x, new_y

class NormalPitchfork(Pitchfork):
    def __init__(self, start_x, start_y, middle_x, middle_y, end_x, end_y):
        super().__init__(start_x, start_y, middle_x, middle_y, end_x, end_y)

class SchiffPitchfork(Pitchfork):
    def __init__(self, start_x, start_y, middle_x, middle_y, end_x, end_y):
        super().__init__(start_x, start_y, middle_x, middle_y, end_x, end_y)

    def _calculate_lines(self):
        # Calculate the lines of the schiff pitchfork
        start_x, start_y = self.start_x, self.start_y
        middle_x, middle_y = self.middle_x, self.middle_y
        end_x, end_y = self.end_x, self.end_y

        lines = []
        lines.append(TrendLine(start_x, start_y, middle_x, middle_y))
        
        # Calculate the median line
        median_x = (start_x + middle_x) / 2
        median_y = (start_y + middle_y) / 2
        lines.append(TrendLine(median_x, median_y, end_x, end_y))

        # Calculate the top and bottom lines
        dx = end_x - start_x
        dy = end_y - start_y
        
        lines.append(TrendLine(middle_x + dx, middle_y + dy, end_x, end_y))
        
        return lines

class ModifiedPitchfork(Pitchfork):
    def __init__(self, start_x, start_y, middle_x, middle_y, end_x, end_y):
        super().__init__(start_x, start_y, middle_x, middle_y, end_x, end_y)

    def _calculate_lines(self):
        # Calculate the lines of the modified pitchfork
        start_x, start_y = self.start_x, self.start_y
        middle_x, middle_y = self.middle_x, self.middle_y
        end_x, end_y = self.end_x, self.end_y

        lines = []
        lines.append(TrendLine(start_x, start_y, middle_x, middle_y))
        
        # Calculate the median line
        median_x = (middle_x + end_x) / 2
        median_y = (middle_y + end_y) / 2
        lines.append(TrendLine(middle_x, middle_y, median_x, median_y))

        # Calculate the top and bottom lines
        dx = end_x - start_x
        dy = end_y - start_y
        
        lines.append(TrendLine(middle_x + dx, middle_y + dy, end_x, end_y))
        
        return lines

class InsidePitchfork(Pitchfork):
    def __init__(self, start_x, start_y, middle_x, middle_y, end_x, end_y):
        super().__init__(start_x, start_y, middle_x, middle_y, end_x, end_y)

    def _calculate_lines(self):
        # Calculate the lines of the inside pitchfork
        start_x, start_y = self.start_x, self.start_y
        middle_x, middle_y = self.middle_x, self.middle_y
        end_x, end_y = self.end_x, self.end_y

        lines = []
        lines.append(TrendLine(start_x, start_y, middle_x, middle_y))
        
        # Calculate the median line
        median_x = (start_x + end_x) / 2
        median_y = (start_y + end_y) / 2
        lines.append(TrendLine(middle_x, middle_y, median_x, median_y))

        # Calculate the top and bottom lines
        dx = end_x - start_x
        dy = end_y - start_y
        
        lines.append(TrendLine(middle_x - dx, middle_y - dy, end_x, end_y))
        
        return lines

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

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class GannBox:
    def __init__(self, start_point, end_point):
        self.start_point = start_point
        self.end_point = end_point
        self.adjusters = [start_point, end_point]

    def get_lines(self):
        x1, y1 = self.start_point.x, self.start_point.y
        x2, y2 = self.end_point.x, self.end_point.y

        lines = []

        # Box lines
        lines.append(((x1, y1), (x2, y1)))
        lines.append(((x2, y1), (x2, y2)))
        lines.append(((x2, y2), (x1, y2)))
        lines.append(((x1, y2), (x1, y1)))

        # Diagonal lines
        lines.append(((x1, y1), (x2, y2)))
        lines.append(((x1, y2), (x2, y1)))

        # Middle lines
        mid_x = (x1 + x2) / 2
        mid_y = (y1 + y2) / 2
        lines.append(((mid_x, y1), (mid_x, y2)))
        lines.append(((x1, mid_y), (x2, mid_y)))

        return lines

class GannSquareFixed:
    def __init__(self, start_point, end_point):
        self.start_point = start_point
        self.end_point = end_point
        self.adjusters = [start_point, end_point]

    def get_lines(self):
        x1, y1 = self.start_point.x, self.start_point.y
        x2, y2 = self.end_point.x, self.end_point.y

        side = min(abs(x2 - x1), abs(y2 - y1))

        if x2 > x1:
            x2 = x1 + side
        else:
            x2 = x1 - side
        if y2 > y1:
            y2 = y1 + side
        else:
            y2 = y1 - side

        lines = []

        # Box lines
        lines.append(((x1, y1), (x2, y1)))
        lines.append(((x2, y1), (x2, y2)))
        lines.append(((x2, y2), (x1, y2)))
        lines.append(((x1, y2), (x1, y1)))

        return lines

class GannSquare:
    def __init__(self, start_point, end_point):
        self.start_point = start_point
        self.end_point = end_point
        self.adjusters = [start_point, end_point]

    def get_lines(self):
        x1, y1 = self.start_point.x, self.start_point.y
        x2, y2 = self.end_point.x, self.end_point.y

        lines = []

        # Box lines
        lines.append(((x1, y1), (x2, y1)))
        lines.append(((x2, y1), (x2, y2)))
        lines.append(((x2, y2), (x1, y2)))
        lines.append(((x1, y2), (x1, y1)))

        return lines

class GannFan:
    def __init__(self, start_point, end_point):
        self.start_point = start_point
        self.end_point = end_point
        self.adjusters = [start_point, end_point]

    def get_lines(self):
        x1, y1 = self.start_point.x, self.start_point.y
        x2, y2 = self.end_point.x, self.end_point.y

        lines = []
        
        angles = [0, 1/8, 2/8, 3/8, 4/8, 5/8, 6/8, 7/8, 1]
        
        dx = x2 - x1
        dy = y2 - y1
        
        for angle in angles:
            
            angle_rad = angle * math.pi / 2
            
            
            new_dx = dx * math.cos(angle_rad) - dy * math.sin(angle_rad)
            new_dy = dx * math.sin(angle_rad) + dy * math.cos(angle_rad)
            
            lines.append(((x1, y1), (x1 + new_dx, y1 + new_dy)))

        return lines
    


import math

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class AdjustmentPointer:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class XABCDPattern:
    def __init__(self, x, a, b, c, d):
        self.x = x
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.adjustment_pointers = [
            AdjustmentPointer(x.x, x.y),
            AdjustmentPointer(a.x, a.y),
            AdjustmentPointer(b.x, b.y),
            AdjustmentPointer(c.x, c.y),
            AdjustmentPointer(d.x, d.y),
        ]
        return

    def is_valid(self):
        xa = math.sqrt((self.a.x - self.x.x)**2 + (self.a.y - self.x.y)**2)
        ab = math.sqrt((self.b.x - self.a.x)**2 + (self.b.y - self.a.y)**2)
        bc = math.sqrt((self.c.x - self.b.x)**2 + (self.c.y - self.b.y)**2)
        cd = math.sqrt((self.d.x - self.c.x)**2 + (self.d.y - self.c.y)**2)

        # Check if AB is a retracement of XA (between 0.382 and 0.886)
        ab_retracement = ab / xa
        if not (0.382 <= ab_retracement <= 0.886):
            return False

        # Check if BC is a retracement of AB (between 0.382 and 0.886)
        bc_retracement = bc / ab
        if not (0.382 <= bc_retracement <= 0.886):
            return False

        # Check if CD is an extension of BC (between 1.272 and 1.618)
        cd_extension = cd / bc
        if not (1.272 <= cd_extension <= 1.618):
            return False

        return True

class CypherPattern:
    def __init__(self, x, a, b, c, d):
        self.x = x
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.adjustment_pointers = [
            AdjustmentPointer(x.x, x.y),
            AdjustmentPointer(a.x, a.y),
            AdjustmentPointer(b.x, b.y),
            AdjustmentPointer(c.x, c.y),
            AdjustmentPointer(d.x, d.y),
        ]
        return

class HeadAndShouldersPattern:
    def __init__(self, left_shoulder, head, right_shoulder, neckline_start, neckline_end):
        self.left_shoulder = left_shoulder
        self.head = head
        self.right_shoulder = right_shoulder
        self.neckline_start = neckline_start
        self.neckline_end = neckline_end
        self.adjustment_pointers = [
            AdjustmentPointer(left_shoulder.x, left_shoulder.y),
            AdjustmentPointer(head.x, head.y),
            AdjustmentPointer(right_shoulder.x, right_shoulder.y),
            AdjustmentPointer(neckline_start.x, neckline_start.y),
            AdjustmentPointer(neckline_end.x, neckline_end.y),
        ]
        return

class ABCDPattern:
    def __init__(self, a, b, c, d):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.adjustment_pointers = [
            AdjustmentPointer(a.x, a.y),
            AdjustmentPointer(b.x, b.y),
            AdjustmentPointer(c.x, c.y),
            AdjustmentPointer(d.x, d.y),
        ]
        return

class TrianglePattern:
    def __init__(self, start, top, bottom):
        self.start = start
        self.top = top
        self.bottom = bottom
        self.adjustment_pointers = [
            AdjustmentPointer(start.x, start.y),
            AdjustmentPointer(top.x, top.y),
             AdjustmentPointer(bottom.x, bottom.y),
        ]
        return

class ThreeDrivesPattern:
    def __init__(self, start, drive1, drive2, drive3, end):
        self.start = start
        self.drive1 = drive1
        self.drive2 = drive2
        self.drive3 = drive3
        self.end = end
        self.adjustment_pointers = [
            AdjustmentPointer(start.x, start.y),
            AdjustmentPointer(drive1.x, drive1.y),
            AdjustmentPointer(drive2.x, drive2.y),
            AdjustmentPointer(drive3.x, drive3.y),
            AdjustmentPointer(end.x, end.y),
        ]
        return

import math

class TrendLine:
    def __init__(self, start_point, end_point):
        self.start_point = start_point
        self.end_point = end_point

    def adjust_start_point(self, new_start_point):
        self.start_point = new_start_point

    def adjust_end_point(self, new_end_point):
        self.end_point = new_end_point

class Ray:
    def __init__(self, start_point, end_point):
        self.start_point = start_point
        self.end_point = end_point

    def adjust_start_point(self, new_start_point):
        self.start_point = new_start_point

    def adjust_end_point(self, new_end_point):
        self.end_point = new_end_point

class InfoRay:
    def __init__(self, start_point, end_point):
        self.start_point = start_point
        self.end_point = end_point

    def adjust_start_point(self, new_start_point):
        self.start_point = new_start_point

    def adjust_end_point(self, new_end_point):
        self.end_point = new_end_point

class ExtendedLine:
    def __init__(self, start_point, end_point):
        self.start_point = start_point
        self.end_point = end_point
        self.calculate_angle()

    def calculate_angle(self):
        x1, y1 = self.start_point
        x2, y2 = self.end_point
        self.angle_rad = math.atan2(y2 - y1, x2 - x1)

    def adjust_start_point(self, new_start_point):
        self.start_point = new_start_point
        self.calculate_angle()

    def adjust_end_point(self, new_end_point):
        self.end_point = new_end_point
        self.calculate_angle()

    def get_extended_points(self, x_range=(-10000, 10000)):
        x1, y1 = self.start_point
        start_x = x_range[0]
        end_x = x_range[1]
        start_y = y1 + (start_x - x1) * math.tan(self.angle_rad)
        end_y = y1 + (end_x - x1) * math.tan(self.angle_rad)
        return (start_x, start_y), (end_x, end_y)


class TrendAngle:
    def __init__(self, start_point, end_point):
        self.start_point = start_point
        self.end_point = end_point

    def adjust_start_point(self, new_start_point):
        self.start_point = new_start_point

    def adjust_end_point(self, new_end_point):
        self.end_point = new_end_point

    def calculate_angle(self):
        x1, y1 = self.start_point
        x2, y2 = self.end_point
        angle_rad = math.atan2(y2 - y1, x2 - x1)
        angle_deg = math.degrees(angle_rad)
        return angle_deg

    def get_angle_text(self):
        angle = self.calculate_angle()
        return f"{angle:.2f}°"

class HorizontalLine:
    def __init__(self, y_value):
        self.y_value = y_value

    def adjust_y_value(self, new_y_value):
        self.y_value = new_y_value

    def get_extended_points(self, x_range=(-10000, 10000)):
        start_x = x_range[0]
        end_x = x_range[1]
        return (start_x, self.y_value), (end_x, self.y_value)

class HorizontalRay:
    def __init__(self, start_point, end_point):
        self.start_point = start_point
        self.end_point = end_point

    def adjust_start_point(self, new_start_point):
        self.start_point = new_start_point

    def adjust_end_point(self, new_end_point):
        self.end_point = new_end_point

class VerticalLine:
    def __init__(self, x_value):
        self.x_value = x_value

    def adjust_x_value(self, new_x_value):
        self.x_value = new_x_value

    def get_extended_points(self, y_range=(-10000, 10000)):
        start_y = y_range[0]
        end_y = y_range[1]
        return (self.x_value, start_y), (self.x_value, end_y)
