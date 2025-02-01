from tvDatafeed import TvDatafeed, Interval

tv = TvDatafeed()
df=tv.get_hist(symbol="AAPL", exchange="NASDAQ", interval=Interval.in_daily, n_bars=1000)   
print(df)

@app.route('/screen_stocks', methods=['POST'])
def screen_stocks():
    try:
        data = request.get_json()
        formula = data['formula']
        segment_data = data['segment']
        market_data = data['market_data']
        
        screener = ScreenerBuilder()
        matching_stocks = screener.screen_stocks(formula, segment_data)
        
        return jsonify(matching_stocks)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/fetch_segment_data', methods=['GET'])
def fetch_segment_data():
    try:
        country = request.args.get('country', 'IN')
        segment = request.args.get('segment', 'EQ')
        timeframe = request.args.get('timeframe', '1D')
        
        # Get exchanges for the segment
        exchanges = segment_data[country][segment]['exchanges']
        
        # Initialize data container
        segment_tickers_data = {}
        
        for exchange in exchanges:
            # Use tvDatafeed for reliable data fetching
            interval_mapping = {
                '1D': Interval.in_daily,
                '1W': Interval.in_weekly,
                '1M': Interval.in_monthly,
                '1h': Interval.in_1_hour,
                '4h': Interval.in_4_hour,
                '15m': Interval.in_15_minute
            }
            
            interval = interval_mapping.get(timeframe, Interval.in_daily)
            
            # Get symbols for this exchange
            symbols = tv.search_symbol(exchange)
            
            for symbol in symbols:
                try:
                    df = tv.get_hist(
                        symbol=symbol,
                        exchange=exchange,
                        interval=interval,
                        n_bars=300
                    )
                    
                    # Format data
                    ticker_data = {
                        'open': df['open'].tolist(),
                        'high': df['high'].tolist(),
                        'low': df['low'].tolist(),
                        'close': df['close'].tolist(),
                        'volume': df['volume'].tolist(),
                        'timestamp': df.index.astype(np.int64) // 10**6
                    }
                    
                    segment_tickers_data[symbol] = ticker_data
                    
                except Exception as e:
                    print(f"Error fetching data for {symbol}: {str(e)}")
                    continue
        
        return jsonify({
            'country': country,
            'segment': segment,
            'exchanges': exchanges,
            'data': segment_tickers_data
        })
        
    except Exception as e:
        print(f"Error fetching segment data: {str(e)}")
        return jsonify({'error': str(e)}), 500
