class TopPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(8)

        # Symbol input field (black background)
        self.symbol_input = QLineEdit()
        self.symbol_input.setPlaceholderText("Enter symbol...")
        self.symbol_input.setStyleSheet("""
            QLineEdit {
                background-color: #131722;
                color: white;
                border: 1px solid #2a2e39;
                border-radius: 4px;
                padding: 5px 10px;
                min-width: 200px;
                height: 24px;
            }
            QLineEdit::placeholder {
                color: #666;
            }
        """)

        dropdown_style = """
            QComboBox {
                background-color: #2a2e39;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 5px 10px;
                height: 24px;
            }
            QComboBox:hover {
                background-color: #363c4e;
            }
            QComboBox QAbstractItemView {
                background-color: #2a2e39;
                color: white;
                selection-background-color: #363c4e;
                selection-color: white;
                border: none;
            }
        """

        # Timeframes Dropdown
        self.timeframe_combo = QComboBox()
        self.timeframe_combo.addItems(['1d', '1h', '4h', '1w', '1m', '5m', '15m', '30m', '1M'])
        self.timeframe_combo.setStyleSheet(dropdown_style)
        self.timeframe_combo.setFixedWidth(60)

        # Strategy Dropdown
        self.strategy_combo = QComboBox()
        self.strategy_combo.addItems(['None', 'Liquidations & Schaff Trend Cycle P1'])
        self.strategy_combo.setStyleSheet(dropdown_style)
        self.strategy_combo.setFixedWidth(200)

        # Add components to layout
        layout.addWidget(self.symbol_input)
        layout.addWidget(self.timeframe_combo)
        layout.addWidget(self.strategy_combo)
        layout.addStretch()
        self.setLayout(layout)

        # Set panel background
        self.setStyleSheet("""
            QWidget {
                background-color: #131722;
            }
        """)

    def get_symbol(self):
        return self.symbol_input.text()

    def get_timeframe(self):
        return self.timeframe_combo.currentText()

    def get_strategy(self):
        return self.strategy_combo.currentText()

    def connect_signals(self, on_symbol_changed, on_timeframe_changed, on_strategy_changed):
        self.symbol_input.returnPressed.connect(
            lambda: on_symbol_changed(self.get_symbol()))
        self.timeframe_combo.currentTextChanged.connect(on_timeframe_changed)
        self.strategy_combo.currentTextChanged.connect(on_strategy_changed) 