class ChartWidget(QWidget):
    def __init__(self, strategy=None):
        super().__init__()
        self.strategy = strategy
        # ... existing initialization code ...

    def set_strategy(self, strategy):
        """Update the current strategy"""
        self.strategy = strategy

    def update_chart(self):
        try:
            # ... existing data fetching code ...

            # Apply strategy if one is selected
            if self.strategy is not None:
                df = self.strategy.apply_strategy(df)
                
                # Plot strategy elements
                self.plot_strategy_elements(df)

            # ... rest of your existing plotting code ...

        except Exception as e:
            print(f"Error updating chart: {str(e)}")
            traceback.print_exc()

    def plot_strategy_elements(self, df):
        """Plot all strategy-related elements"""
        if isinstance(self.strategy, LiquidationStrategy):
            # Plot main bands
            self.chart.plot(df['upper'], pen=pg.mkPen(color='gray', width=1))
            self.chart.plot(df['lower'], pen=pg.mkPen(color='gray', width=1))
            
            # Plot volatility bands
            self.chart.plot(df['upperu'], pen=pg.mkPen(color=self.strategy.red_color, width=1, alpha=0.5))
            self.chart.plot(df['loweru'], pen=pg.mkPen(color=self.strategy.red_color, width=1, alpha=0.1))
            self.chart.plot(df['upperl'], pen=pg.mkPen(color=self.strategy.green_color, width=1, alpha=0.1))
            self.chart.plot(df['lowerl'], pen=pg.mkPen(color=self.strategy.green_color, width=1, alpha=0.5))

            # Plot liquidation levels
            leverages = [5, 10, 25, 50, 100]
            for lev in leverages:
                liq_key_long = f'long_liq_{lev}x'
                liq_key_short = f'short_liq_{lev}x'
                
                if liq_key_long in df.columns:
                    self.chart.plot(
                        df[liq_key_long].dropna(),
                        pen=pg.mkPen(color=self.strategy.col_dn, width=self.strategy.lines_width, alpha=0.9-lev/100)
                    )
                    self.chart.plot(
                        df[liq_key_short].dropna(),
                        pen=pg.mkPen(color=self.strategy.col_up, width=self.strategy.lines_width, alpha=0.9-lev/100)
                    )

            # Plot signals
            for i in range(len(df)):
                if df['bullish_continuation'].iloc[i]:
                    arrow = pg.ArrowItem(pos=(i, df['Low'].iloc[i]), angle=-90, brush=self.strategy.green_color)
                    self.chart.addItem(arrow)
                
                if df['bearish_continuation'].iloc[i]:
                    arrow = pg.ArrowItem(pos=(i, df['High'].iloc[i]), angle=90, brush=self.strategy.red_color)
                    self.chart.addItem(arrow) 