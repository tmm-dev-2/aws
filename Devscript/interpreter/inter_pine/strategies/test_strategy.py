from engine import StrategySyntax
import unittest
from datetime import datetime

class TestStrategySystem(unittest.TestCase):
    def setUp(self):
        self.strategy = StrategySyntax()

    def test_basic_long_trade(self):
        # Enter long position
        entry_price = 100.0
        qty = 1.0
        self.strategy.execute('strategy_entry_long', entry_price, qty, "Test Long")
        
        # Verify position details
        self.assertEqual(self.strategy.execute('strategy_position_size'), qty)
        self.assertEqual(self.strategy.execute('strategy_position_entry_price'), entry_price)
        self.assertEqual(self.strategy.execute('strategy_position_entry_name'), "Test Long")
        
        # Exit with profit
        exit_price = 110.0
        self.strategy.execute('strategy_exit', exit_price)
        
        # Verify trade results
        metrics = self.strategy.strategy_engine.performance_engine.get_trade_metrics()
        self.assertEqual(metrics['total_trades'], 1)
        self.assertEqual(metrics['net_profit'], 10.0)
        self.assertEqual(metrics['win_rate'], 100.0)

    def test_basic_short_trade(self):
        # Enter short position
        entry_price = 100.0
        qty = 1.0
        self.strategy.execute('strategy_entry_short', entry_price, qty, "Test Short")
        
        # Exit with profit
        exit_price = 90.0
        self.strategy.execute('strategy_exit', exit_price)
        
        metrics = self.strategy.strategy_engine.performance_engine.get_trade_metrics()
        self.assertEqual(metrics['total_trades'], 1)
        self.assertEqual(metrics['net_profit'], 10.0)

    def test_risk_management(self):
        # Set risk limits
        self.strategy.execute('strategy_risk_max_position', 2.0)
        self.strategy.execute('strategy_risk_max_loss', 1000.0)
        
        # Try to exceed position limit
        self.strategy.execute('strategy_entry_long', 100.0, 3.0)
        self.assertEqual(self.strategy.execute('strategy_position_size'), 0.0)

    def test_performance_metrics(self):
        # Create multiple trades
        self.strategy.execute('strategy_entry_long', 100.0, 1.0)
        self.strategy.execute('strategy_exit', 110.0)
        
        self.strategy.execute('strategy_entry_long', 100.0, 1.0)
        self.strategy.execute('strategy_exit', 90.0)
        
        metrics = self.strategy.strategy_engine.performance_engine.get_trade_metrics()
        equity_stats = self.strategy.strategy_engine.performance_engine.get_equity_stats()
        
        print("\nPerformance Test Results:")
        print(f"Total Trades: {metrics['total_trades']}")
        print(f"Win Rate: {metrics['win_rate']}%")
        print(f"Net Profit: ${metrics['net_profit']}")
        print(f"Max Drawdown: {metrics['max_drawdown']}%")
        print(f"Sharpe Ratio: {metrics['sharpe_ratio']}")
        print(f"Return %: {equity_stats['return_pct']}%")

    def test_trade_management(self):
        # Test commission calculations
        trade_value = 10000.0
        commission = self.strategy.execute('strategy_commission_amount', trade_value)
        self.assertGreater(commission, 0)
        
        # Test slippage calculations
        slippage = self.strategy.execute('strategy_slippage_amount', trade_value)
        self.assertGreater(slippage, 0)

def run_strategy_tests():
    print("Starting Strategy Engine Tests...")
    unittest.main(argv=[''], verbosity=2, exit=False)

if __name__ == "__main__":
    run_strategy_tests()
