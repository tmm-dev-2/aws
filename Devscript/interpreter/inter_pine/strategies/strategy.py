from typing import List, Dict, Any, Optional, TYPE_CHECKING
from dataclasses import dataclass
from datetime import datetime
import numpy as np
from enum import Enum

class OrderType(Enum):
    MARKET = "market"
    LIMIT = "limit"
    STOP = "stop"
    STOP_LIMIT = "stop_limit"

@dataclass
class Position:
    direction: str
    size: float
    entry_price: float
    entry_time: datetime
    entry_name: str
    entry_id: str
    entry_bar: int
    entry_comment: str
    sl_price: Optional[float] = None
    tp_price: Optional[float] = None

@dataclass
class Order:
    direction: str
    price: float
    quantity: float
    order_type: OrderType
    order_id: str
    timestamp: datetime
    status: str = 'pending'

class RiskEngine:
    def __init__(self):
        self.max_position_size = float('inf')
        self.max_drawdown = float('inf')
        self.max_loss = float('inf')
        self.max_trades = float('inf')
        self.max_loss_days = float('inf')
        self.max_correlation = 1.0
        self.max_exposure = float('inf')
        
    def set_max_position_size(self, size: float) -> None:
        self.max_position_size = size
        
    def set_max_drawdown(self, pct: float) -> None:
        self.max_drawdown = pct
        
    def set_max_loss(self, amount: float) -> None:
        self.max_loss = amount
        
    def set_max_trades(self, num: int) -> None:
        self.max_trades = num
        
    def set_max_loss_days(self, days: int) -> None:
        self.max_loss_days = days
        
    def set_max_correlation(self, threshold: float) -> None:
        self.max_correlation = threshold
        
    def set_max_exposure(self, amount: float) -> None:
        self.max_exposure = amount
        
    def calculate_position_size(self, risk_pct: float, sl_price: float) -> float:
        return risk_pct * self.max_position_size
        
    def check_entry_allowed(self) -> bool:
        return True

class PerformanceEngine:
    def __init__(self, strategy_engine: 'StrategyEngine'):
        self.strategy_engine = strategy_engine
        self.trades: List[Dict[str, Any]] = []
        self.equity_curve: List[float] = []
        self.initial_capital: float = strategy_engine.initial_capital
        self.current_capital: float = self.initial_capital
        self.max_drawdown_value: float = 0
        self.peak_capital: float = self.initial_capital
        
    def calculate_equity(self) -> float:
        return self.current_capital
        
    def calculate_net_profit(self) -> float:
        return self.current_capital - self.initial_capital
        
    def calculate_gross_profit(self) -> float:
        return sum(trade['pnl'] for trade in self.strategy_engine.trade_history if trade['pnl'] > 0)
        
    def calculate_gross_loss(self) -> float:
        return sum(trade['pnl'] for trade in self.strategy_engine.trade_history if trade['pnl'] < 0)
        
    def calculate_profit_factor(self) -> float:
        gross_profit = self.calculate_gross_profit()
        gross_loss = abs(self.calculate_gross_loss())
        return gross_profit / gross_loss if gross_loss != 0 else float('inf')
        
    def calculate_max_drawdown(self) -> float:
        if not self.equity_curve:
            return 0.0
        peak = self.equity_curve[0]
        max_dd = 0.0
        
        for equity in self.equity_curve:
            if equity > peak:
                peak = equity
            dd = (peak - equity) / peak
            max_dd = max(max_dd, dd)
        return max_dd
        
    def calculate_recovery_factor(self) -> float:
        net_profit = self.calculate_net_profit()
        max_dd = self.calculate_max_drawdown() * self.initial_capital
        return net_profit / max_dd if max_dd > 0 else 0
        
    def calculate_sharpe_ratio(self, risk_free_rate: float = 0.02) -> float:
        if len(self.equity_curve) < 2:
            return 0.0
            
        returns = np.diff(self.equity_curve) / self.equity_curve[:-1]
        excess_returns = returns - (risk_free_rate / 252)
        return np.mean(excess_returns) / np.std(excess_returns) * np.sqrt(252) if np.std(excess_returns) > 0 else 0
        
    def calculate_sortino_ratio(self, risk_free_rate: float = 0.02) -> float:
        if len(self.equity_curve) < 2:
            return 0.0
            
        returns = np.diff(self.equity_curve) / self.equity_curve[:-1]
        excess_returns = returns - (risk_free_rate / 252)
        downside_returns = excess_returns[excess_returns < 0]
        
        if len(downside_returns) == 0 or np.std(downside_returns) == 0:
            return 0.0
            
        return np.mean(excess_returns) / np.std(downside_returns) * np.sqrt(252)

        
    def calculate_calmar_ratio(self) -> float:
        annual_return = (self.calculate_net_profit() / self.initial_capital) * (252 / len(self.strategy_engine.trade_history))
        max_dd = self.calculate_max_drawdown()
        return annual_return / max_dd if max_dd > 0 else 0
        
    def get_total_trades(self) -> int:
        return len(self.strategy_engine.trade_history)
        
    def get_winning_trades(self) -> int:
        return sum(1 for trade in self.strategy_engine.trade_history if trade['pnl'] > 0)
        
    def get_losing_trades(self) -> int:
        return sum(1 for trade in self.strategy_engine.trade_history if trade['pnl'] < 0)
        
    def calculate_win_rate(self) -> float:
        total = self.get_total_trades()
        return (self.get_winning_trades() / total) * 100 if total > 0 else 0
        
    def calculate_avg_trade(self) -> float:
        trades = self.strategy_engine.trade_history
        return sum(trade['pnl'] for trade in trades) / len(trades) if trades else 0
        
    def calculate_avg_winning_trade(self) -> float:
        winning_trades = [trade['pnl'] for trade in self.strategy_engine.trade_history if trade['pnl'] > 0]
        return sum(winning_trades) / len(winning_trades) if winning_trades else 0
        
    def calculate_avg_losing_trade(self) -> float:
        losing_trades = [trade['pnl'] for trade in self.strategy_engine.trade_history if trade['pnl'] < 0]
        return sum(losing_trades) / len(losing_trades) if losing_trades else 0
        
    def get_largest_win(self) -> float:
        return max((trade['pnl'] for trade in self.strategy_engine.trade_history), default=0)
        
    def get_largest_loss(self) -> float:
        return min((trade['pnl'] for trade in self.strategy_engine.trade_history), default=0)
        
    def get_max_contracts_held(self) -> float:
        return max((trade['quantity'] for trade in self.strategy_engine.trade_history), default=0)
        
    def calculate_max_leverage(self) -> float:
        max_exposure = max((trade['quantity'] * trade['entry_price'] 
                          for trade in self.strategy_engine.trade_history), default=0)
        return max_exposure / self.initial_capital if self.initial_capital > 0 else 0

    def update_metrics(self, trade: Dict[str, Any]) -> None:
        self.trades.append(trade)
        self.current_capital += trade['pnl']
        self.equity_curve.append(self.current_capital)
        
        if self.current_capital > self.peak_capital:
            self.peak_capital = self.current_capital
        current_dd = (self.peak_capital - self.current_capital) / self.peak_capital
        self.max_drawdown_value = max(self.max_drawdown_value, current_dd)

    def get_trade_metrics(self) -> Dict[str, Any]:
        return {
            'total_trades': self.get_total_trades(),
            'winning_trades': self.get_winning_trades(),
            'losing_trades': self.get_losing_trades(),
            'win_rate': self.calculate_win_rate(),
            'profit_factor': self.calculate_profit_factor(),
            'net_profit': self.calculate_net_profit(),
            'gross_profit': self.calculate_gross_profit(),
            'gross_loss': self.calculate_gross_loss(),
            'max_drawdown': self.calculate_max_drawdown(),
            'sharpe_ratio': self.calculate_sharpe_ratio(),
            'sortino_ratio': self.calculate_sortino_ratio(),
            'calmar_ratio': self.calculate_calmar_ratio(),
            'recovery_factor': self.calculate_recovery_factor(),
            'avg_trade': self.calculate_avg_trade(),
            'avg_winning_trade': self.calculate_avg_winning_trade(),
            'avg_losing_trade': self.calculate_avg_losing_trade(),
            'largest_win': self.get_largest_win(),
            'largest_loss': self.get_largest_loss(),
            'max_contracts': self.get_max_contracts_held(),
            'max_leverage': self.calculate_max_leverage()
        }

    def get_equity_stats(self) -> Dict[str, float]:
        return {
            'initial_capital': self.initial_capital,
            'current_capital': self.current_capital,
            'peak_capital': self.peak_capital,
            'max_drawdown': self.max_drawdown_value,
            'return_pct': (self.current_capital - self.initial_capital) / self.initial_capital * 100
        }

    def reset_metrics(self) -> None:
        self.trades = []
        self.equity_curve = []
        self.current_capital = self.initial_capital
        self.peak_capital = self.initial_capital
        self.max_drawdown_value = 0

class TradeEngine:
    def __init__(self, strategy_engine: 'StrategyEngine'):
        self.strategy_engine = strategy_engine
        self.commission_rate = 0.001
        self.slippage_rate = 0.0001
        self.initial_margin_rate = 0.1
        self.maintenance_margin_rate = 0.05
        self.rollover_rate = 0.0001
        self.swap_long_rate = -0.0002
        self.swap_short_rate = 0.0001

    def get_initial_margin(self) -> float:
        position_value = self.strategy_engine.get_position_value()
        return position_value * self.initial_margin_rate

    def get_maintenance_margin(self) -> float:
        position_value = self.strategy_engine.get_position_value()
        return position_value * self.maintenance_margin_rate

    def calculate_commission_amount(self, trade_value: float) -> float:
        return trade_value * self.commission_rate

    def calculate_commission_percent(self) -> float:
        return self.commission_rate * 100

    def calculate_slippage_amount(self, trade_value: float) -> float:
        return trade_value * self.slippage_rate

    def calculate_slippage_percent(self) -> float:
        return self.slippage_rate * 100

    def calculate_rollover_fee(self, position_value: float) -> float:
        return position_value * self.rollover_rate

    def calculate_swap_long(self, position_value: float) -> float:
        return position_value * self.swap_long_rate

    def calculate_swap_short(self, position_value: float) -> float:
        return position_value * self.swap_short_rate

class StrategyEngine:
    def __init__(self):
        self.positions: Dict[str, Position] = {}
        self.orders: Dict[str, Order] = {}
        self.trade_history: List[Dict] = []
        self.equity_curve = []
        self.initial_capital = 100000
        self.current_capital = self.initial_capital
        
        self.risk_engine = RiskEngine()
        self.performance_engine = PerformanceEngine(self)
        self.trade_engine = TradeEngine(self)
        
        self.current_bar = 0

    def _check_risk_limits(self, order: Order) -> bool:
        # Check current position size + new order against max position size
        total_size = self.get_position_size() + order.quantity
        if total_size > self.risk_engine.max_position_size:
            return False
            
        # Check if entry is allowed by risk engine
        if not self.risk_engine.check_entry_allowed():
            return False
            
        return True

    def enter_long(self, price: float, qty: float, name: Optional[str] = None) -> bool:
        order = Order(
            direction='long',
            price=price,
            quantity=qty,
            order_type=OrderType.MARKET,
            order_id=self._generate_position_id(),
            timestamp=datetime.now()
        )
        
        if self._check_risk_limits(order):
            position = Position(
                direction='long',
                size=qty,
                entry_price=price,
                entry_time=datetime.now(),
                entry_name=name or 'Long Entry',
                entry_id=order.order_id,
                entry_bar=self.current_bar,
                entry_comment=""
            )
            self.positions[position.entry_id] = position
            return True
        return False
    def cancel_order(self, order_id: str) -> bool:
        if order_id in self.orders:
            del self.orders[order_id]
            return True
        return False

    def cancel_all_orders(self) -> bool:
        self.orders.clear()
        return True


    def enter_short(self, price: float, qty: float, name: Optional[str] = None) -> bool:
        order = Order(
            direction='short',
            price=price,
            quantity=qty,
            order_type=OrderType.MARKET,
            order_id=self._generate_position_id(),
            timestamp=datetime.now()
        )
        
        if self._check_risk_limits(order):
            position = Position(
                direction='short',
                size=qty,
                entry_price=price,
                entry_time=datetime.now(),
                entry_name=name or 'Short Entry',
                entry_id=order.order_id,
                entry_bar=self.current_bar,
                entry_comment=""
            )
            self.positions[position.entry_id] = position
            return True
        return False
    def exit_position(self, price: Optional[float] = None, qty: Optional[float] = None, 
                     name: Optional[str] = None) -> bool:
        for pos_id, position in self.positions.items():
            if name is None or position.entry_name == name:
                exit_qty = qty or position.size
                self._process_exit(pos_id, position, price, exit_qty)
                return True
        return False

    def close_position(self, name: Optional[str] = None) -> bool:
        return self.exit_position(name=name)

    def close_all_positions(self) -> bool:
        for pos_id in list(self.positions.keys()):
            self.exit_position(pos_id=pos_id)
        return True

    def get_position_size(self) -> float:
        return sum(pos.size for pos in self.positions.values())

    def get_position_value(self) -> float:
        return sum(pos.size * pos.entry_price for pos in self.positions.values())

    def get_position_avg_price(self) -> float:
        total_value = sum(pos.size * pos.entry_price for pos in self.positions.values())
        total_size = sum(pos.size for pos in self.positions.values())
        return total_value / total_size if total_size > 0 else 0.0

    def get_position_entry_name(self) -> str:
        return next(iter(self.positions.values())).entry_name if self.positions else ""

    def get_position_entry_bar(self) -> int:
        return next(iter(self.positions.values())).entry_bar if self.positions else 0

    def get_position_entry_time(self) -> datetime:
        return next(iter(self.positions.values())).entry_time if self.positions else datetime.now()

    def get_position_entry_price(self) -> float:
        return next(iter(self.positions.values())).entry_price if self.positions else 0.0

    def get_position_entry_id(self) -> str:
        return next(iter(self.positions.values())).entry_id if self.positions else ""

    def get_position_entry_comment(self) -> str:
        return next(iter(self.positions.values())).entry_comment if self.positions else ""

    def _process_exit(self, pos_id: str, position: Position, exit_price: float, exit_qty: float):
        pnl = self._calculate_position_pnl(position, exit_price)
        self._update_equity(pnl)
        
        trade_record = {
            'entry_time': position.entry_time,
            'exit_time': datetime.now(),
            'direction': position.direction,
            'entry_price': position.entry_price,
            'exit_price': exit_price,
            'quantity': exit_qty,
            'pnl': pnl,
            'name': position.entry_name
        }
        self.trade_history.append(trade_record)
        self.performance_engine.update_metrics(trade_record)
        
        if exit_qty >= position.size:
            del self.positions[pos_id]
        else:
            position.size -= exit_qty

    def _calculate_position_pnl(self, position: Position, exit_price: float) -> float:
        if position.direction == 'long':
            return (exit_price - position.entry_price) * position.size
        return (position.entry_price - exit_price) * position.size

    def _update_equity(self, pnl: float):
        self.current_capital += pnl
        self.equity_curve.append(self.current_capital)
        self.performance_engine.equity_curve = self.equity_curve

    def _generate_position_id(self) -> str:
        return f"pos_{datetime.now().timestamp()}"

    def update_bar(self, bar_index: int) -> None:
        self.current_bar = bar_index

class StrategySyntax:
    def __init__(self):
        self.strategy_engine = StrategyEngine()
        
        self.syntax_mappings = {
            # Entry/Exit Functions
            'strategy_entry_long': lambda price, qty, name=None: self.strategy_engine.enter_long(price, qty, name),
            'strategy_entry_short': lambda price, qty, name=None: self.strategy_engine.enter_short(price, qty, name),
            'strategy_exit': lambda price=None, qty=None, name=None: self.strategy_engine.exit_position(price, qty, name),
            'strategy_close': lambda name=None: self.strategy_engine.close_position(name),
            'strategy_cancel': lambda id=None: self.strategy_engine.cancel_order(id),
            'strategy_cancel_all': lambda: self.strategy_engine.cancel_all_orders(),
            'strategy_close_all': lambda: self.strategy_engine.close_all_positions(),
            'strategy_order': lambda direction, price, qty: self.strategy_engine.cancel_all_orders(direction, price, qty),
            'strategy_order_cancel': lambda id: self.strategy_engine.cancel_order(id),
            'strategy_risk_allow_entry': lambda: self.strategy_engine.risk_engine.check_entry_allowed(),

            # Position Management
            'strategy_position_size': lambda: self.strategy_engine.get_position_size(),
            'strategy_position_avg_price': lambda: self.strategy_engine.get_position_avg_price(),
            'strategy_position_entry_name': lambda: self.strategy_engine.get_position_entry_name(),
            'strategy_position_entry_bar': lambda: self.strategy_engine.get_position_entry_bar(),
            'strategy_position_entry_time': lambda: self.strategy_engine.get_position_entry_time(),
            'strategy_position_entry_price': lambda: self.strategy_engine.get_position_entry_price(),
            'strategy_position_entry_id': lambda: self.strategy_engine.get_position_entry_id(),
            'strategy_position_entry_comment': lambda: self.strategy_engine.get_position_entry_comment(),

            # Risk Management
            'strategy_risk_max_position': lambda size: self.strategy_engine.risk_engine.set_max_position_size(size),
            'strategy_risk_max_drawdown': lambda pct: self.strategy_engine.risk_engine.set_max_drawdown(pct),
            'strategy_risk_max_loss': lambda amount: self.strategy_engine.risk_engine.set_max_loss(amount),
            'strategy_risk_max_trades': lambda num: self.strategy_engine.risk_engine.set_max_trades(num),
            'strategy_risk_max_loss_days': lambda days: self.strategy_engine.risk_engine.set_max_loss_days(days),
            'strategy_risk_max_correlation': lambda threshold: self.strategy_engine.risk_engine.set_max_correlation(threshold),
            'strategy_risk_max_exposure': lambda amount: self.strategy_engine.risk_engine.set_max_exposure(amount),
            'strategy_risk_position_size': lambda risk_pct, sl_price: self.strategy_engine.risk_engine.calculate_position_size(risk_pct, sl_price),

            # Performance Metrics
            'strategy_equity': lambda: self.strategy_engine.performance_engine.calculate_equity(),
            'strategy_net_profit': lambda: self.strategy_engine.performance_engine.calculate_net_profit(),
            'strategy_gross_profit': lambda: self.strategy_engine.performance_engine.calculate_gross_profit(),
            'strategy_gross_loss': lambda: self.strategy_engine.performance_engine.calculate_gross_loss(),
            'strategy_profit_factor': lambda: self.strategy_engine.performance_engine.calculate_profit_factor(),
            'strategy_max_drawdown': lambda: self.strategy_engine.performance_engine.calculate_max_drawdown(),
            'strategy_recovery_factor': lambda: self.strategy_engine.performance_engine.calculate_recovery_factor(),
            'strategy_sharpe_ratio': lambda: self.strategy_engine.performance_engine.calculate_sharpe_ratio(),
            'strategy_sortino_ratio': lambda: self.strategy_engine.performance_engine.calculate_sortino_ratio(),
            'strategy_calmar_ratio': lambda: self.strategy_engine.performance_engine.calculate_calmar_ratio(),
            'strategy_trades_total': lambda: self.strategy_engine.performance_engine.get_total_trades(),
            'strategy_trades_won': lambda: self.strategy_engine.performance_engine.get_winning_trades(),
            'strategy_trades_lost': lambda: self.strategy_engine.performance_engine.get_losing_trades(),
            'strategy_win_rate': lambda: self.strategy_engine.performance_engine.calculate_win_rate(),
            'strategy_avg_trade': lambda: self.strategy_engine.performance_engine.calculate_avg_trade(),
            'strategy_avg_winning_trade': lambda: self.strategy_engine.performance_engine.calculate_avg_winning_trade(),
            'strategy_avg_losing_trade': lambda: self.strategy_engine.performance_engine.calculate_avg_losing_trade(),
            'strategy_largest_win': lambda: self.strategy_engine.performance_engine.get_largest_win(),
            'strategy_largest_loss': lambda: self.strategy_engine.performance_engine.get_largest_loss(),
            'strategy_max_contracts_held': lambda: self.strategy_engine.performance_engine.get_max_contracts_held(),
            'strategy_max_leverage_used': lambda: self.strategy_engine.performance_engine.calculate_max_leverage(),

            # Trade Management
            'strategy_margin_initial': lambda: self.strategy_engine.trade_engine.get_initial_margin(),
            'strategy_margin_maintenance': lambda: self.strategy_engine.trade_engine.get_maintenance_margin(),
            'strategy_commission_amount': lambda trade_value: self.strategy_engine.trade_engine.calculate_commission_amount(trade_value),
            'strategy_commission_percent': lambda: self.strategy_engine.trade_engine.calculate_commission_percent(),
            'strategy_slippage_amount': lambda trade_value: self.strategy_engine.trade_engine.calculate_slippage_amount(trade_value),
            'strategy_slippage_percent': lambda: self.strategy_engine.trade_engine.calculate_slippage_percent(),
            'strategy_rollover_fee': lambda position_value: self.strategy_engine.trade_engine.calculate_rollover_fee(position_value),
            'strategy_swap_long': lambda position_value: self.strategy_engine.trade_engine.calculate_swap_long(position_value),
            'strategy_swap_short': lambda position_value: self.strategy_engine.trade_engine.calculate_swap_short(position_value)
        }

    def execute(self, syntax_name: str, *args, **kwargs):
        if syntax_name in self.syntax_mappings:
            return self.syntax_mappings[syntax_name](*args, **kwargs)
        raise ValueError(f"Unknown syntax: {syntax_name}")
