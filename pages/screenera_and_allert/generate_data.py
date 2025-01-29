import json
from ScreenerData import get_market_data
from Screener_Builder import ScreenerBuilder
import sys

def generate_and_save_data(formula, country, segment, timeframe):
    
    screener = ScreenerBuilder()
    results = screener.screen_stocks(formula, country, segment, timeframe)
    
    with open('market_data.json', 'w') as f:
        json.dump(results, f)

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python generate_data.py <formula> <country> <segment> <timeframe>")
        sys.exit(1)
    
    formula = sys.argv[1]
    country = sys.argv[2]
    segment = sys.argv[3]
    timeframe = sys.argv[4]
    
    generate_and_save_data(formula, country, segment, timeframe)
