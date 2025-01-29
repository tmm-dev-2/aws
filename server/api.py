from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
import os
import threading
from collections import deque
import time
import yfinance as yf
from tvDatafeed import TvDatafeed, Interval
from datetime import datetime
import time
import sys
import os
import numpy as np
import talib
import json
import requests
import pandas as pd

app = Flask(__name__)
CORS(app)


# Market mapping and cache setup
MARKETS = {
    # Stocks with their symbol patterns
    "NYSE": ["", ".US", ".N", "-US"],
    "NASDAQ": ["", ".US", ".O", "-US"],
    "AMEX": [".A", "-AM"],
    "TSX": [".TO", ".V", ".CN"],
    "LSE": [".L", ".IL", "-L", "-LN"],
    "EURONEXT": [".PA", ".AS", ".BR", ".AMS", ".LIS"],
    "XETRA": [".DE", ".F", ".BE", ".HAM", ".HAN", ".MU", ".SG"],
    "ASX": [".AX", "-AU"],
    "NSE": [".NS", "-IN"],
    "BSE": [".BO", "-IN"],
    "HKEX": [".HK", "-HK"],
    "SGX": [".SI", "-SG"],
    "KRX": [".KS", ".KQ", "-KR"],
    "JPX": [".T", ".JP", "-JP"],
    
    # Crypto patterns
    "BINANCE": ["USDT", "BUSD", "BTC", "ETH", "BNB"],
    "COINBASE": ["USD", "-USD", "-USDC"],
    "KRAKEN": ["-USD", "-EUR", "-BTC", "-ETH"],
    "BITFINEX": [":USD", ":BTC", ":UST"],
    "BYBIT": [".P", "-PERP"],
    
    # Forex patterns
    "FOREX": ["FX:", "FX_IDC:", "OANDA:", "FXCM:"],
    
    # Futures
    "CME": ["1!", "ES1!", "NQ1!", "YM1!"],
    "NYMEX": ["CL1!", "NG1!", "GC1!", "SI1!"]
}

def determine_market(symbol):
    """Determine the market based on symbol characteristics"""
    for market, patterns in MARKETS.items():
        if any(pattern in symbol for pattern in patterns):
            return market
            
    # Smart fallback based on symbol structure
    if ':' in symbol:
        prefix = symbol.split(':')[0]
        return MARKETS.get(prefix, "NYSE")
        
    return "NYSE"

def get_symbol_type(symbol: str) -> str:
    if any(crypto_suffix in symbol for market, suffixes in MARKETS.items() if market in ["BINANCE", "COINBASE", "KRAKEN"]):
        return "crypto"
    if any(forex_pattern in symbol for forex_pattern in MARKETS["FOREX"]):
        return "forex"
    if any(futures_pattern in symbol for market, patterns in MARKETS.items() if market in ["CME", "NYMEX"]):
        return "futures"
    return "stock"

# Add your TradingView username and password
TV_USERNAME = "ojasforbusiness2"
TV_PASSWORD = "APVOm@007!!!"

# Initialize TvDatafeed with username and password
tv = TvDatafeed(username=TV_USERNAME, password=TV_PASSWORD)

# Store exchange info from symbol search results
exchange_info = {}

@app.route('/fetch_candles', methods=['GET'])
def fetch_candles():
    try:
        symbol = request.args.get('symbol')
        timeframe = request.args.get('timeframe', '1D')
        
        # Handle default crypto pairs and other symbols
        if ':' not in symbol:
            if 'USDT' in symbol:
                exchange = 'BINANCE'
                base_symbol = symbol
            elif 'USD' in symbol and not symbol.endswith('USD'):
                exchange = 'COINBASE'
                base_symbol = symbol
            else:
                exchange = determine_market(symbol)
                base_symbol = symbol
            
            symbol = f"{exchange}:{base_symbol}"
        else:
            exchange, base_symbol = symbol.split(':')
            
        print(f"Fetching data for {symbol}")
        
        interval_mapping = {
            '1d': Interval.in_daily,
            '1w': Interval.in_weekly,
            '1M': Interval.in_monthly,
            '1h': Interval.in_1_hour,
            '4h': Interval.in_4_hour,
            '15m': Interval.in_15_minute,
            '5m': Interval.in_5_minute,
            '30m': Interval.in_30_minute
        }
        
        df = tv.get_hist(
            symbol=symbol,
            exchange=exchange,
            interval=interval_mapping.get(timeframe.lower(), Interval.in_daily),
            n_bars=1000
        )
        
        if df is None or df.empty:
            raise ValueError(f"No data available for {symbol}")
        
        candles = []
        for index, row in df.iterrows():
            timestamp = int(time.mktime(index.timetuple()) * 1000)
            candle = {
                'time': timestamp,
                'open': float(row['open']),
                'high': float(row['high']),
                'low': float(row['low']),
                'close': float(row['close']),
                'volume': float(row['volume'])
            }
            candles.append(candle)
            
        print(f"Successfully returned {len(candles)} candles for {symbol}")
        return jsonify(candles)

    except Exception as e:
        print(f"Error processing request: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/fetch_segment_data', methods=['GET'])
def fetch_segment_data():
    country = request.args.get('country', 'IN')
    segment = request.args.get('segment', 'EQ')
    timeframe = request.args.get('timeframe', '1D')
    
    interval_mapping = {
        '1D': Interval.in_daily,
        '1W': Interval.in_weekly,
        '1M': Interval.in_monthly,
        '1h': Interval.in_1_hour,
        '4h': Interval.in_4_hour,
        '15m': Interval.in_15_minute
    }
    
    interval = interval_mapping.get(timeframe, Interval.in_daily)
    exchanges = segment_data[country][segment]['exchanges']
    segment_tickers_data = {}
    
    for exchange in exchanges:
        symbols = tv.search_symbol(exchange)
        for symbol in symbols:
            df = tv.get_hist(
                symbol=symbol,
                exchange=exchange,
                interval=interval,
                n_bars=300
            )
            segment_tickers_data[symbol] = {
                'open': df['open'].tolist(),
                'high': df['high'].tolist(),
                'low': df['low'].tolist(),
                'close': df['close'].tolist(),
                'volume': df['volume'].tolist(),
                'timestamp': df.index.astype(np.int64) // 10**6
            }
    
    return jsonify({
        'country': country,
        'segment': segment,
        'exchanges': exchanges,
        'data': segment_tickers_data
    })

def format_symbol(symbol):
    """Format symbol for TradingView"""
    # Add exchange prefix if needed
    if ':' not in symbol:
        return f"BINANCE:{symbol}"  # Default to BINANCE, adjust as needed
    return symbol




def process_historical_data(data):
    """Process historical data into candle format"""
    candles = []
    for bar in data:
        candle = {
            'time': int(bar['time']),
            'open': str(bar['open']),
            'high': str(bar['high']),
            'low': str(bar['low']),
            'close': str(bar['close']),
            'volume': str(bar['volume'])
        }
        candles.append(candle)
    return candles






@app.errorhandler(500)
def internal_error(error):
    print(f"Internal Server Error: {str(error)}")
    return jsonify({'error': 'Internal Server Error'}), 500

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({'error': 'Not Found'}), 404

@app.route('/fetch_stock_details', methods=['GET'])
def fetch_stock_details():
    try:
        symbol = request.args.get('symbol')
        
        if not symbol:
            return jsonify({'error': 'Symbol is required'}), 400
            
        print(f"Fetching details for symbol: {symbol}")
        
        ticker = yf.Ticker(symbol)
        info = ticker.info
        
        stock_details = {
            'symbol': symbol,
            'price': float(info.get('currentPrice', info.get('regularMarketPrice', 0))),
            'change': float(info.get('regularMarketChange', 0)),
            'changePercent': float(info.get('regularMarketChangePercent', 0)),
            'companyName': info.get('longName', ''),
            'exchange': info.get('exchange', ''),
            'industry': info.get('industry', ''),
            'lastUpdated': str(info.get('regularMarketTime', '')),
            
            # Price information
            'previousClose': float(info.get('previousClose', 0)),
            'open': float(info.get('open', 0)),
            'dayLow': float(info.get('dayLow', 0)),
            'dayHigh': float(info.get('dayHigh', 0)),
            
            # Volume information
            'volume': float(info.get('volume', 0)),
            'avgVolume': float(info.get('averageVolume', 0)),
            'avgVolume10days': float(info.get('averageVolume10days', 0)),
            
            # Market data
            'marketCap': float(info.get('marketCap', 0)),
            'high52Week': float(info.get('fiftyTwoWeekHigh', 0)),
            'low52Week': float(info.get('fiftyTwoWeekLow', 0)),
            
            # Financial ratios
            'peRatio': float(info.get('trailingPE', 0)) if info.get('trailingPE') else None,
            'forwardPE': float(info.get('forwardPE', 0)) if info.get('forwardPE') else None,
            'eps': float(info.get('trailingEps', 0)) if info.get('trailingEps') else None,
            'forwardEps': float(info.get('forwardEps', 0)) if info.get('forwardEps') else None,
            'dividend': float(info.get('dividendYield', 0)) if info.get('dividendYield') else None,
            'beta': float(info.get('beta', 0)) if info.get('beta') else None,
            'priceToBook': float(info.get('priceToBook', 0)) if info.get('priceToBook') else None,
            'debtToEquity': float(info.get('debtToEquity', 0)) if info.get('debtToEquity') else None,
            'returnOnEquity': float(info.get('returnOnEquity', 0)) if info.get('returnOnEquity') else None,
            'returnOnAssets': float(info.get('returnOnAssets', 0)) if info.get('returnOnAssets') else None,
            'profitMargins': float(info.get('profitMargins', 0)) if info.get('profitMargins') else None,
            'operatingMargins': float(info.get('operatingMargins', 0)) if info.get('operatingMargins') else None,
            
            # Additional info
            'sector': info.get('sector', ''),
            'description': info.get('longBusinessSummary', ''),
            'website': info.get('website', ''),
            'employees': int(info.get('fullTimeEmployees', 0)) if info.get('fullTimeEmployees') else None
        }
        
        return jsonify(stock_details)

    except Exception as e:
        print(f"Error fetching stock details: {str(e)}")
        return jsonify({'error': str(e)}), 500

watchlists = []

@app.route('/watchlists', methods=['GET'])
def get_watchlists():
    return jsonify(watchlists)

@app.route('/watchlist', methods=['POST'])
def watchlist():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Request body is required'}), 400

    if 'name' in data:
        # Creating a new watchlist
        new_watchlist_name = data['name']
        watchlists.append({'name': new_watchlist_name, 'stocks': []})
        return jsonify({'message': f'Watchlist "{new_watchlist_name}" created successfully'}), 201

    elif 'symbols' in data and isinstance(data['symbols'], list):
        # Adding symbols to a watchlist
        symbol_list = data['symbols']
        stocks_data = []
        for symbol in symbol_list:
            try:
                ticker = yf.Ticker(symbol.strip())
                info = ticker.info
                stock_data = {
                    'symbol': symbol.strip(),
                    'last': str(info.get('currentPrice', info.get('regularMarketPrice', 0))),
                    'chg': str(info.get('regularMarketChange', 0)),
                    'chgPercent': str(info.get('regularMarketChangePercent', 0))
                }
                stocks_data.append(stock_data)
            except Exception as e:
                print(f"Error fetching data for {symbol}: {str(e)}")
                continue
        return jsonify(stocks_data)

    else:
        return jsonify({'error': 'Invalid request body'}), 400

@app.route('/fetch_multiple_stocks', methods=['GET'])
def fetch_multiple_stocks():
    try:
        symbols = request.args.get('symbols')
        if not symbols:
            return jsonify({'error': 'Symbols are required'}), 400

        # Split the comma-separated symbols
        symbol_list = symbols.split(',')

        stocks_data = []
        for symbol in symbol_list:
            try:
                ticker = yf.Ticker(symbol.strip())
                info = ticker.info

                stock_data = {
                    'symbol': symbol.strip(),
                    'price': str(info.get('currentPrice', info.get('regularMarketPrice', 0))),
                    'change': str(info.get('regularMarketChange', 0)),
                    'changePercent': str(info.get('regularMarketChangePercent', 0)),
                    'companyName': info.get('longName', '')
                }
                stocks_data.append(stock_data)
            except Exception as e:
                print(f"Error fetching data for {symbol}: {str(e)}")
                continue

        return jsonify(stocks_data)

    except Exception as e:
        print(f"Error processing request: {str(e)}")
        return jsonify(stocks_data)

    except Exception as e:
        print(f"Error processing request: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/get_stock_suggestions', methods=['GET'])
def get_stock_suggestions():
    query = request.args.get('query', '').upper()
    
    try:
        search_url = "https://symbol-search.tradingview.com/symbol_search/"
        params = {
            'text': query,
            'hl': True,
            'exchange': '',
            'lang': 'en',
            'type': 'stock,crypto,forex,futures'  # Added more types for comprehensive search
        }
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json',
            'Referer': 'https://www.tradingview.com/',
            'Origin': 'https://www.tradingview.com',
            'Accept-Language': 'en-US,en;q=0.9'
        }

        response = requests.get(search_url, params=params, headers=headers, timeout=5)
        data = response.json()
        
        # Include the full exchange and symbol info in results
        formatted_results = [{
            'symbol': item['symbol'].replace('<em>', '').replace('</em>', ''),
            'name': item['description'].replace('<em>', '').replace('</em>', ''),
            'exchange': item['exchange'],
            'fullSymbol': f"{item['exchange']}:{item['symbol'].replace('<em>', '').replace('</em>', '')}"
        } for item in data]
        
        return jsonify(formatted_results)
    
    except Exception as e:
        print(f"Search error: {str(e)}")
        return jsonify([])

@app.route('/fetch_financials', methods=['GET'])
def fetch_financials():
    try:
        symbol = request.args.get('symbol')
        
        if not symbol:
            return jsonify({'error': 'Symbol is required'}), 400
            
        print(f"Fetching income statement for symbol: {symbol}")
        
        ticker = yf.Ticker(symbol)
        
        try:
            # Get income statement data with error handling
            annual_income_stmt = ticker.income_stmt
            print(f"Raw income statement data received for {symbol}")
            
            # Validate if we got valid data
            if annual_income_stmt is None or annual_income_stmt.empty:
                return jsonify({'error': f'No financial data available for symbol {symbol}'}), 404

            # Convert DataFrame to dictionary with proper date handling
            def process_dataframe(df):
                if df.empty:
                    return {}
                
                data_dict = {}
                try:
                    # Iterate through rows (metrics)
                    for idx in df.index:
                        metric_data = {}
                        # Iterate through columns (dates)
                        for col in df.columns:
                            try:
                                # Convert timestamp to string format
                                date_key = col.strftime('%Y-%m-%d') if hasattr(col, 'strftime') else str(col)
                                value = df.loc[idx, col]
                                # Convert numpy/pandas types to native Python types
                                if pd.isna(value):
                                    metric_data[date_key] = None
                                else:
                                    metric_data[date_key] = str(float(value))
                            except Exception as e:
                                print(f"Error processing column {col} for metric {idx}: {str(e)}")
                                metric_data[str(col)] = None
                        data_dict[str(idx)] = metric_data
                except Exception as e:
                    print(f"Error processing dataframe: {str(e)}")
                    return {}
                
                return data_dict

            # Process the income statement
            processed_data = process_dataframe(annual_income_stmt)
            
            if not processed_data:
                return jsonify({'error': 'Failed to process financial data'}), 500

            financials = {
                'income_statement': processed_data
            }
            
            print(f"Successfully processed financial data for {symbol}")
            return jsonify(financials)

        except Exception as e:
            print(f"Error processing ticker data for {symbol}: {str(e)}")
            return jsonify({'error': f'Failed to fetch financial data: {str(e)}'}), 500

    except Exception as e:
        print(f"Error in fetch_financials: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/fetch_balance_sheet', methods=['GET'])
def fetch_balance_sheet():
    try:
        symbol = request.args.get('symbol')
        
        if not symbol:
            return jsonify({'error': 'Symbol is required'}), 400
            
        print(f"Fetching balance sheet for symbol: {symbol}")
        
        ticker = yf.Ticker(symbol)
        
        try:
            # Get balance sheet data with error handling
            balance_sheet = ticker.balance_sheet
            print(f"Raw balance sheet data received for {symbol}")
            
            # Validate if we got valid data
            if balance_sheet is None or balance_sheet.empty:
                return jsonify({'error': f'No balance sheet data available for symbol {symbol}'}), 404

            # Convert DataFrame to dictionary with proper date handling
            def process_dataframe(df):
                if df.empty:
                    return {}
                
                data_dict = {}
                try:
                    # Iterate through rows (metrics)
                    for idx in df.index:
                        metric_data = {}
                        # Iterate through columns (dates)
                        for col in df.columns:
                            try:
                                # Convert timestamp to string format
                                date_key = col.strftime('%Y-%m-%d') if hasattr(col, 'strftime') else str(col)
                                value = df.loc[idx, col]
                                # Convert numpy/pandas types to native Python types
                                if pd.isna(value):
                                    metric_data[date_key] = None
                                else:
                                    metric_data[date_key] = str(float(value))
                            except Exception as e:
                                print(f"Error processing column {col} for metric {idx}: {str(e)}")
                                metric_data[str(col)] = None
                        data_dict[str(idx)] = metric_data
                except Exception as e:
                    print(f"Error processing dataframe: {str(e)}")
                    return {}
                
                return data_dict

            # Process the balance sheet
            processed_data = process_dataframe(balance_sheet)
            
            if not processed_data:
                return jsonify({'error': 'Failed to process balance sheet data'}), 500

            balance_sheet_data = {
                'balance_sheet': processed_data
            }
            
            print(f"Successfully processed balance sheet data for {symbol}")
            return jsonify(balance_sheet_data)

        except Exception as e:
            print(f"Error processing ticker data for {symbol}: {str(e)}")
            return jsonify({'error': f'Failed to fetch balance sheet data: {str(e)}'}), 500

    except Exception as e:
        print(f"Error in fetch_balance_sheet: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/fetch_cash_flow', methods=['GET'])
def fetch_cash_flow():
    try:
        symbol = request.args.get('symbol')
        
        if not symbol:
            return jsonify({'error': 'Symbol is required'}), 400
            
        print(f"Fetching cash flow for symbol: {symbol}")
        
        ticker = yf.Ticker(symbol)
        
        try:
            # Get cash flow data with error handling
            cash_flow = ticker.cashflow
            print(f"Raw cash flow data received for {symbol}")
            
            # Validate if we got valid data
            if cash_flow is None or cash_flow.empty:
                return jsonify({'error': f'No cash flow data available for symbol {symbol}'}), 404

            # Convert DataFrame to dictionary with proper date handling
            def process_dataframe(df):
                if df.empty:
                    return {}
                
                data_dict = {}
                try:
                    # Iterate through rows (metrics)
                    for idx in df.index:
                        metric_data = {}
                        # Iterate through columns (dates)
                        for col in df.columns:
                            try:
                                # Convert timestamp to string format
                                date_key = col.strftime('%Y-%m-%d') if hasattr(col, 'strftime') else str(col)
                                value = df.loc[idx, col]
                                # Convert numpy/pandas types to native Python types
                                if pd.isna(value):
                                    metric_data[date_key] = None
                                else:
                                    metric_data[date_key] = str(float(value))
                            except Exception as e:
                                print(f"Error processing column {col} for metric {idx}: {str(e)}")
                                metric_data[str(col)] = None
                        data_dict[str(idx)] = metric_data
                except Exception as e:
                    print(f"Error processing dataframe: {str(e)}")
                    return {}
                
                return data_dict

            # Process the cash flow
            processed_data = process_dataframe(cash_flow)
            
            if not processed_data:
                return jsonify({'error': 'Failed to process cash flow data'}), 500

            cash_flow_data = {
                'cash_flow': processed_data
            }
            
            print(f"Successfully processed cash flow data for {symbol}")
            return jsonify(cash_flow_data)

        except Exception as e:
            print(f"Error processing ticker data for {symbol}: {str(e)}")
            return jsonify({'error': f'Failed to fetch cash flow data: {str(e)}'}), 500

    except Exception as e:
        print(f"Error in fetch_cash_flow: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/fetch_statistics', methods=['GET'])
def fetch_statistics():
    try:
        symbol = request.args.get('symbol')
        
        if not symbol:
            return jsonify({'error': 'Symbol is required'}), 400
            
        print(f"Fetching statistics for symbol: {symbol}")
        
        ticker = yf.Ticker(symbol)
        stats = ticker.stats()
        
        if not stats:
            return jsonify({'error': f'No statistics data found for symbol {symbol}'}), 404
        
        # Include ticker info
        ticker_info = ticker.info
        
        statistics_data = {
            'stats': stats,
            'ticker_info': ticker_info
        }
        
        return jsonify(statistics_data)

    except Exception as e:
        print(f"Error fetching statistics: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/market_segments', methods=['GET'])
def get_market_segments():
    country = request.args.get('country', 'IN')
    segment = request.args.get('segment', 'EQ')
    
    tv = TvDatafeed()
    exchanges = segment_data[country][segment]['exchanges']
    symbols = []
    
    for exchange in exchanges:
        exchange_symbols = tv.search_symbol(exchange)
        symbols.extend(exchange_symbols)
    
    return jsonify({
        'country': country,
        'segment': segment,
        'exchanges': exchanges,
        'symbols': symbols
    })

def fetch_candle_data(symbol, timeframe):
    response = requests.get(f'http://localhost:5000/fetch_candles?symbol={symbol}&timeframe={timeframe}')
    return response.json()

def calculate_technicals(candle_data):
    close_prices = np.array([candle['close'] for candle in candle_data])
    high_prices = np.array([candle['high'] for candle in candle_data])
    low_prices = np.array([candle['low'] for candle in candle_data])
    volume = np.array([candle['volume'] for candle in candle_data])

    def safe_talib_function(func, *args, **kwargs):
        result = func(*args, **kwargs)
        return np.nan_to_num(result).tolist()

    technicals = {
        'moving_averages': {
            'SMA': {
                'SMA10': safe_talib_function(talib.SMA, close_prices, timeperiod=10),
                'SMA20': safe_talib_function(talib.SMA, close_prices, timeperiod=20),
                'SMA30': safe_talib_function(talib.SMA, close_prices, timeperiod=30),
                'SMA50': safe_talib_function(talib.SMA, close_prices, timeperiod=50),
                'SMA100': safe_talib_function(talib.SMA, close_prices, timeperiod=100),
                'SMA200': safe_talib_function(talib.SMA, close_prices, timeperiod=200),
            },
            'EMA': {
                'EMA10': safe_talib_function(talib.EMA, close_prices, timeperiod=10),
                'EMA20': safe_talib_function(talib.EMA, close_prices, timeperiod=20),
                'EMA30': safe_talib_function(talib.EMA, close_prices, timeperiod=30),
                'EMA50': safe_talib_function(talib.EMA, close_prices, timeperiod=50),
                'EMA100': safe_talib_function(talib.EMA, close_prices, timeperiod=100),
                'EMA200': safe_talib_function(talib.EMA, close_prices, timeperiod=200),
            },
            'VWMA': {
                'VWMA20': safe_talib_function(talib.WMA, close_prices, timeperiod=20),
            },
            'HMA': {
                'HMA9': safe_talib_function(talib.WMA, close_prices, timeperiod=9),
            },
        },
        'oscillators': {
            'RSI': safe_talib_function(talib.RSI, close_prices, timeperiod=14),
            'MACD': {
                'macd': safe_talib_function(talib.MACD, close_prices)[0],
                'signal': safe_talib_function(talib.MACD, close_prices)[1],
                'hist': safe_talib_function(talib.MACD, close_prices)[2],
            },
            'Stochastic': {
                'slowk': safe_talib_function(talib.STOCH, high_prices, low_prices, close_prices)[0],
                'slowd': safe_talib_function(talib.STOCH, high_prices, low_prices, close_prices)[1],
            },
            'CCI': safe_talib_function(talib.CCI, high_prices, low_prices, close_prices),
            'ADX': safe_talib_function(talib.ADX, high_prices, low_prices, close_prices),
            'Williams%R': safe_talib_function(talib.WILLR, high_prices, low_prices, close_prices),
            
            'Momentum': safe_talib_function(talib.MOM, close_prices, timeperiod=10),
            'StochRSI': {
                'fastk': safe_talib_function(talib.STOCHRSI, close_prices)[0],
                'fastd': safe_talib_function(talib.STOCHRSI, close_prices)[1],
            },
            'BullBearPower': safe_talib_function(talib.BBANDS, close_prices)[0],
            'UltimateOscillator': safe_talib_function(talib.ULTOSC, high_prices, low_prices, close_prices, timeperiod1=7, timeperiod2=14, timeperiod3=28),
        },
        'pivots': {
            'Classic': safe_talib_function(talib.PIVOT, high_prices, low_prices, close_prices),
            'Fibonacci': safe_talib_function(talib.PIVOT, high_prices, low_prices, close_prices, type='fibonacci'),
            'Camarilla': safe_talib_function(talib.PIVOT, high_prices, low_prices, close_prices, type='camarilla'),
            'Woodie': safe_talib_function(talib.PIVOT, high_prices, low_prices, close_prices, type='woodie'),
            'DM': safe_talib_function(talib.PIVOT, high_prices, low_prices, close_prices, type='dm'),
        }
    }
    
    return technicals

@app.route('/fetch_technicals', methods=['GET'])
def fetch_technicals():
    symbol = request.args.get('symbol')
    timeframe = request.args.get('timeframe', '1d')
    
    if not symbol:
        return jsonify({'error': 'Symbol is required'}), 400
    
    candle_data = fetch_candle_data(symbol, timeframe)
    if isinstance(candle_data, dict) and 'error' in candle_data:
        return jsonify(candle_data), 500
    
    technicals = calculate_technicals(candle_data)
    
    return jsonify(technicals)

if __name__ == '__main__':
    app.run(debug=True, port=5000)