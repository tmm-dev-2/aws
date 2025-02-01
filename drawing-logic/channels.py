import math

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