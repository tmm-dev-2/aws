from tradingview_ta import TA_Handler, Interval
from tvDatafeed import TvDatafeed
import pandas as pd

class MarketDataFetcher:
    def __init__(self):
        self.tv = TvDatafeed()
        self.handler = TA_Handler()
        
    def get_segment_symbols(self, country: str, segment: str):
        exchange_map = {
            'IN': {'FUT': 'NSE', 'EQ': 'NSE', 'FOREX': 'FX_IDC'},
            'US': {'FUT': 'CME', 'EQ': 'NYSE', 'FOREX': 'OANDA'},
            'UK': {'FUT': 'LSE', 'EQ': 'LSE', 'FOREX': 'FX_IDC'}
        }
        
        exchange = exchange_map[country][segment]
        symbols = self.handler.get_exchange_info(exchange)
        
        if segment == 'FUT':
            symbols = [s for s in symbols if s.endswith('1!')]
            
        return symbols

    def fetch_market_data(self, country: str, segment: str, timeframe: str):
        symbols = self.get_segment_symbols(country, segment)
        market_data = {}
        
        for symbol in symbols:
            try:
                data = self.tv.get_hist(
                    symbol=symbol,
                    exchange=self.get_exchange(country, segment),
                    interval=self.get_interval(timeframe),
                    n_bars=300
                )
                
                market_data[symbol] = {
                    'open': data['open'].tolist(),
                    'high': data['high'].tolist(),
                    'low': data['low'].tolist(),
                    'close': data['close'].tolist(),
                    'volume': data['volume'].tolist(),
                    'timestamp': data.index.astype(int).tolist()
                }
            except Exception as e:
                print(f"Error fetching {symbol}: {e}")
                continue
                
        return {
            'country': country,
            'segment': segment,
            'timeframe': timeframe,
            'data': market_data
        }

    def get_exchange(self, country: str, segment: str):
        exchange_mapping = {
            'IN': {'FUT': 'NSE', 'EQ': 'NSE'},
            'US': {'FUT': 'CME', 'EQ': 'NYSE'},
            'UK': {'FUT': 'LSE', 'EQ': 'LSE'}
        }
        return exchange_mapping[country][segment]

    def get_interval(self, timeframe: str):
        interval_mapping = {
            '1m': Interval.INTERVAL_1_MINUTE,
            '5m': Interval.INTERVAL_5_MINUTES,
            '15m': Interval.INTERVAL_15_MINUTES,
            '1h': Interval.INTERVAL_1_HOUR,
            '4h': Interval.INTERVAL_4_HOURS,
            '1D': Interval.INTERVAL_1_DAY,
            '1W': Interval.INTERVAL_1_WEEK
        }
        return interval_mapping[timeframe]

# Global instance
market_fetcher = MarketDataFetcher()

def get_market_data(country: str, segment: str, timeframe: str):
    return market_fetcher.fetch_market_data(country, segment, timeframe)
