import talib
import numpy as np

# Create sample data
close_prices = np.array([10.0, 12.0, 15.0, 14.0, 13.0, 16.0, 15.0, 17.0, 19.0, 20.0])

# Calculate a simple moving average
sma = talib.SMA(close_prices, timeperiod=3)

print("TA-Lib is working! Here's a 3-period SMA calculation:")
print(sma)
