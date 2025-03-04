import unittest
import numpy as np
from risk import RiskEngine

class TestRiskEngine(unittest.TestCase):
    def setUp(self):
        self.risk_engine = RiskEngine()
        
        # Sample data for testing
        self.returns = np.array([0.01, -0.02, 0.03, -0.01, 0.02])
        self.positions = {
            'AAPL': np.array([0.01, 0.02, -0.01, 0.03]),
            'GOOGL': np.array([0.02, -0.01, 0.01, 0.02]),
            'MSFT': np.array([0.01, 0.01, 0.02, -0.01])
        }
        
    def test_position_sizing(self):
        size = self.risk_engine.calculate_position_size(
            capital=100000,
            risk_per_trade=0.02,
            stop_loss=95,
            entry_price=100
        )
        self.assertTrue(size > 0)
        self.assertTrue(size <= 100000 * self.risk_engine.risk_limits['max_position_size'])

    def test_risk_metrics(self):
        var = self.risk_engine.value_at_risk(self.returns)
        sharpe = self.risk_engine.sharpe_ratio(self.returns)
        max_dd = self.risk_engine.max_drawdown(self.returns)
        
        self.assertTrue(-1 <= var <= 0)
        self.assertTrue(isinstance(sharpe, float))
        self.assertTrue(0 <= max_dd <= 1)

    def test_portfolio_risk(self):
        weights = {'AAPL': 0.4, 'GOOGL': 0.3, 'MSFT': 0.3}
        port_var = self.risk_engine.portfolio_var(self.positions, weights)
        corr_risk = self.risk_engine.correlation_risk(self.positions)
        
        self.assertTrue(-1 <= port_var <= 0)
        self.assertTrue(isinstance(corr_risk, np.ndarray))

    def test_max_limits(self):
        max_pos_size = self.risk_engine.calculate_max_position_size(100000, 100)
        max_port_risk = self.risk_engine.calculate_max_portfolio_risk(100000, {'AAPL': 20000, 'GOOGL': 30000})
        max_corr = self.risk_engine.calculate_max_correlation(self.positions)
        max_lev = self.risk_engine.calculate_max_leverage(150000, 100000)
        max_conc = self.risk_engine.calculate_max_concentration(25000, 100000)
        
        self.assertTrue(max_pos_size > 0)
        self.assertTrue(0 <= max_port_risk <= 1)
        self.assertTrue(-1 <= max_corr <= 1)
        self.assertTrue(max_lev >= 1)
        self.assertTrue(0 <= max_conc <= 1)

    def test_risk_limits_check(self):
        limits = self.risk_engine.check_limits(
            position_size=0.05,
            portfolio_risk=0.15,
            correlation=0.6,
            leverage=1.5,
            concentration=0.2
        )
        
        self.assertTrue(all(isinstance(v, bool) for v in limits.values()))

def run_risk_tests():
    print("Starting Risk Management Tests...")
    unittest.main(argv=[''], verbosity=2, exit=False)

if __name__ == "__main__":
    run_risk_tests()
