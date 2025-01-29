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
