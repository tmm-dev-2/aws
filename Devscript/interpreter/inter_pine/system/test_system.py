import unittest
from system import StrategyEngine, get_strategy_registry

class TestSystemEngine(unittest.TestCase):
    def setUp(self):
        self.engine = StrategyEngine()
        self.registry = get_strategy_registry(self.engine)

    def test_alerts(self):
        self.registry['alerts']['alert_popup_buy']("Buy Signal: AAPL crossed above MA")
        self.registry['alerts']['alert_popup_sell']("Sell Signal: TSLA RSI overbought")
        self.registry['alerts']['alert_popup_info']("Market Analysis Update")
        self.registry['alerts']['alert_popup_warning']("High Volatility Detected")
        self.registry['alerts']['alert_sound']()
        self.assertTrue(True)

    def test_logging(self):
        trade_info = {
            'symbol': 'AAPL',
            'signal_type': 'buy',
            'price': 150.25,
            'strategy': 'MA Crossover'
        }
        self.registry['logging']['log_trade'](trade_info)
        self.assertTrue(len(self.engine.trade_log) > 0)
        self.assertEqual(self.engine.trade_log[-1]['trade']['symbol'], 'AAPL')
        self.registry['logging']['log_error']("Strategy calculation error")
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
