from flask import Flask, request
import yfinance as yf

app = Flask(__name__)

@app.route("/stock-data")
def get_stock_data():
    symbol = request.args.get('symbol', default="AAPL")
    period = request.args.get('period', default="1y")
    interval = request.args.get('interval', default="1mo")
    quote = yf.Ticker(symbol)
    hist = quote.history(period=period, interval=interval)
    data = hist.to_json()
    return data

if __name__ == "__main__":
    app.run(debug=True)