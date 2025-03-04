import numpy as np
import pandas as pd
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional, Union

class TimeEngine:
    def __init__(self):
        self.current_time = None
        self.data_times = []
        
    def get_current_time(self) -> datetime:
        return self.current_time
        
    def get_bar_close_time(self) -> datetime:
        return self.current_time + timedelta(minutes=1)
        
    def get_bar_open_time(self) -> datetime:
        return self.current_time
        
    def get_bar_high_time(self) -> datetime:
        return self.current_time + timedelta(minutes=1)
        
    def get_bar_low_time(self) -> datetime:
        return self.current_time + timedelta(minutes=1)
        
    def get_trading_day(self) -> pd.Timestamp:
        return pd.Timestamp(self.current_time).normalize()
    
    def get_year(self) -> int:
        return pd.Timestamp(self.current_time).year
    
    def get_month(self) -> int:
        return pd.Timestamp(self.current_time).month
    
    def get_week_of_year(self) -> int:
        return pd.Timestamp(self.current_time).week
    
    def get_day_of_month(self) -> int:
        return pd.Timestamp(self.current_time).day
    
    def get_day_of_week(self) -> int:
        return pd.Timestamp(self.current_time).dayofweek
    
    def get_hour(self) -> int:
        return pd.Timestamp(self.current_time).hour
    
    def get_minute(self) -> int:
        return pd.Timestamp(self.current_time).minute
    
    def get_second(self) -> int:
        return pd.Timestamp(self.current_time).second
    
    def get_local_time(self) -> pd.Timestamp:
        return pd.Timestamp(self.current_time)
    
    def get_gmt_time(self) -> pd.Timestamp:
        return pd.Timestamp(self.current_time).tz_localize('UTC')
    
    def get_timestamp(self) -> int:
        return int(pd.Timestamp(self.current_time).timestamp())

    def format_time(self, time: datetime, format_str: str) -> str:
        return time.strftime(format_str)

    def convert_time_to_string(self, time: datetime) -> str:
        return time.isoformat()

    def convert_string_to_time(self, time_str: str) -> datetime:
        return datetime.fromisoformat(time_str)

    def convert_time_to_unix(self, time: datetime) -> int:
        return int(time.timestamp())

    def convert_unix_to_time(self, unix_time: int) -> datetime:
        return datetime.fromtimestamp(unix_time)

    def convert_time_to_timezone(self, time: datetime, tz_str: str) -> datetime:
        return time.astimezone(timezone.utc).astimezone(timezone.utc)

    def convert_time_from_timezone(self, time: datetime, tz_str: str) -> datetime:
        return time.astimezone(timezone.utc)

    def get_period_start(self, period: str) -> datetime:
        return self.current_time.replace(hour=0, minute=0, second=0, microsecond=0)

    def get_period_end(self, period: str) -> datetime:
        return self.current_time.replace(hour=23, minute=59, second=59, microsecond=999999)
class SessionEngine:
    def __init__(self):
        self.current_session = 'regular'
        self.is_live = False
        self.session_times = {
            'regular': {'start': '09:30', 'end': '16:00'},
            'premarket': {'start': '04:00', 'end': '09:30'},
            'postmarket': {'start': '16:00', 'end': '20:00'}
        }
        self.holidays = [
            '2024-01-01',  # New Year's Day
            '2024-01-15',  # Martin Luther King Jr. Day
            '2024-02-19',  # Presidents Day
            '2024-03-29',  # Good Friday
            '2024-05-27',  # Memorial Day
            '2024-06-19',  # Juneteenth
            '2024-07-04',  # Independence Day
            '2024-09-02',  # Labor Day
            '2024-11-28',  # Thanksgiving Day
            '2024-12-25'   # Christmas Day
        ]

    def is_market_session(self) -> bool:
        return self.current_session == 'regular'
        
    def is_premarket_session(self) -> bool:
        return self.current_session == 'premarket'
        
    def is_postmarket_session(self) -> bool:
        return self.current_session == 'postmarket'
        
    def is_first_bar(self) -> bool:
        return self.current_bar == 0
        
    def is_last_bar(self) -> bool:
        return self.current_bar == len(self.data) - 1
        
    def is_realtime(self) -> bool:
        return self.is_live
        
    def get_regular_session(self) -> Dict:
        return self.session_times['regular']
        
    def get_extended_session(self) -> Dict:
        return {
            'premarket': self.session_times['premarket'],
            'postmarket': self.session_times['postmarket']
        }
        
    def get_holidays(self) -> List:
        return self.holidays

class MarketDataEngine:
    def __init__(self):
        self.data = pd.DataFrame()
        self.current_bar = 0
        self.is_realtime = False
        self.time_engine = TimeEngine()
        
    def _get_series_data(self, column: str) -> np.ndarray:
        return self.data[column].values

    def _get_current_bar_index(self) -> int:
        return self.current_bar
        
    def _get_current_bar_time(self) -> datetime:
        return self.data.index[self.current_bar]
        
    def _get_bar_state(self) -> str:
        if self.is_realtime:
            return 'realtime'
        return 'historical'
        
    def _is_bar_confirmed(self) -> bool:
        return not self.is_realtime or self.current_bar < len(self.data) - 1
        
    def _is_first_bar(self) -> bool:
        return self.current_bar == 0
        
    def _is_historical_bar(self) -> bool:
        return not self.is_realtime
        
    def _is_last_bar(self) -> bool:
        return self.current_bar == len(self.data) - 1
        
    def _is_last_confirmed_historical_bar(self) -> bool:
        return self._is_historical_bar() and self._is_last_bar()
        
    def _is_new_bar(self) -> bool:
        return self.is_realtime and self._is_last_bar()
        
    def _is_realtime_bar(self) -> bool:
        return self.is_realtime and self._is_last_bar()
        
    def _get_tick_volume(self) -> float:
        return self.data['volume'].iloc[self.current_bar]
        
    def _get_tick_price(self) -> float:
        return self.data['close'].iloc[self.current_bar]
        
    def _get_tick_direction(self) -> int:
        if self.current_bar == 0:
            return 0
        prev_close = self.data['close'].iloc[self.current_bar - 1]
        curr_close = self.data['close'].iloc[self.current_bar]
        return 1 if curr_close > prev_close else -1 if curr_close < prev_close else 0
        
    def _get_tick_size(self) -> float:
        return 0.01
        
    def _get_tick_id(self) -> int:
        return self.current_bar

class MarketDataSyntax:
    def __init__(self):
        self.market_engine = MarketDataEngine()
        self.session_engine = SessionEngine()

        self.syntax_mappings = {
            # Price Functions
            'open': lambda: self.market_engine._get_series_data('open'),
            'high': lambda: self.market_engine._get_series_data('high'),
            'low': lambda: self.market_engine._get_series_data('low'),
            'close': lambda: self.market_engine._get_series_data('close'),
            'volume': lambda: self.market_engine._get_series_data('volume'),
            'hl2': lambda: (self.market_engine._get_series_data('high') + self.market_engine._get_series_data('low')) / 2,
            'hlc3': lambda: (self.market_engine._get_series_data('high') + self.market_engine._get_series_data('low') + self.market_engine._get_series_data('close')) / 3,
            'hlcc4': lambda: (self.market_engine._get_series_data('high') + self.market_engine._get_series_data('low') + 2 * self.market_engine._get_series_data('close')) / 4,
            'ohlc4': lambda: (self.market_engine._get_series_data('open') + self.market_engine._get_series_data('high') + self.market_engine._get_series_data('low') + self.market_engine._get_series_data('close')) / 4,
            'typical_price': lambda: (self.market_engine._get_series_data('high') + self.market_engine._get_series_data('low') + self.market_engine._get_series_data('close')) / 3,
            'weighted_close': lambda: (self.market_engine._get_series_data('high') + self.market_engine._get_series_data('low') + 2 * self.market_engine._get_series_data('close')) / 4,
            'median_price': lambda: (self.market_engine._get_series_data('high') + self.market_engine._get_series_data('low')) / 2,
            'average_price': lambda: (self.market_engine._get_series_data('open') + self.market_engine._get_series_data('high') + self.market_engine._get_series_data('low') + self.market_engine._get_series_data('close')) / 4,

            # Bar State Functions
            'bar_index': lambda: self.market_engine._get_current_bar_index(),
            'bar_time': lambda: self.market_engine._get_current_bar_time(),
            'bar_state': lambda: self.market_engine._get_bar_state(),
            'barStateIsConfirmed': lambda: self.market_engine._is_bar_confirmed(),
            'barStateIsFirst': lambda: self.market_engine._is_first_bar(),
            'barStateIsHistory': lambda: self.market_engine._is_historical_bar(),
            'barStateIsLast': lambda: self.market_engine._is_last_bar(),
            'barStateIsLastConfirmedHistory': lambda: self.market_engine._is_last_confirmed_historical_bar(),
            'barStateIsNew': lambda: self.market_engine._is_new_bar(),
            'barStateIsRealtime': lambda: self.market_engine._is_realtime_bar(),

            # Tick Data Functions
            'tick_volume': lambda: self.market_engine._get_tick_volume(),
            'tick_price': lambda: self.market_engine._get_tick_price(),
            'tick_direction': lambda: self.market_engine._get_tick_direction(),
            'tick_size': lambda: self.market_engine._get_tick_size(),
            'tick_id': lambda: self.market_engine._get_tick_id(),

            # Time Components
            'time': lambda: self.market_engine.time_engine.get_current_time(),
            'time_close': lambda: self.market_engine.time_engine.get_bar_close_time(),
            'time_open': lambda: self.market_engine.time_engine.get_bar_open_time(),
            'time_high': lambda: self.market_engine.time_engine.get_bar_high_time(),
            'time_low': lambda: self.market_engine.time_engine.get_bar_low_time(),
            'time_tradingday': lambda: self.market_engine.time_engine.get_trading_day(),
            'year': lambda: self.market_engine.time_engine.get_year(),
            'month': lambda: self.market_engine.time_engine.get_month(),
            'weekofyear': lambda: self.market_engine.time_engine.get_week_of_year(),
            'dayofmonth': lambda: self.market_engine.time_engine.get_day_of_month(),
            'dayofweek': lambda: self.market_engine.time_engine.get_day_of_week(),
            'hour': lambda: self.market_engine.time_engine.get_hour(),
            'minute': lambda: self.market_engine.time_engine.get_minute(),
            'second': lambda: self.market_engine.time_engine.get_second(),
            'time_format': lambda time, format: self.market_engine.time_engine.format_time(time, format),
            'time_local': lambda: self.market_engine.time_engine.get_local_time(),
            'time_gmt': lambda: self.market_engine.time_engine.get_gmt_time(),
            'timestamp': lambda: self.market_engine.time_engine.get_timestamp(),

   
        
            # Session States
            'session_ismarket': lambda: self.session_engine.is_market_session(),
            'session_ispremarket': lambda: self.session_engine.is_premarket_session(),
            'session_ispostmarket': lambda: self.session_engine.is_postmarket_session(),
            'session_isfirstbar': lambda: self.session_engine.is_first_bar(),
            'session_islastbar': lambda: self.session_engine.is_last_bar(),
            'session_isrealtime': lambda: self.session_engine.is_realtime(),
            'session_regular': lambda: self.session_engine.get_regular_session(),
            'session_extended': lambda: self.session_engine.get_extended_session(),
            'session_holidays': lambda: self.session_engine.get_holidays(),
        


            # Time Conversions
            'time_to_string': lambda time: self.market_engine.time_engine.convert_time_to_string(time),
            'time_from_string': lambda str: self.market_engine.time_engine.convert_string_to_time(str),
            'time_to_unix': lambda time: self.market_engine.time_engine.convert_time_to_unix(time),
            'time_from_unix': lambda unix: self.market_engine.time_engine.convert_unix_to_time(unix),
            'time_to_timezone': lambda time, timezone: self.market_engine.time_engine.convert_time_to_timezone(time, timezone),
            'time_from_timezone': lambda time, timezone: self.market_engine.time_engine.convert_time_from_timezone(time, timezone),
            'time_period_start': lambda period: self.market_engine.time_engine.get_period_start(period),
            'time_period_end': lambda period: self.market_engine.time_engine.get_period_end(period)
        }
