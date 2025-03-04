// Trading Strategy Template
strategy("Custom Strategy", overlay=true)

// Parameters
fast_length = input(10, "Fast MA")
slow_length = input(20, "Slow MA")

// Calculations
fast_ma = ta.sma(close, fast_length)
slow_ma = ta.sma(close, slow_length)

// Trading Logic
if ta.crossover(fast_ma, slow_ma)
    strategy.entry("Long", strategy.long)

if ta.crossunder(fast_ma, slow_ma)
    strategy.close("Long")
