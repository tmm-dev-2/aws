export const stocksList = ['RELIANCE', 'TCS', 'HDFCBANK', 'INFY', 'ICICIBANK', 'HDFC', 'ITC', 'KOTAKBANK', 'LT', 'HINDUNILVR'];

export const stockData = {
  'RELIANCE': {
    timeframes: {
      '1d': {
        price: [2500, 2520, 2480, 2510, 2530],
        volume: [5000000, 5200000, 4800000, 5100000, 5300000],
        rsi: [62, 65, 58, 63, 67],
        sma20: [2450, 2460, 2470, 2480, 2490],
        ema20: [2455, 2465, 2475, 2485, 2495],
        macd: [15, 18, 12, 16, 20],
        macdSignal: [14, 16, 13, 15, 18]
      },
      '1h': {
        // Similar structure for hourly data
      }
    }
  },
  'TCS': {
    timeframes: {
      '1d': {
        price: [3500, 3520, 3480, 3510, 3530],
        volume: [2000000, 2200000, 1800000, 2100000, 2300000],
        rsi: [58, 60, 55, 59, 62],
        sma20: [3450, 3460, 3470, 3480, 3490],
        ema20: [3455, 3465, 3475, 3485, 3495],
        macd: [10, 12, 8, 11, 14],
        macdSignal: [9, 11, 9, 10, 12]
      }
    }
  }
  // Add more stocks with similar structure
};

export const indicatorDefaults = {
  sma: [5, 10, 20, 50, 200],
  rsi: [14, 21, 28],
  macd: {
    fast: 12,
    slow: 26,
    signal: 9
  }
};

export const timeframes = ['1m', '5m', '15m', '1h', '1d', '1w'];
