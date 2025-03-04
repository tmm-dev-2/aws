from typing import Dict, Optional, Union
import requests
import json

class TVSymbolEngine:
    def __init__(self):
        self.base_url = "https://udf.tradingview.com"
        self.symbol_data = {}
        self.current_symbol = None
        
    def load_symbol(self, symbol: str):
        self.current_symbol = symbol
        response = requests.get(f"{self.base_url}/symbols/{symbol}")
        self.symbol_data = response.json()

    def get_ticker(self) -> str:
        return self.symbol_data.get('ticker', self.current_symbol)

    def get_description(self) -> str:
        return self.symbol_data.get('description', '')

    def get_type(self) -> str:
        return self.symbol_data.get('type', '')

    def get_root(self) -> str:
        return self.symbol_data.get('root', '')

    def get_prefix(self) -> str:
        return self.symbol_data.get('prefix', '')

    def get_suffix(self) -> str:
        return self.symbol_data.get('suffix', '')

    def get_currency(self) -> str:
        return self.symbol_data.get('currency', 'USD')

    def get_exchange(self) -> str:
        return self.symbol_data.get('exchange', '')

    def get_min_tick(self) -> float:
        return float(self.symbol_data.get('minmov', 1)) / float(self.symbol_data.get('pricescale', 1))

    def get_min_move(self) -> float:
        return float(self.symbol_data.get('minmov', 1))

    def get_point_value(self) -> float:
        return float(self.symbol_data.get('pointvalue', 1.0))

    def get_price_scale(self) -> int:
        return int(self.symbol_data.get('pricescale', 2))

    def get_pip_size(self) -> float:
        return float(self.symbol_data.get('pipsize', 0.0001))

    def get_pip_value(self) -> float:
        return float(self.symbol_data.get('pipvalue', 1.0))

    def get_min_lot(self) -> float:
        return float(self.symbol_data.get('minlot', 0.01))

    def get_max_lot(self) -> float:
        return float(self.symbol_data.get('maxlot', 100000.0))

    def get_lot_step(self) -> float:
        return float(self.symbol_data.get('lotstep', 0.01))

    def get_initial_margin(self) -> float:
        return float(self.symbol_data.get('margin_initial', 100.0))

    def get_maintenance_margin(self) -> float:
        return float(self.symbol_data.get('margin_maintenance', 50.0))

    def get_session(self) -> Dict:
        return self.symbol_data.get('session', {})

    def get_regular_session(self) -> Dict:
        return self.symbol_data.get('session_regular', {})

    def get_extended_session(self) -> Dict:
        return self.symbol_data.get('session_extended', {})

    def get_premarket_session(self) -> Dict:
        return self.symbol_data.get('session_premarket', {})

    def get_postmarket_session(self) -> Dict:
        return self.symbol_data.get('session_postmarket', {})

    def get_timezone(self) -> str:
        return self.symbol_data.get('timezone', 'UTC')

    def get_industry(self) -> str:
        return self.symbol_data.get('industry', '')

    def get_sector(self) -> str:
        return self.symbol_data.get('sector', '')

    def get_market_cap(self) -> float:
        return float(self.symbol_data.get('market_cap', 0.0))

    def get_average_volume(self) -> float:
        return float(self.symbol_data.get('average_volume', 0.0))

    def get_dividend_yield(self) -> float:
        return float(self.symbol_data.get('dividend_yield', 0.0))

    def get_earnings_per_share(self) -> float:
        return float(self.symbol_data.get('earnings_per_share', 0.0))

    def get_price_earnings_ratio(self) -> float:
        return float(self.symbol_data.get('price_earnings_ratio', 0.0))

    def get_shares_outstanding(self) -> float:
        return float(self.symbol_data.get('shares_outstanding', 0.0))

    def get_float_shares(self) -> float:
        return float(self.symbol_data.get('float_shares', 0.0))

class TVSymbolSyntax:
    def __init__(self):
        self.symbol_engine = TVSymbolEngine()
        
        self.syntax_mappings = {
            'syminfo_ticker': lambda: self.symbol_engine.get_ticker(),
            'syminfo_description': lambda: self.symbol_engine.get_description(),
            'syminfo_type': lambda: self.symbol_engine.get_type(),
            'syminfo_root': lambda: self.symbol_engine.get_root(),
            'syminfo_prefix': lambda: self.symbol_engine.get_prefix(),
            'syminfo_suffix': lambda: self.symbol_engine.get_suffix(),
            'syminfo_currency': lambda: self.symbol_engine.get_currency(),
            'syminfo_exchange': lambda: self.symbol_engine.get_exchange(),
            'syminfo_mintick': lambda: self.symbol_engine.get_min_tick(),
            'syminfo_minmove': lambda: self.symbol_engine.get_min_move(),
            'syminfo_pointvalue': lambda: self.symbol_engine.get_point_value(),
            'syminfo_pricescale': lambda: self.symbol_engine.get_price_scale(),
            'syminfo_pipsize': lambda: self.symbol_engine.get_pip_size(),
            'syminfo_pipvalue': lambda: self.symbol_engine.get_pip_value(),
            'syminfo_minlot': lambda: self.symbol_engine.get_min_lot(),
            'syminfo_maxlot': lambda: self.symbol_engine.get_max_lot(),
            'syminfo_lotstep': lambda: self.symbol_engine.get_lot_step(),
            'syminfo_margin_initial': lambda: self.symbol_engine.get_initial_margin(),
            'syminfo_margin_maintenance': lambda: self.symbol_engine.get_maintenance_margin(),
            'syminfo_session': lambda: self.symbol_engine.get_session(),
            'syminfo_session_regular': lambda: self.symbol_engine.get_regular_session(),
            'syminfo_session_extended': lambda: self.symbol_engine.get_extended_session(),
            'syminfo_session_premarket': lambda: self.symbol_engine.get_premarket_session(),
            'syminfo_session_postmarket': lambda: self.symbol_engine.get_postmarket_session(),
            'syminfo_timezone': lambda: self.symbol_engine.get_timezone(),
            'syminfo_industry': lambda: self.symbol_engine.get_industry(),
            'syminfo_sector': lambda: self.symbol_engine.get_sector(),
            'syminfo_market_cap': lambda: self.symbol_engine.get_market_cap(),
            'syminfo_volume_avg': lambda: self.symbol_engine.get_average_volume(),
            'syminfo_dividend_yield': lambda: self.symbol_engine.get_dividend_yield(),
            'syminfo_earnings_per_share': lambda: self.symbol_engine.get_earnings_per_share(),
            'syminfo_price_earnings': lambda: self.symbol_engine.get_price_earnings_ratio(),
            'syminfo_shares_outstanding': lambda: self.symbol_engine.get_shares_outstanding(),
            'syminfo_float_shares': lambda: self.symbol_engine.get_float_shares()
        }
