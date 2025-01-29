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
    

