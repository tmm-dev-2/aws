import unittest
from renderer import RenderEngine, ChartEngine, DrawingEngine, IndicatorEngine, VisualElement

class TestRenderEngine(unittest.TestCase):
    def setUp(self):
        self.render_engine = RenderEngine()

    def test_chart_styles(self):
        # Test chart style setting
        element_id = "test_chart"
        self.render_engine.chart_engine.elements[element_id] = VisualElement(
            id=element_id,
            type='chart',
            style='line',
            color='#000000',
            data={},
            properties={}
        )
        
        self.render_engine.get_registry()['style_candlesticks'](element_id)
        self.assertEqual(self.render_engine.chart_engine.elements[element_id].style, 'candlesticks')

    def test_colors(self):
        # Test color functions
        red_color = self.render_engine.get_registry()['color_red']()
        self.assertEqual(red_color.lower(), '#ff0000')
        
        # Test gradient color
        gradient = self.render_engine.get_registry()['color_from_gradient']('#FF0000', '#0000FF', 0.5)
        self.assertEqual(gradient.lower(), '#7f007f')

    def test_drawing_tools(self):
        # Test line creation and modification
        line_id = self.render_engine.get_registry()['line_new'](0, 0, 100, 100)
        self.assertIn(line_id, self.render_engine.drawing_engine.elements)
        
        # Test line color setting
        self.render_engine.get_registry()['line_set_color'](line_id, '#FF0000')
        self.assertEqual(self.render_engine.drawing_engine.elements[line_id].color, '#FF0000')
        
        # Test box creation
        box_id = self.render_engine.get_registry()['box_new'](0, 0, 50, 50)
        self.assertIn(box_id, self.render_engine.drawing_engine.elements)

    def test_indicator_functions(self):
        # Test indicator settings
        indicator_id = "test_indicator"
        self.render_engine.indicator_engine.indicators[indicator_id] = VisualElement(
            id=indicator_id,
            type='indicator',
            style='line',
            color='#000000',
            data={},
            properties={}
        )
        
        self.render_engine.get_registry()['indicator_color'](indicator_id, '#00FF00')
        self.assertEqual(self.render_engine.indicator_engine.indicators[indicator_id].color, '#00FF00')

def run_renderer_tests():
    print("Starting Renderer Tests...")
    unittest.main(argv=[''], verbosity=2, exit=False)

if __name__ == "__main__":
    run_renderer_tests()
