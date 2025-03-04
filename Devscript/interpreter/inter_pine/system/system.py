import datetime
import logging
import json
import tkinter as tk
import time
import winsound
from pathlib import Path
from typing import Dict, List, Any, Callable

class AlertManager:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.colors = {
            'buy': '#4CAF50',
            'sell': '#F44336',
            'info': '#2196F3',
            'warning': '#FF9800'
        }
        
    def show_popup(self, alert_type: str, message: str):
        popup = tk.Toplevel(self.root)
        popup.geometry('300x150+1000+50')
        popup.overrideredirect(True)
        popup.configure(bg=self.colors.get(alert_type, '#424242'))
        
        tk.Label(popup, 
                text=message,
                fg='white',
                bg=self.colors.get(alert_type, '#424242'),
                wraplength=280,
                font=('Arial', 11)).pack(pady=20)
        
        popup.after(5000, popup.destroy)
        
        for i in range(0, 100, 2):
            popup.attributes('-alpha', i/100)
            popup.update()
            time.sleep(0.01)
            
    def play_sound(self, frequency: int = 2500, duration: int = 1000):
        winsound.Beep(frequency, duration)

class SystemEngine:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.alert_manager = AlertManager(self.root)
        self.trade_log = []
        
        # Create logs directory
        self.log_dir = Path('logs')
        self.log_dir.mkdir(exist_ok=True)
        
        # Initialize logging
        self._setup_logging()

    def _setup_logging(self):
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        self.log_file_path = self.log_dir / f'strategy_{timestamp}.log'
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_file_path),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def log_trade(self, trade_info: Dict[str, Any]):
        timestamp = datetime.datetime.now().isoformat()
        log_entry = {
            'timestamp': timestamp,
            'trade': trade_info
        }
        self.trade_log.append(log_entry)
        self.logger.info(f"Trade logged: {json.dumps(log_entry)}")
        
        # Also write to trade specific log file
        trade_log_path = self.log_dir / 'trades.log'
        with open(trade_log_path, 'a') as f:
            f.write(f"{json.dumps(log_entry)}\n")

    def log_error(self, message: str):
        self.logger.error(message)
        
        # Also write to error specific log file
        error_log_path = self.log_dir / 'errors.log'
        with open(error_log_path, 'a') as f:
            timestamp = datetime.datetime.now().isoformat()
            f.write(f"{timestamp} - ERROR - {message}\n")

def get_strategy_registry(strategy_engine: SystemEngine) -> Dict[str, Callable]:
    return {
        'alerts': {
            'alert_popup_buy': lambda msg: strategy_engine.alert_manager.show_popup('buy', msg),
            'alert_popup_sell': lambda msg: strategy_engine.alert_manager.show_popup('sell', msg),
            'alert_popup_info': lambda msg: strategy_engine.alert_manager.show_popup('info', msg),
            'alert_popup_warning': lambda msg: strategy_engine.alert_manager.show_popup('warning', msg),
            'alert_sound': lambda: strategy_engine.alert_manager.play_sound()
        },
        'logging': {
            'log_trade': strategy_engine.log_trade,
            'log_error': strategy_engine.log_error
        }
    }
