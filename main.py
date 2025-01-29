from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from top_panel import TopPanel
from chart_widget import ChartWidget
from strategies.liquidations_schaff_trend_cycle_p1 import LiquidationStrategy

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Create central widget and layout
        self.central_widget = QWidget()
        self.layout = QVBoxLayout()
        
        # Initialize top panel
        self.top_panel = TopPanel()
        self.layout.addWidget(self.top_panel)
        
        # Initialize chart widget
        self.chart_widget = ChartWidget()
        self.layout.addWidget(self.chart_widget)
        
        # Set up central widget
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)
        
        # Initialize strategies dictionary
        self.strategies = {
            "None": None,
            "Liquidations & Schaff Trend Cycle P1": LiquidationStrategy()
        }
        self.current_strategy = None

        # Connect top panel signals with all three callbacks
        self.top_panel.connect_signals(
            self.on_symbol_changed,
            self.on_timeframe_changed,
            self.on_strategy_changed
        )

    def on_symbol_changed(self, symbol):
        # Implement symbol change handling
        pass

    def on_timeframe_changed(self, timeframe):
        self.chart_widget.set_timeframe(timeframe)
        self.chart_widget.update_chart()

    def on_strategy_changed(self, strategy_name):
        if strategy_name != "None":
            self.current_strategy = self.strategies.get(strategy_name)
            self.chart_widget.set_strategy(self.current_strategy)
            self.chart_widget.update_chart()
        else:
            self.current_strategy = None
            self.chart_widget.set_strategy(None)
            self.chart_widget.update_chart() 