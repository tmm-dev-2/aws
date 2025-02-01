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