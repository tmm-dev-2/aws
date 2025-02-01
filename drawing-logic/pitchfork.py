import math

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

