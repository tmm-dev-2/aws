import pygame
from .settings import drawing_settings

class Brush:
    def __init__(self):
        self.points = []

    def add_point(self, point):
        self.points.append(point)

    def draw(self, surface):
        if len(self.points) > 1:
            pygame.draw.lines(
                surface, 
                drawing_settings.color, 
                False, 
                self.points, 
                drawing_settings.line_thickness
            )

class Highlighter(Brush):
    def __init__(self):
        super().__init__()

    def draw(self, surface):
        if len(self.points) > 1:
            line_surface = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
            color = drawing_settings.color + (int(drawing_settings.transparency * 255),)
            pygame.draw.lines(
                line_surface, 
                color, 
                False, 
                self.points, 
                drawing_settings.line_thickness
            )
            surface.blit(line_surface, (0, 0))

class Brushes:
    def __init__(self):
        self.brushes = {}
        self.current_brush = None
        self.current_highlighter = None

    def create_brush(self):
        brush = Brush()
        self.brushes['brush'] = brush
        self.current_brush = brush

    def create_highlighter(self):
        highlighter = Highlighter()
        self.brushes['highlighter'] = highlighter
        self.current_highlighter = highlighter

    def add_point(self, point):
        if self.current_brush:
            self.current_brush.add_point(point)
        if self.current_highlighter:
            self.current_highlighter.add_point(point)

    def draw(self, surface):
        if self.current_brush:
            self.current_brush.draw(surface)
        if self.current_highlighter:
            self.current_highlighter.draw(surface)

    def clear_points(self):
        if self.current_brush:
            self.current_brush.points = []
        if self.current_highlighter:
            self.current_highlighter.points = []