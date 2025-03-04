import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Union
from scipy import stats

class RiskEngine:
    def __init__(self):
        self.positions = {}
        self.portfolio = {}
        self.risk_limits = {
            'max_position_size': 0.1,  # 10% of capital
            'max_portfolio_risk': 0.2,  # 20% VaR
            'max_correlation': 0.7,     # 70% correlation limit
            'max_leverage': 2.0,        # 2x leverage
            'max_concentration': 0.25    # 25% max in single position
        }

    def calculate_position_size(self, 
                              capital: float,
                              risk_per_trade: float,
                              stop_loss: float,
                              entry_price: float) -> float:
        """Calculate position size based on risk parameters"""
        risk_amount = capital * risk_per_trade
        position_size = risk_amount / (entry_price - stop_loss)
        return min(position_size, capital * self.risk_limits['max_position_size'])

    def kelly_criterion(self, 
                       win_rate: float,
                       win_loss_ratio: float) -> float:
        """Calculate optimal position size using Kelly Criterion"""
        kelly_fraction = win_rate - ((1 - win_rate) / win_loss_ratio)
        return max(0, min(kelly_fraction, self.risk_limits['max_position_size']))

    def optimal_f(self, returns: np.ndarray) -> float:
        """Calculate optimal f (fraction) for position sizing"""
        positive_returns = returns[returns > 0]
        negative_returns = abs(returns[returns < 0])
        
        if len(negative_returns) == 0:
            return self.risk_limits['max_position_size']
            
        avg_win = np.mean(positive_returns)
        avg_loss = np.mean(negative_returns)
        
        optimal_fraction = avg_win / avg_loss - 1
        return min(optimal_fraction, self.risk_limits['max_position_size'])

    def fixed_fractional(self, 
                        capital: float,
                        risk_fraction: float) -> float:
        """Calculate position size using fixed fractional method"""
        return min(capital * risk_fraction, 
                  capital * self.risk_limits['max_position_size'])

    def fixed_ratio(self, 
                   capital: float,
                   delta: float,
                   target_risk: float) -> float:
        """Calculate position size using fixed ratio method"""
        contracts = np.floor(np.sqrt((2 * capital * target_risk) / delta))
        position_size = contracts * delta
        return min(position_size, capital * self.risk_limits['max_position_size'])

    def max_drawdown_limit(self, 
                          returns: np.ndarray,
                          max_allowed_dd: float) -> bool:
        """Check if drawdown limit is exceeded"""
        cumulative = (1 + returns).cumprod()
        rolling_max = np.maximum.accumulate(cumulative)
        drawdowns = (cumulative - rolling_max) / rolling_max
        return np.min(drawdowns) > -max_allowed_dd

    def value_at_risk(self, 
                     returns: np.ndarray,
                     confidence: float = 0.95) -> float:
        """Calculate Value at Risk"""
        return np.percentile(returns, (1 - confidence) * 100)

    def expected_shortfall(self, 
                         returns: np.ndarray,
                         confidence: float = 0.95) -> float:
        """Calculate Expected Shortfall (Conditional VaR)"""
        var = self.value_at_risk(returns, confidence)
        return np.mean(returns[returns <= var])

    def sharpe_ratio(self, 
                    returns: np.ndarray,
                    risk_free_rate: float = 0.02) -> float:
        """Calculate Sharpe Ratio"""
        excess_returns = returns - risk_free_rate/252  # Daily adjustment
        return np.mean(excess_returns) / np.std(excess_returns) * np.sqrt(252)

    def sortino_ratio(self, 
                     returns: np.ndarray,
                     risk_free_rate: float = 0.02) -> float:
        """Calculate Sortino Ratio"""
        excess_returns = returns - risk_free_rate/252
        downside_returns = returns[returns < 0]
        downside_std = np.std(downside_returns) if len(downside_returns) > 0 else 0
        return np.mean(excess_returns) / downside_std * np.sqrt(252)

    def calmar_ratio(self, 
                    returns: np.ndarray,
                    window: int = 252) -> float:
        """Calculate Calmar Ratio"""
        cumulative = (1 + returns).cumprod()
        rolling_max = np.maximum.accumulate(cumulative)
        drawdowns = (cumulative - rolling_max) / rolling_max
        max_dd = abs(np.min(drawdowns))
        return (np.mean(returns) * 252) / max_dd if max_dd != 0 else 0

    def max_drawdown(self, returns: np.ndarray) -> float:
        """Calculate Maximum Drawdown"""
        cumulative = (1 + returns).cumprod()
        rolling_max = np.maximum.accumulate(cumulative)
        drawdowns = (cumulative - rolling_max) / rolling_max
        return abs(np.min(drawdowns))

    def risk_of_ruin(self, 
                    win_rate: float,
                    win_loss_ratio: float,
                    risk_per_trade: float) -> float:
        """Calculate Risk of Ruin"""
        if win_loss_ratio <= 1:
            return 1.0
        return ((1 - win_rate) / win_rate) ** (1 / risk_per_trade)

    def portfolio_var(self, 
                     returns: Dict[str, np.ndarray],
                     weights: Dict[str, float],
                     confidence: float = 0.95) -> float:
        """Calculate Portfolio Value at Risk"""
        portfolio_returns = sum(returns[asset] * weight 
                              for asset, weight in weights.items())
        return self.value_at_risk(portfolio_returns, confidence)

    def correlation_risk(self, 
                        returns: Dict[str, np.ndarray]) -> np.ndarray:
        """Calculate correlation matrix of assets"""
        return np.corrcoef([returns[asset] for asset in returns])

    def beta_exposure(self, 
                     asset_returns: np.ndarray,
                     market_returns: np.ndarray) -> float:
        """Calculate beta exposure"""
        covariance = np.cov(asset_returns, market_returns)[0][1]
        market_variance = np.var(market_returns)
        return covariance / market_variance if market_variance != 0 else 0

    def sector_exposure(self, 
                       positions: Dict[str, float],
                       sectors: Dict[str, str]) -> Dict[str, float]:
        """Calculate sector exposure"""
        sector_exposure = {}
        for asset, position in positions.items():
            sector = sectors.get(asset, 'Unknown')
            sector_exposure[sector] = sector_exposure.get(sector, 0) + position
        return sector_exposure

    def position_correlation(self, 
                           position1: np.ndarray,
                           position2: np.ndarray) -> float:
        """Calculate correlation between two positions"""
        return np.corrcoef(position1, position2)[0][1]

    def check_limits(self, 
                    position_size: float,
                    portfolio_risk: float,
                    correlation: float,
                    leverage: float,
                    concentration: float) -> Dict[str, bool]:
        """Check if risk limits are exceeded"""
        return {
            'position_size': position_size <= self.risk_limits['max_position_size'],
            'portfolio_risk': portfolio_risk <= self.risk_limits['max_portfolio_risk'],
            'correlation': correlation <= self.risk_limits['max_correlation'],
            'leverage': leverage <= self.risk_limits['max_leverage'],
            'concentration': concentration <= self.risk_limits['max_concentration']
        }
    def calculate_max_position_size(self, capital: float, price: float) -> float:
        """Calculate maximum allowed position size based on capital"""
        max_size = capital * self.risk_limits['max_position_size']
        return max_size / price

    def calculate_max_portfolio_risk(self, portfolio_value: float, positions: Dict[str, float]) -> float:
        """Calculate current portfolio risk vs maximum allowed"""
        current_risk = sum(abs(pos) for pos in positions.values()) / portfolio_value
        return current_risk / self.risk_limits['max_portfolio_risk']

    def calculate_max_correlation(self, positions: Dict[str, np.ndarray]) -> float:
        """Calculate maximum correlation between any two positions"""
        correlations = []
        assets = list(positions.keys())
        for i in range(len(assets)):
            for j in range(i + 1, len(assets)):
                corr = self.position_correlation(positions[assets[i]], positions[assets[j]])
                correlations.append(abs(corr))
        return max(correlations) if correlations else 0

    def calculate_max_leverage(self, total_positions: float, equity: float) -> float:
        """Calculate current leverage ratio"""
        return total_positions / equity

    def calculate_max_concentration(self, position_value: float, portfolio_value: float) -> float:
        """Calculate position concentration"""
        return position_value / portfolio_value
    def calculate_max_portfolio_risk(self, portfolio_value: float, positions: Dict[str, float]) -> float:
        """Calculate current portfolio risk vs maximum allowed"""
        current_risk = sum(abs(pos) for pos in positions.values()) / portfolio_value
        # Ensure result is between 0 and 1
        return min(max(current_risk / self.risk_limits['max_portfolio_risk'], 0), 1)
    
    def portfolio_var(self, 
                     returns: Dict[str, np.ndarray],
                     weights: Dict[str, float],
                     confidence: float = 0.95) -> float:
        """Calculate Portfolio Value at Risk"""
        portfolio_returns = sum(returns[asset] * weight 
                              for asset, weight in weights.items())
        # Ensure VaR is between -1 and 0
        var = self.value_at_risk(portfolio_returns, confidence)
        return max(min(var, 0), -1)


# Registry for risk management functions
def get_risk_registry(risk_engine: RiskEngine) -> Dict:
    return {
        # Position Sizing
        'calculate_position_size': risk_engine.calculate_position_size,
        'kelly_criterion': risk_engine.kelly_criterion,
        'optimal_f': risk_engine.optimal_f,
        'fixed_fractional': risk_engine.fixed_fractional,
        'fixed_ratio': risk_engine.fixed_ratio,
        'max_drawdown_limit': risk_engine.max_drawdown_limit,
        
        # Risk Metrics
        'value_at_risk': risk_engine.value_at_risk,
        'expected_shortfall': risk_engine.expected_shortfall,
        'sharpe_ratio': risk_engine.sharpe_ratio,
        'sortino_ratio': risk_engine.sortino_ratio,
        'calmar_ratio': risk_engine.calmar_ratio,
        'max_drawdown': risk_engine.max_drawdown,
        'risk_of_ruin': risk_engine.risk_of_ruin,
        
        # Portfolio Risk
        'portfolio_var': risk_engine.portfolio_var,
        'correlation_risk': risk_engine.correlation_risk,
        'beta_exposure': risk_engine.beta_exposure,
        'sector_exposure': risk_engine.sector_exposure,
        'position_correlation': risk_engine.position_correlation,
        
        # Risk Limits
        'check_limits': risk_engine.check_limits,

        # Add these to get_risk_registry()
        'calculate_max_position_size': risk_engine.calculate_max_position_size,
        'calculate_max_portfolio_risk': risk_engine.calculate_max_portfolio_risk,
        'calculate_max_correlation': risk_engine.calculate_max_correlation,
        'calculate_max_leverage': risk_engine.calculate_max_leverage,
        'calculate_max_concentration': risk_engine.calculate_max_concentration

    }
