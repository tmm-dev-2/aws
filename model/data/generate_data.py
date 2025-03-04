import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import plotly.graph_objects as go
from PIL import Image
import os

def generate_chart_images(symbol, start_date, end_date, output_dir):
    # Fetch data
    data = yf.download(symbol, start=start_date, end=end_date)
    
    # Generate charts with patterns
    patterns = []
    
    for i in range(0, len(data)-30, 30):
        chunk = data.iloc[i:i+30]
        
        fig = go.Figure(data=[go.Candlestick(
            x=chunk.index,
            open=chunk['Open'],
            high=chunk['High'],
            low=chunk['Low'],
            close=chunk['Close']
        )])
        
        # Save chart
        img_path = f"{output_dir}/{symbol}_{i}.png"
        fig.write_image(img_path)
        
        # Detect patterns (simplified)
        pattern = detect_pattern(chunk)
        
        patterns.append({
            'image_file': f"{symbol}_{i}.png",
            'pattern': pattern,
            'date': chunk.index[-1]
        })
    
    return pd.DataFrame(patterns)

def detect_pattern(data):
    # Simplified pattern detection
    patterns = ['bullish_engulfing', 'bearish_engulfing', 'doji', 'hammer']
    return np.random.choice(patterns)

if __name__ == "__main__":
    os.makedirs("data/images", exist_ok=True)
    
    symbols = ['AAPL', 'GOOGL', 'MSFT']
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    
    all_patterns = []
    
    for symbol in symbols:
        patterns_df = generate_chart_images(
            symbol,
            start_date,
            end_date,
            "data/images"
        )
        all_patterns.append(patterns_df)
    
    final_df = pd.concat(all_patterns)
    final_df.to_csv("data/annotations.csv", index=False)
