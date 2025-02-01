export const indicatorGroups: IndicatorGroup[] = [
  {
    name: 'Price',
    indicators: {
      close: {
        name: 'Close Price',
        operators: ['>', '<', '>=', '<=', '==', 'crosses above', 'crosses below'],
      },
      open: {
        name: 'Open Price',
        operators: ['>', '<', '>=', '<=', '=='],
      }
    }
  },
  {
    name: 'Moving Averages',
    indicators: {
      sma: {
        name: 'Simple Moving Average',
        parameters: [5, 10, 20, 50, 100, 200],
        operators: ['crosses above', 'crosses below', '>', '<'],
        defaultValue: 20
      },
      ema: {
        name: 'Exponential Moving Average',
        parameters: [5, 10, 20, 50, 100, 200],
        operators: ['crosses above', 'crosses below', '>', '<'],
        defaultValue: 20
      }
    }
  },
  {
    name: 'Momentum',
    indicators: {
      rsi: {
        name: 'RSI',
        parameters: [14, 21, 28],
        operators: ['>', '<', 'crosses above', 'crosses below'],
        defaultValue: 14
      },
      macd: {
        name: 'MACD',
        operators: ['crosses above', 'crosses below', 'is positive', 'is negative'],
      }
    }
  }
];
