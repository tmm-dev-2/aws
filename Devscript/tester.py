def _calculate_market_data(self):
    """
    Calculate all market data related values including OHLCV, symbol info, and derived price calculations
    """
    market_data = {
        # Basic OHLCV
        'open': self.current_bar.open,
        'high': self.current_bar.high,
        'low': self.current_bar.low,
        'close': self.current_bar.close,
        'volume': self.current_bar.volume,
        
        # Derived price calculations
        'hl2': (self.current_bar.high + self.current_bar.low) / 2,
        'hlc3': (self.current_bar.high + self.current_bar.low + self.current_bar.close) / 3, 
        'hlcc4': (self.current_bar.high + self.current_bar.low + self.current_bar.close + self.current_bar.close) / 4,
        'ohlc4': (self.current_bar.open + self.current_bar.high + self.current_bar.low + self.current_bar.close) / 4,
        
        # Symbol information
        'symInfoMinMove': self.symbol.min_move,
        'symInfoMinTick': self.symbol.min_tick,
        'symInfoPointValue': self.symbol.point_value,
        'symInfoPrefix': self.symbol.prefix,
        'symInfoPriceScale': self.symbol.price_scale,
        'symInfoRoot': self.symbol.root,
        'symInfoSector': self.symbol.sector,
        'symInfoSession': self.symbol.session,
        'symInfoShareholders': self.symbol.shareholders,
        'symInfoSharesOutstandingFloat': self.symbol.shares_outstanding_float,
        'symInfoSharesOutstandingTotal': self.symbol.shares_outstanding_total,
        
        # Additional symbol metadata
        'symInfoBaseCurrency': self.symbol.base_currency,
        'symInfoCountry': self.symbol.country,
        'symInfoCurrency': self.symbol.currency,
        'symInfoDescription': self.symbol.description,
        'symInfoEmployees': self.symbol.employees,
        'symInfoExpirationDate': self.symbol.expiration_date,
        'symInfoIndustry': self.symbol.industry,
        'symInfoMainTickerId': self.symbol.main_ticker_id,
        'symInfoMinContract': self.symbol.min_contract,
        
        # Market recommendations
        'symInfoRecommendationsBuy': self.symbol.recommendations_buy,
        'symInfoRecommendationsBuyStrong': self.symbol.recommendations_buy_strong,
        'symInfoRecommendationsDate': self.symbol.recommendations_date,
        'symInfoRecommendationsHold': self.symbol.recommendations_hold,
        'symInfoRecommendationsSell': self.symbol.recommendations_sell,
        'symInfoRecommendationsSellStrong': self.symbol.recommendations_sell_strong,
        'symInfoRecommendationsTotal': self.symbol.recommendations_total,
        
        # Price targets
        'symInfoTargetPriceAverage': self.symbol.target_price_average,
        'symInfoTargetPriceDate': self.symbol.target_price_date,
        'symInfoTargetPriceEstimates': self.symbol.target_price_estimates,
        'symInfoTargetPriceHigh': self.symbol.target_price_high,
        'symInfoTargetPriceLow': self.symbol.target_price_low,
        'symInfoTargetPriceMedian': self.symbol.target_price_median,
        
        # Additional identifiers
        'symInfoTicker': self.symbol.ticker,
        'symInfoTickerId': self.symbol.ticker_id,
        'symInfoTimezone': self.symbol.timezone,
        'symInfoType': self.symbol.type,
        'symInfoVolumeType': self.symbol.volume_type,
        
        # Bar state information
        'barStateIsConfirmed': self.current_bar.is_confirmed,
        'barStateIsFirst': self.current_bar.is_first,
        'barStateIsHistory': self.current_bar.is_history,
        'barStateIsLast': self.current_bar.is_last,
        'barStateIsLastConfirmedHistory': self.current_bar.is_last_confirmed_history,
        'barStateIsNew': self.current_bar.is_new,
        'barStateIsRealtime': self.current_bar.is_realtime,
        
        # Bar indexing
        'barIndex': self.current_bar.index,
        'lastBarIndex': self.last_bar_index,
        'lastBarTime': self.last_bar_time
    }
    
    return market_data.get(self.current_syntax) if self.current_syntax else market_data




























def _handle_ta_operation(self, operation, args):
    """
    Technical Analysis handler with syntax validation and calculations
    """
    # Basic Technical Indicators
    if operation == 'sma':
        source = args[0]
        length = args[1]
        return sum(source[-length:]) / length
        
    if operation == 'ema':
        source = args[0]
        length = args[1]
        alpha = 2 / (length + 1)
        result = source[0]
        for value in source[1:]:
            result = alpha * value + (1 - alpha) * result
        return result
        
    if operation == 'rsi':
        source = args[0]
        length = args[1]
        changes = [source[i] - source[i-1] for i in range(1, len(source))]
        gains = [max(0, change) for change in changes]
        losses = [abs(min(0, change)) for change in changes]
        avg_gain = sum(gains[-length:]) / length
        avg_loss = sum(losses[-length:]) / length
        rs = avg_gain / avg_loss if avg_loss != 0 else float('inf')
        return 100 - (100 / (1 + rs))

    # Volume Analysis
    if operation == 'taAccDist':
        high, low, close, volume = args
        mfm = ((close - low) - (high - close)) / (high - low) if high != low else 0
        return mfm * volume
        
    if operation == 'taOBV':
        close, volume = args
        prev_close = close[-1]
        if close > prev_close:
            return volume
        elif close < prev_close:
            return -volume
        return 0
        
    if operation == 'taVWAP':
        high, low, close, volume = args
        typical_price = (high + low + close) / 3
        return sum(typical_price * volume) / sum(volume)

    # Momentum Indicators
    if operation == 'taMom':
        source = args[0]
        length = args[1]
        return source[-1] - source[-length]
        
    if operation == 'taCci':
        high, low, close, length = args
        typical_price = (high + low + close) / 3
        sma = sum(typical_price[-length:]) / length
        mean_deviation = sum(abs(price - sma) for price in typical_price[-length:]) / length
        return (typical_price[-1] - sma) / (0.015 * mean_deviation)
        
    if operation == 'taRoc':
        source = args[0]
        length = args[1]
        return ((source[-1] - source[-length]) / source[-length]) * 100

    # Volatility Indicators
    if operation == 'taAtr':
        high, low, close, length = args
        tr = max(
            high - low,
            abs(high - close[-1]),
            abs(low - close[-1])
        )
        return sum(tr[-length:]) / length
        
    if operation == 'taBb':
        source, length, mult = args
        sma = sum(source[-length:]) / length
        std = (sum((x - sma) ** 2 for x in source[-length:]) / length) ** 0.5
        return {
            'middle': sma,
            'upper': sma + (mult * std),
            'lower': sma - (mult * std)
        }

    # Trend Indicators
    if operation == 'taDmi':
        high, low, close, length = args
        tr = max(high - low, abs(high - close[-1]), abs(low - close[-1]))
        plus_dm = max(0, high - high[-1]) if high - high[-1] > low[-1] - low else 0
        minus_dm = max(0, low[-1] - low) if low[-1] - low > high - high[-1] else 0
        tr_sum = sum(tr[-length:])
        plus_di = 100 * sum(plus_dm[-length:]) / tr_sum
        minus_di = 100 * sum(minus_dm[-length:]) / tr_sum
        return {
            'plus_di': plus_di,
            'minus_di': minus_di,
            'adx': abs(plus_di - minus_di) / (plus_di + minus_di) * 100
        }

    # Statistical Indicators
    if operation == 'taStdev':
        source = args[0]
        length = args[1]
        mean = sum(source[-length:]) / length
        return (sum((x - mean) ** 2 for x in source[-length:]) / length) ** 0.5
        
    if operation == 'taVariance':
        source = args[0]
        length = args[1]
        mean = sum(source[-length:]) / length
        return sum((x - mean) ** 2 for x in source[-length:]) / length
        
    if operation == 'taMedian':
        source = args[0]
        length = args[1]
        sorted_values = sorted(source[-length:])
        mid = length // 2
        return sorted_values[mid] if length % 2 else (sorted_values[mid-1] + sorted_values[mid]) / 2

    # Range Indicators
    if operation == 'taHighest':
        source = args[0]
        length = args[1]
        return max(source[-length:])
        
    if operation == 'taLowest':
        source = args[0]
        length = args[1]
        return min(source[-length:])
        
    if operation == 'taRange':
        source = args[0]
        length = args[1]
        return max(source[-length:]) - min(source[-length:])

        # Moving Average Variants
    if operation == 'taWma':
        source, length = args
        weights = list(range(1, length + 1))
        weight_sum = sum(weights)
        return sum(source[-i] * weights[i-1] for i in range(1, length + 1)) / weight_sum
        
    if operation == 'taHma':
        source, length = args
        wma1 = self._handle_ta_operation('taWma', [source, length//2])
        wma2 = self._handle_ta_operation('taWma', [source, length])
        diff = [2 * wma1[i] - wma2[i] for i in range(len(wma1))]
        return self._handle_ta_operation('taWma', [diff, int(length**0.5)])
        
    if operation == 'taAlma':
        source, length, offset, sigma = args
        m = offset * (length - 1)
        s = length / sigma
        weights = [exp(-((i - m)**2) / (2 * s**2)) for i in range(length)]
        weight_sum = sum(weights)
        return sum(source[-i] * weights[i-1] for i in range(1, length + 1)) / weight_sum

    # Oscillators
    if operation == 'taMfi':
        high, low, close, volume, length = args
        typical_price = [(h + l + c) / 3 for h, l, c in zip(high, low, close)]
        money_flow = [tp * v for tp, v in zip(typical_price, volume)]
        pos_flow = sum(mf for mf, tp, ptp in zip(money_flow[-length:], typical_price[-length:], typical_price[-length-1:]) if tp > ptp)
        neg_flow = sum(mf for mf, tp, ptp in zip(money_flow[-length:], typical_price[-length:], typical_price[-length-1:]) if tp < ptp)
        return 100 * pos_flow / (pos_flow + neg_flow) if (pos_flow + neg_flow) > 0 else 50
        
    if operation == 'taWpr':
        high, low, close, length = args
        highest = max(high[-length:])
        lowest = min(low[-length:])
        return -100 * (highest - close[-1]) / (highest - lowest) if (highest - lowest) > 0 else 0

    # Trend Strength
    if operation == 'taTsi':
        source, short_length, long_length = args
        momentum = [source[i] - source[i-1] for i in range(1, len(source))]
        smooth1 = self._handle_ta_operation('taEma', [momentum, long_length])
        smooth2 = self._handle_ta_operation('taEma', [smooth1, short_length])
        abs_momentum = [abs(m) for m in momentum]
        abs_smooth1 = self._handle_ta_operation('taEma', [abs_momentum, long_length])
        abs_smooth2 = self._handle_ta_operation('taEma', [abs_smooth1, short_length])
        return 100 * smooth2[-1] / abs_smooth2[-1] if abs_smooth2[-1] != 0 else 0
        
    if operation == 'taCmo':
        source, length = args
        changes = [source[i] - source[i-1] for i in range(1, len(source))]
        pos_sum = sum(ch for ch in changes[-length:] if ch > 0)
        neg_sum = abs(sum(ch for ch in changes[-length:] if ch < 0))
        return 100 * (pos_sum - neg_sum) / (pos_sum + neg_sum) if (pos_sum + neg_sum) > 0 else 0

    # Pattern Recognition
    if operation == 'taCross':
        source1, source2 = args
        return source1[-2] < source2[-2] and source1[-1] > source2[-1]
        
    if operation == 'taCrossover':
        source1, source2 = args
        return source1[-2] <= source2[-2] and source1[-1] > source2[-1]
        
    if operation == 'taCrossunder':
        source1, source2 = args
        return source1[-2] >= source2[-2] and source1[-1] < source2[-1]

    # Pivot Points
    if operation == 'taPivotHigh':
        source, leftbars, rightbars = args
        if len(source) < leftbars + rightbars + 1:
            return None
        center = source[-rightbars-1]
        left_range = source[-(leftbars+rightbars+1):-rightbars-1]
        right_range = source[-rightbars:]
        return center if all(center >= x for x in left_range + right_range) else None
        
    if operation == 'taPivotLow':
        source, leftbars, rightbars = args
        if len(source) < leftbars + rightbars + 1:
            return None
        center = source[-rightbars-1]
        left_range = source[-(leftbars+rightbars+1):-rightbars-1]
        right_range = source[-rightbars:]
        return center if all(center <= x for x in left_range + right_range) else None

    # Correlation and Regression
    if operation == 'taCorrelation':
        source1, source2, length = args
        if len(source1) < length or len(source2) < length:
            return None
        mean1 = sum(source1[-length:]) / length
        mean2 = sum(source2[-length:]) / length
        covar = sum((x - mean1) * (y - mean2) for x, y in zip(source1[-length:], source2[-length:]))
        std1 = sum((x - mean1)**2 for x in source1[-length:]) ** 0.5
        std2 = sum((x - mean2)**2 for x in source2[-length:]) ** 0.5
        return covar / (std1 * std2) if std1 * std2 != 0 else 0
        
    if operation == 'taLinReg':
        source, length = args
        x = list(range(length))
        y = source[-length:]
        mean_x = sum(x) / length
        mean_y = sum(y) / length
        covar = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
        var_x = sum((xi - mean_x)**2 for xi in x)
        slope = covar / var_x if var_x != 0 else 0
        intercept = mean_y - slope * mean_x
        return slope * (length - 1) + intercept

        # Supertrend Indicator
    if operation == 'taSuperTrend':
        high, low, close, length, multiplier = args
        atr = self._handle_ta_operation('taAtr', [high, low, close, length])
        hl2 = [(h + l) / 2 for h, l in zip(high, low)]
        
        upper_band = [hl + multiplier * atr for hl in hl2]
        lower_band = [hl - multiplier * atr for hl in hl2]
        
        trend = [1]  # 1 for uptrend, -1 for downtrend
        supertrend = [lower_band[0]]
        
        for i in range(1, len(close)):
            if close[i] > supertrend[i-1]:
                trend.append(1)
            elif close[i] < supertrend[i-1]:
                trend.append(-1)
            else:
                trend.append(trend[i-1])
                
            if trend[i] == 1:
                supertrend.append(min(lower_band[i], supertrend[i-1]))
            else:
                supertrend.append(max(upper_band[i], supertrend[i-1]))
                
        return supertrend[-1]

    # Value When Condition
    if operation == 'taValueWhen':
        condition, source = args
        for i in range(len(condition)-1, -1, -1):
            if condition[i]:
                return source[i]
        return None

    # Bars Since Condition
    if operation == 'taBarsSince':
        condition = args[0]
        count = 0
        for i in range(len(condition)-1, -1, -1):
            if condition[i]:
                return count
            count += 1
        return count

    # Rising/Falling Detection
    if operation == 'taRising':
        source, length = args
        return all(source[i] > source[i-1] for i in range(-1, -length-1, -1))
        
    if operation == 'taFalling':
        source, length = args
        return all(source[i] < source[i-1] for i in range(-1, -length-1, -1))

    # Center of Gravity
    if operation == 'taCog':
        source, length = args
        weighted_sum = sum(source[-i] * i for i in range(1, length + 1))
        total_sum = sum(source[-length:])
        return -weighted_sum / total_sum if total_sum != 0 else 0

    # Percentile and Rank
    if operation == 'taPercentile':
        source, length, percentage = args
        sorted_values = sorted(source[-length:])
        index = (length - 1) * percentage / 100
        return sorted_values[int(index)]
        
    if operation == 'taPercentRank':
        source, length = args
        current = source[-1]
        history = source[-length:]
        return sum(1 for x in history if x < current) * 100 / length

    # Keltner Channels
    if operation == 'taKc':
        high, low, close, length, mult = args
        basis = self._handle_ta_operation('taEma', [close, length])
        atr = self._handle_ta_operation('taAtr', [high, low, close, length])
        
        return {
            'middle': basis,
            'upper': basis + mult * atr,
            'lower': basis - mult * atr
        }
        
    if operation == 'taKcw':
        high, low, close, length = args
        return self._handle_ta_operation('taKc', [high, low, close, length, 1.0])

    # Smoothed Moving Average
    if operation == 'taSwma':
        source = args[0]
        weights = [0.4, 0.3, 0.2, 0.1]
        if len(source) < 4:
            return None
        return sum(w * p for w, p in zip(weights, source[-4:]))

    # Running Moving Average
    if operation == 'taRma':
        source, length = args
        alpha = 1 / length
        result = source[0]
        for value in source[1:]:
            result = alpha * value + (1 - alpha) * result
        return result

    # Cumulative Sum
    if operation == 'taCum':
        source = args[0]
        return sum(source)

    # Change Over Time
    if operation == 'taChange':
        source, length = args
        return source[-1] - source[-length]

    return None



















def _handle_ticker_operation(self, operation, args):
    """
    Handles all ticker and symbol related operations
    """
    # Basic Symbol Info
    if operation == 'symInfoMinMove':
        return self.symbol.min_move
        
    if operation == 'symInfoMinTick':
        return self.symbol.min_tick
        
    if operation == 'symInfoPointValue':
        return self.symbol.point_value
        
    if operation == 'symInfoPrefix':
        return self.symbol.prefix
        
    if operation == 'symInfoPriceScale':
        return self.symbol.price_scale
        
    if operation == 'symInfoRoot':
        return self.symbol.root
        
    if operation == 'symInfoSector':
        return self.symbol.sector
        
    if operation == 'symInfoSession':
        return self.symbol.session

    # Company Information
    if operation == 'symInfoBaseCurrency':
        return self.symbol.base_currency
        
    if operation == 'symInfoCountry':
        return self.symbol.country
        
    if operation == 'symInfoCurrency':
        return self.symbol.currency
        
    if operation == 'symInfoDescription':
        return self.symbol.description
        
    if operation == 'symInfoEmployees':
        return self.symbol.employees
        
    if operation == 'symInfoIndustry':
        return self.symbol.industry

    # Market Data
    if operation == 'symInfoMainTickerId':
        return self.symbol.main_ticker_id
        
    if operation == 'symInfoMinContract':
        return self.symbol.min_contract
        
    if operation == 'symInfoType':
        return self.symbol.type
        
    if operation == 'symInfoVolumeType':
        return self.symbol.volume_type

    # Share Statistics
    if operation == 'symInfoShareholders':
        return self.symbol.shareholders
        
    if operation == 'symInfoSharesOutstandingFloat':
        return self.symbol.shares_outstanding_float
        
    if operation == 'symInfoSharesOutstandingTotal':
        return self.symbol.shares_outstanding_total

    # Analyst Recommendations
    if operation == 'symInfoRecommendationsBuy':
        return self.symbol.recommendations_buy
        
    if operation == 'symInfoRecommendationsBuyStrong':
        return self.symbol.recommendations_buy_strong
        
    if operation == 'symInfoRecommendationsDate':
        return self.symbol.recommendations_date
        
    if operation == 'symInfoRecommendationsHold':
        return self.symbol.recommendations_hold
        
    if operation == 'symInfoRecommendationsSell':
        return self.symbol.recommendations_sell
        
    if operation == 'symInfoRecommendationsSellStrong':
        return self.symbol.recommendations_sell_strong
        
    if operation == 'symInfoRecommendationsTotal':
        return self.symbol.recommendations_total

    # Price Targets
    if operation == 'symInfoTargetPriceAverage':
        return self.symbol.target_price_average
        
    if operation == 'symInfoTargetPriceDate':
        return self.symbol.target_price_date
        
    if operation == 'symInfoTargetPriceEstimates':
        return self.symbol.target_price_estimates
        
    if operation == 'symInfoTargetPriceHigh':
        return self.symbol.target_price_high
        
    if operation == 'symInfoTargetPriceLow':
        return self.symbol.target_price_low
        
    if operation == 'symInfoTargetPriceMedian':
        return self.symbol.target_price_median

    # Identifiers
    if operation == 'symInfoTicker':
        return self.symbol.ticker
        
    if operation == 'symInfoTickerId':
        return self.symbol.ticker_id
        
    if operation == 'symInfoTimezone':
        return self.symbol.timezone

        # Dividends Information
    if operation == 'dividendsFutureAmount':
        return self.symbol.dividends_future_amount
        
    if operation == 'dividendsFutureExDate':
        return self.symbol.dividends_future_ex_date
        
    if operation == 'dividendsFuturePayDate':
        return self.symbol.dividends_future_pay_date

    # Earnings Information    
    if operation == 'earningsFutureEps':
        return self.symbol.earnings_future_eps
        
    if operation == 'earningsFuturePeriodEndTime':
        return self.symbol.earnings_future_period_end_time
        
    if operation == 'earningsFutureRevenue':
        return self.symbol.earnings_future_revenue
        
    if operation == 'earningsFutureTime':
        return self.symbol.earnings_future_time

    # Splits Information
    if operation == 'splitsDenominator':
        return self.symbol.splits_denominator
        
    if operation == 'splitsNumerator':
        return self.symbol.splits_numerator

    # Adjustments
    if operation == 'adjustmentDividends':
        return self.symbol.adjustment_dividends
        
    if operation == 'adjustmentNone':
        return self.symbol.adjustment_none
        
    if operation == 'adjustmentSplits':
        return self.symbol.adjustment_splits

    return None

























def _handle_strategy_operation(self, operation, args):
    """
    Handles all strategy related operations and calculations
    """
    # Account Information
    if operation == 'strategyAccountCurrency':
        return self.strategy.account_currency
        
    if operation == 'strategyInitialCapital':
        return self.strategy.initial_capital
        
    if operation == 'strategyEquity':
        return self.strategy.equity

    # Trade Performance
    if operation == 'strategyNetProfit':
        return self.strategy.net_profit
        
    if operation == 'strategyNetProfitPercent':
        return (self.strategy.net_profit / self.strategy.initial_capital) * 100
        
    if operation == 'strategyGrossProfit':
        return self.strategy.gross_profit
        
    if operation == 'strategyGrossProfitPercent':
        return (self.strategy.gross_profit / self.strategy.initial_capital) * 100
        
    if operation == 'strategyGrossLoss':
        return self.strategy.gross_loss
        
    if operation == 'strategyGrossLossPercent':
        return (self.strategy.gross_loss / self.strategy.initial_capital) * 100

    # Trade Statistics
    if operation == 'strategyWinTrades':
        return self.strategy.win_trades
        
    if operation == 'strategyLossTrades':
        return self.strategy.loss_trades
        
    if operation == 'strategyEvenTrades':
        return self.strategy.even_trades
        
    if operation == 'strategyClosedTrades':
        return self.strategy.closed_trades
        
    if operation == 'strategyClosedTradesFirstIndex':
        return self.strategy.closed_trades_first_index

    # Average Trade Performance
    if operation == 'strategyAvgTrade':
        return self.strategy.avg_trade
        
    if operation == 'strategyAvgTradePercent':
        return self.strategy.avg_trade_percent
        
    if operation == 'strategyAvgWinningTrade':
        return self.strategy.avg_winning_trade
        
    if operation == 'strategyAvgWinningTradePercent':
        return self.strategy.avg_winning_trade_percent
        
    if operation == 'strategyAvgLosingTrade':
        return self.strategy.avg_losing_trade
        
    if operation == 'strategyAvgLosingTradePercent':
        return self.strategy.avg_losing_trade_percent

    # Position Information
    if operation == 'strategyOpenTrades':
        return self.strategy.open_trades
        
    if operation == 'strategyOpenTradesCapitalHeld':
        return self.strategy.open_trades_capital_held
        
    if operation == 'strategyPositionSize':
        return self.strategy.position_size
        
    if operation == 'strategyPositionAvgPrice':
        return self.strategy.position_avg_price
        
    if operation == 'strategyPositionEntryName':
        return self.strategy.position_entry_name

    # Risk Metrics
    if operation == 'strategyMaxDrawdown':
        return self.strategy.max_drawdown
        
    if operation == 'strategyMaxDrawdownPercent':
        return self.strategy.max_drawdown_percent
        
    if operation == 'strategyMaxRunup':
        return self.strategy.max_runup
        
    if operation == 'strategyMaxRunupPercent':
        return self.strategy.max_runup_percent

    # Contract Holdings
    if operation == 'strategyMaxContractsHeldAll':
        return self.strategy.max_contracts_held_all
        
    if operation == 'strategyMaxContractsHeldLong':
        return self.strategy.max_contracts_held_long
        
    if operation == 'strategyMaxContractsHeldShort':
        return self.strategy.max_contracts_held_short

    # Open Profit/Loss
    if operation == 'strategyOpenProfit':
        return self.strategy.open_profit
        
    if operation == 'strategyOpenProfitPercent':
        return self.strategy.open_profit_percent

    # Margin Information
    if operation == 'strategyMarginLiquidationPrice':
        return self.strategy.margin_liquidation_price

        # Trade Ratios
    if operation == 'strategyProfitFactor':
        return abs(self.strategy.gross_profit / self.strategy.gross_loss) if self.strategy.gross_loss != 0 else float('inf')
        
    if operation == 'strategyWinRate':
        return (self.strategy.win_trades / self.strategy.closed_trades * 100) if self.strategy.closed_trades > 0 else 0
        
    if operation == 'strategyPayoffRatio':
        avg_win = self.strategy.avg_winning_trade
        avg_loss = abs(self.strategy.avg_losing_trade)
        return avg_win / avg_loss if avg_loss != 0 else float('inf')

    # Trade Duration Stats
    if operation == 'strategyAvgTradeLength':
        return self.strategy.avg_trade_length
        
    if operation == 'strategyAvgWinningTradeLength':
        return self.strategy.avg_winning_trade_length
        
    if operation == 'strategyAvgLosingTradeLength':
        return self.strategy.avg_losing_trade_length
        
    if operation == 'strategyMaxTradeLength':
        return self.strategy.max_trade_length
        
    if operation == 'strategyMinTradeLength':
        return self.strategy.min_trade_length

    # Commission and Slippage
    if operation == 'strategyCommissionPaid':
        return self.strategy.commission_paid
        
    if operation == 'strategyTotalFeesPaid':
        return self.strategy.total_fees_paid
        
    if operation == 'strategySlippagePaid':
        return self.strategy.slippage_paid

    # Risk-Adjusted Returns
    if operation == 'strategySharpeRatio':
        return self.strategy.sharpe_ratio
        
    if operation == 'strategySortinoRatio':
        return self.strategy.sortino_ratio
        
    if operation == 'strategyCalmarRatio':
        return self.strategy.calmar_ratio

    # Consecutive Trade Stats
    if operation == 'strategyMaxConsecutiveWins':
        return self.strategy.max_consecutive_wins
        
    if operation == 'strategyMaxConsecutiveLosses':
        return self.strategy.max_consecutive_losses

    # Trade Volume Stats
    if operation == 'strategyTotalVolumeLong':
        return self.strategy.total_volume_long
        
    if operation == 'strategyTotalVolumeShort':
        return self.strategy.total_volume_short
        
    if operation == 'strategyTotalVolumeTraded':
        return self.strategy.total_volume_traded

    # Position Tracking
    if operation == 'strategyPositionProfit':
        return self.strategy.position_profit
        
    if operation == 'strategyPositionRisk':
        return self.strategy.position_risk
        
    if operation == 'strategyPositionDirection':
        return self.strategy.position_direction

    # Trade Count by Direction
    if operation == 'strategyLongTrades':
        return self.strategy.long_trades
        
    if operation == 'strategyShortTrades':
        return self.strategy.short_trades

    # Performance Metrics
    if operation == 'strategyReturnOnCapital':
        return self.strategy.return_on_capital
        
    if operation == 'strategyAnnualizedReturn':
        return self.strategy.annualized_return
        
    if operation == 'strategyMonthlyReturn':
        return self.strategy.monthly_return
        
    if operation == 'strategyDailyReturn':
        return self.strategy.daily_return

    # Risk Management
    if operation == 'strategyCurrentRisk':
        return self.strategy.current_risk
        
    if operation == 'strategyMaxRiskPerTrade':
        return self.strategy.max_risk_per_trade
        
    if operation == 'strategyRiskFreeRate':
        return self.strategy.risk_free_rate

    # Market Exposure
    if operation == 'strategyMarketExposure':
        return self.strategy.market_exposure
        
    if operation == 'strategyTimeInMarket':
        return self.strategy.time_in_market

    return None















def _calculate_time_components(self):
    """
    Handles all time-related calculations and operations
    """
    # Basic Time Components
    if self.current_syntax == 'time':
        return self.current_bar.timestamp
        
    if self.current_syntax == 'year':
        return self.current_bar.timestamp.year
        
    if self.current_syntax == 'month':
        return self.current_bar.timestamp.month
        
    if self.current_syntax == 'weekofyear':
        return self.current_bar.timestamp.isocalendar()[1]
        
    if self.current_syntax == 'dayofweek':
        return self.current_bar.timestamp.weekday()
        
    if self.current_syntax == 'dayofmonth':
        return self.current_bar.timestamp.day
        
    if self.current_syntax == 'hour':
        return self.current_bar.timestamp.hour
        
    if self.current_syntax == 'minute':
        return self.current_bar.timestamp.minute
        
    if self.current_syntax == 'second':
        return self.current_bar.timestamp.second

    # Time Comparisons
    if self.current_syntax == 'timenow':
        return datetime.now()
        
    if self.current_syntax == 'timestamp':
        return self.current_bar.timestamp.timestamp()
        
    if self.current_syntax == 'bar_index':
        return self.current_bar.index
        
    if self.current_syntax == 'time_close':
        return self.current_bar.close_time

    # Session Time
    if self.current_syntax == 'session':
        return self.current_bar.session
        
    if self.current_syntax == 'session_ismarket':
        return self.current_bar.is_market_hours
        
    if self.current_syntax == 'session_ispremarket':
        return self.current_bar.is_premarket
        
    if self.current_syntax == 'session_ispostmarket':
        return self.current_bar.is_postmarket

    # Extended Time Functions
    if self.current_syntax == 'time_tradingday':
        return self.current_bar.trading_day
        
    if self.current_syntax == 'time_elapsed':
        return self.current_bar.elapsed_time
        
    if self.current_syntax == 'time_remaining':
        return self.current_bar.remaining_time

        # Additional Time Components
    if self.current_syntax == 'timeframe':
        return self.current_bar.timeframe
        
    if self.current_syntax == 'time_format':
        return self.current_bar.timestamp.strftime(self.time_format)
        
    if self.current_syntax == 'time_unix':
        return int(self.current_bar.timestamp.timestamp())
        
    if self.current_syntax == 'time_utc':
        return self.current_bar.timestamp.utc
        
    if self.current_syntax == 'time_local':
        return self.current_bar.timestamp.astimezone()

    # Market Hours
    if self.current_syntax == 'market_open':
        return self.current_bar.market_open_time
        
    if self.current_syntax == 'market_close':
        return self.current_bar.market_close_time
        
    if self.current_syntax == 'is_market_open':
        return self.current_bar.is_market_open
        
    if self.current_syntax == 'is_regular_trading_hours':
        return self.current_bar.is_regular_trading_hours

    # Time Calculations
    if self.current_syntax == 'time_since_market_open':
        return self.current_bar.time_since_market_open
        
    if self.current_syntax == 'time_until_market_close':
        return self.current_bar.time_until_market_close
        
    if self.current_syntax == 'days_since_epoch':
        return (self.current_bar.timestamp - datetime(1970, 1, 1)).days

    return None














def _calculate_price_components(self):
    """
    Handles all price-related calculations and operations
    """
    # Basic Price Components
    if self.current_syntax == 'open':
        return self.current_bar.open
        
    if self.current_syntax == 'high':
        return self.current_bar.high
        
    if self.current_syntax == 'low':
        return self.current_bar.low
        
    if self.current_syntax == 'close':
        return self.current_bar.close
        
    if self.current_syntax == 'hl2':
        return (self.current_bar.high + self.current_bar.low) / 2
        
    if self.current_syntax == 'hlc3':
        return (self.current_bar.high + self.current_bar.low + self.current_bar.close) / 3
        
    if self.current_syntax == 'ohlc4':
        return (self.current_bar.open + self.current_bar.high + self.current_bar.low + self.current_bar.close) / 4

    # Volume Components
    if self.current_syntax == 'volume':
        return self.current_bar.volume
        
    if self.current_syntax == 'volume_ma':
        return self.current_bar.volume_ma
        
    if self.current_syntax == 'volume_delta':
        return self.current_bar.volume_delta

    # Price Changes
    if self.current_syntax == 'change':
        return self.current_bar.close - self.current_bar.open
        
    if self.current_syntax == 'change_percent':
        return ((self.current_bar.close - self.current_bar.open) / self.current_bar.open) * 100
        
    if self.current_syntax == 'range':
        return self.current_bar.high - self.current_bar.low
        
    if self.current_syntax == 'range_percent':
        return ((self.current_bar.high - self.current_bar.low) / self.current_bar.low) * 100

    # Price Gaps
    if self.current_syntax == 'gap':
        return self.current_bar.open - self.previous_bar.close
        
    if self.current_syntax == 'gap_percent':
        return ((self.current_bar.open - self.previous_bar.close) / self.previous_bar.close) * 100

    # Price Extremes
    if self.current_syntax == 'highest':
        return max(bar.high for bar in self.price_history)
        
    if self.current_syntax == 'lowest':
        return min(bar.low for bar in self.price_history)
        
    if self.current_syntax == 'avg_price':
        return sum(bar.close for bar in self.price_history) / len(self.price_history)

    # Price Momentum
    if self.current_syntax == 'momentum':
        return self.current_bar.close - self.previous_bar.close
        
    if self.current_syntax == 'rate_of_change':
        return ((self.current_bar.close - self.previous_bar.close) / self.previous_bar.close) * 100

        # Tick Information
    if self.current_syntax == 'tick_volume':
        return self.current_bar.tick_volume
        
    if self.current_syntax == 'tick_count':
        return self.current_bar.tick_count
        
    if self.current_syntax == 'tick_size':
        return self.current_bar.tick_size

    # Advanced Price Components
    if self.current_syntax == 'vwap':
        return self.current_bar.vwap
        
    if self.current_syntax == 'typical_price':
        return (self.current_bar.high + self.current_bar.low + self.current_bar.close) / 3
        
    if self.current_syntax == 'weighted_close':
        return (self.current_bar.high + self.current_bar.low + self.current_bar.close + self.current_bar.close) / 4
        
    if self.current_syntax == 'median_price':
        return (self.current_bar.high + self.current_bar.low) / 2

    # Price Spreads
    if self.current_syntax == 'spread':
        return self.current_bar.spread
        
    if self.current_syntax == 'spread_percent':
        return (self.current_bar.spread / self.current_bar.close) * 100

    # Volume Analysis
    if self.current_syntax == 'volume_up':
        return self.current_bar.volume_up
        
    if self.current_syntax == 'volume_down':
        return self.current_bar.volume_down
        
    if self.current_syntax == 'volume_weighted':
        return self.current_bar.volume_weighted

    # Price Levels
    if self.current_syntax == 'pivot':
        return (self.current_bar.high + self.current_bar.low + self.current_bar.close) / 3
        
    if self.current_syntax == 'pivot_high':
        return self.current_bar.pivot_high
        
    if self.current_syntax == 'pivot_low':
        return self.current_bar.pivot_low

    # Price Statistics
    if self.current_syntax == 'price_deviation':
        return self.current_bar.price_deviation
        
    if self.current_syntax == 'price_variance':
        return self.current_bar.price_variance
        
    if self.current_syntax == 'price_skewness':
        return self.current_bar.price_skewness
        
    if self.current_syntax == 'price_kurtosis':
        return self.current_bar.price_kurtosis

        # Historical References
    if self.current_syntax == 'previous_close':
        return self.previous_bar.close
        
    if self.current_syntax == 'previous_open':
        return self.previous_bar.open
        
    if self.current_syntax == 'previous_high':
        return self.previous_bar.high
        
    if self.current_syntax == 'previous_low':
        return self.previous_bar.low

    # Price Channels
    if self.current_syntax == 'price_channel_high':
        return max(bar.high for bar in self.price_history[-self.period:])
        
    if self.current_syntax == 'price_channel_low':
        return min(bar.low for bar in self.price_history[-self.period:])
        
    if self.current_syntax == 'price_channel_middle':
        high = max(bar.high for bar in self.price_history[-self.period:])
        low = min(bar.low for bar in self.price_history[-self.period:])
        return (high + low) / 2

    # Price Oscillations
    if self.current_syntax == 'price_oscillator':
        return ((self.current_bar.close - self.current_bar.open) / self.current_bar.open) * 100
        
    if self.current_syntax == 'price_momentum':
        return self.current_bar.close - self.price_history[-self.period].close

    return None
















def _calculate_bar_states(self):
    """
    Handles all bar state calculations and conditions
    """
    # Bar State Flags
    if self.current_syntax == 'isNew':
        return self.current_bar.is_new
        
    if self.current_syntax == 'isConfirmed':
        return self.current_bar.is_confirmed
        
    if self.current_syntax == 'isComplete':
        return self.current_bar.is_complete
        
    if self.current_syntax == 'isRealtime':
        return self.current_bar.is_realtime
        
    if self.current_syntax == 'isHistory':
        return self.current_bar.is_history
        
    if self.current_syntax == 'isFirst':
        return self.current_bar.is_first
        
    if self.current_syntax == 'isLast':
        return self.current_bar.is_last

    # Bar Pattern States
    if self.current_syntax == 'isBullish':
        return self.current_bar.close > self.current_bar.open
        
    if self.current_syntax == 'isBearish':
        return self.current_bar.close < self.current_bar.open
        
    if self.current_syntax == 'isDoji':
        return abs(self.current_bar.close - self.current_bar.open) <= (self.current_bar.high - self.current_bar.low) * 0.1
        
    if self.current_syntax == 'isInside':
        return (self.current_bar.high <= self.previous_bar.high and 
                self.current_bar.low >= self.previous_bar.low)
        
    if self.current_syntax == 'isOutside':
        return (self.current_bar.high > self.previous_bar.high and 
                self.current_bar.low < self.previous_bar.low)

    # Bar Size States
    if self.current_syntax == 'isLargeRange':
        avg_range = sum(b.high - b.low for b in self.price_history[-20:]) / 20
        return (self.current_bar.high - self.current_bar.low) > avg_range * 1.5
        
    if self.current_syntax == 'isSmallRange':
        avg_range = sum(b.high - b.low for b in self.price_history[-20:]) / 20
        return (self.current_bar.high - self.current_bar.low) < avg_range * 0.5

    # Volume States
    if self.current_syntax == 'isHighVolume':
        avg_volume = sum(b.volume for b in self.price_history[-20:]) / 20
        return self.current_bar.volume > avg_volume * 1.5
        
    if self.current_syntax == 'isLowVolume':
        avg_volume = sum(b.volume for b in self.price_history[-20:]) / 20
        return self.current_bar.volume < avg_volume * 0.5

    return None















def _calculate_time_components(self):
    """
    Handles all time-related calculations and operations
    """
    # Basic Time Components
    if self.current_syntax == 'time':
        return self.current_bar.timestamp
        
    if self.current_syntax == 'year':
        return self.current_bar.timestamp.year
        
    if self.current_syntax == 'month':
        return self.current_bar.timestamp.month
        
    if self.current_syntax == 'weekOfYear':
        return self.current_bar.timestamp.isocalendar()[1]
        
    if self.current_syntax == 'dayOfWeek':
        return self.current_bar.timestamp.weekday()
        
    if self.current_syntax == 'dayOfMonth':
        return self.current_bar.timestamp.day
        
    if self.current_syntax == 'hour':
        return self.current_bar.timestamp.hour
        
    if self.current_syntax == 'minute':
        return self.current_bar.timestamp.minute
        
    if self.current_syntax == 'second':
        return self.current_bar.timestamp.second

    # Session States
    if self.current_syntax == 'sessionIsFirstBar':
        return self.current_bar.is_session_first
        
    if self.current_syntax == 'sessionIsFirstBarRegular':
        return self.current_bar.is_session_first_regular
        
    if self.current_syntax == 'sessionIsLastBar':
        return self.current_bar.is_session_last
        
    if self.current_syntax == 'sessionIsLastBarRegular':
        return self.current_bar.is_session_last_regular
        
    if self.current_syntax == 'sessionIsMarket':
        return self.current_bar.is_market_hours
        
    if self.current_syntax == 'sessionIsPostMarket':
        return self.current_bar.is_post_market
        
    if self.current_syntax == 'sessionIsPreMarket':
        return self.current_bar.is_pre_market

    # Trading Time
    if self.current_syntax == 'timeClose':
        return self.current_bar.close_time
        
    if self.current_syntax == 'timeTradingDay':
        return self.current_bar.trading_day
        
    if self.current_syntax == 'timeNow':
        return datetime.now()

        # Timeframe Information
    if self.current_syntax == 'timeframeIsDaily':
        return self.timeframe == 'D'
        
    if self.current_syntax == 'timeframeIsDWM':
        return self.timeframe in ['D', 'W', 'M']
        
    if self.current_syntax == 'timeframeIsIntraday':
        return self.timeframe not in ['D', 'W', 'M']
        
    if self.current_syntax == 'timeframeIsMinutes':
        return self.timeframe.endswith('M')
        
    if self.current_syntax == 'timeframeIsMonthly':
        return self.timeframe == 'M'
        
    if self.current_syntax == 'timeframeIsSeconds':
        return self.timeframe.endswith('S')
        
    if self.current_syntax == 'timeframeIsTicks':
        return self.timeframe == 'T'
        
    if self.current_syntax == 'timeframeIsWeekly':
        return self.timeframe == 'W'
        
    if self.current_syntax == 'timeframeMainPeriod':
        return self.main_timeframe
        
    if self.current_syntax == 'timeframeMultiplier':
        return self.timeframe_multiplier
        
    if self.current_syntax == 'timeframePeriod':
        return self.timeframe_period

    return None












def _calculate_session_states(self):
    """
    Handles all session-related calculations and operations
    """
    # Session Types
    if self.current_syntax == 'sessionRegular':
        return 'regular'
        
    if self.current_syntax == 'sessionExtended':
        return 'extended'

    # Session Adjustments
    if self.current_syntax == 'settlementAsCloseInherit':
        return 'inherit'
        
    if self.current_syntax == 'settlementAsCloseOff':
        return 'off'
        
    if self.current_syntax == 'settlementAsCloseOn':
        return 'on'

    # Bar Merge Settings
    if self.current_syntax == 'barMergeGapsOff':
        return False
        
    if self.current_syntax == 'barMergeGapsOn':
        return True
        
    if self.current_syntax == 'barMergeLookaheadOff':
        return False
        
    if self.current_syntax == 'barMergeLookaheadOn':
        return True

    return None










def _handle_color_operation(self, operation, args):
    """
    Handles all color-related operations
    """
    # Basic Colors
    if operation == 'colAqua':
        return '#00FFFF'
        
    if operation == 'colBlack':
        return '#000000'
        
    if operation == 'colBlue':
        return '#0000FF'
        
    if operation == 'colFuchsia':
        return '#FF00FF'
        
    if operation == 'colGray':
        return '#808080'
        
    if operation == 'colGreen':
        return '#008000'
        
    if operation == 'colLime':
        return '#00FF00'
        
    if operation == 'colMaroon':
        return '#800000'
        
    if operation == 'colNavy':
        return '#000080'
        
    if operation == 'colOlive':
        return '#808000'
        
    if operation == 'colOrange':
        return '#FFA500'
        
    if operation == 'colPurple':
        return '#800080'
        
    if operation == 'colRed':
        return '#FF0000'
        
    if operation == 'colSilver':
        return '#C0C0C0'
        
    if operation == 'colTeal':
        return '#008080'
        
    if operation == 'colWhite':
        return '#FFFFFF'
        
    if operation == 'colYellow':
        return '#FFFF00'

    return None









def _handle_type_declaration(self, node, args):
    """
    Handles all type declarations and operations
    """
    # Basic Types
    if node == 'bool':
        return bool(args[0]) if args else False
        
    if node == 'float':
        return float(args[0]) if args else 0.0
        
    if node == 'int':
        return int(args[0]) if args else 0
        
    if node == 'string':
        return str(args[0]) if args else ""

    # Complex Types
    if node == 'array':
        return [] if not args else list(args)
        
    if node == 'matrix':
        return [[]] if not args else args
        
    if node == 'table':
        return {} if not args else dict(args)

    # Chart Types
    if node == 'box':
        return {'type': 'box', 'props': args}
        
    if node == 'line':
        return {'type': 'line', 'props': args}
        
    if node == 'label':
        return {'type': 'label', 'props': args}

    # Special Types
    if node == 'color':
        return args[0] if args else '#000000'
        
    if node == 'position':
        return args[0] if args else 'auto'
        
    if node == 'style':
        return args[0] if args else 'solid'

    
    # Basic Types
    if node == 'bool':
        return bool(args[0]) if args else False
        
    if node == 'float':
        return float(args[0]) if args else 0.0
        
    if node == 'int':
        return int(args[0]) if args else 0
        
    if node == 'string':
        return str(args[0]) if args else ""

    # Complex Types
    if node == 'array':
        return [] if not args else list(args)
        
    if node == 'matrix':
        return [[]] if not args else args
        
    if node == 'table':
        return {} if not args else dict(args)

    # Chart Types
    if node == 'box':
        return {'type': 'box', 'props': args}
        
    if node == 'line':
        return {'type': 'line', 'props': args}
        
    if node == 'label':
        return {'type': 'label', 'props': args}
        
    if node == 'chartPoint':
        return {'type': 'chartPoint', 'props': args}
        
    if node == 'polyline':
        return {'type': 'polyline', 'props': args}
        
    if node == 'lineFill':
        return {'type': 'lineFill', 'props': args}

    # Special Types
    if node == 'color':
        return args[0] if args else '#000000'
        
    if node == 'position':
        return args[0] if args else 'auto'
        
    if node == 'style':
        return args[0] if args else 'solid'
        
    if node == 'col':
        return args[0] if args else '#000000'
        
    if node == 'arr':
        return [] if not args else list(args)

    return None











def _handle_keyword_operation(self, operation, args):
    """
    Handles all keyword operations
    """
    # Logical Operators
    if operation == 'and':
        return all(args)
        
    if operation == 'or':
        return any(args)
        
    if operation == 'not':
        return not args[0]

    # Control Flow
    if operation == 'if':
        condition, true_block, false_block = args
        return true_block if condition else false_block
        
    if operation == 'for':
        iterable, block = args
        return [self._evaluate(block) for _ in iterable]
        
    if operation == 'while':
        condition, block = args
        results = []
        while self._evaluate(condition):
            results.append(self._evaluate(block))
        return results

    # Variable Declaration
    if operation == 'let':
        name, value = args
        self.variables[name] = value
        return value
        
    if operation == 'const':
        name, value = args
        self.constants[name] = value
        return value

    # Function Operations
    if operation == 'onTick':
        return self._handle_tick_event(args[0])
        
    if operation == 'onBar':
        return self._handle_bar_event(args[0])

    
    # Loop Operations
    if operation == 'forLoop':
        init, condition, update, block = args
        self._evaluate(init)
        results = []
        while self._evaluate(condition):
            results.append(self._evaluate(block))
            self._evaluate(update)
        return results
        
    if operation == 'forInLoop':
        var, collection, block = args
        results = []
        for item in self._evaluate(collection):
            self.variables[var] = item
            results.append(self._evaluate(block))
        return results
        
    if operation == 'whileLoop':
        condition, block = args
        results = []
        while self._evaluate(condition):
            results.append(self._evaluate(block))
        return results

    # Function Declarations
    if operation == 'exportFunc':
        name, params, block = args
        self.functions[name] = {'params': params, 'block': block}
        return None
        
    if operation == 'importFunc':
        module, name = args
        return self._import_function(module, name)
        
    if operation == 'methodFunc':
        name, params, block = args
        self.methods[name] = {'params': params, 'block': block}
        return None

    # Type Operations
    if operation == 'enumType':
        name, values = args
        self.enums[name] = values
        return None
        
    if operation == 'typeDef':
        name, base_type = args
        self.types[name] = base_type
        return None

    # Logical Operators
    if operation == 'andOp':
        return all(self._evaluate(arg) for arg in args)
        
    if operation == 'orOp':
        return any(self._evaluate(arg) for arg in args)
        
    if operation == 'notOp':
        return not self._evaluate(args[0])

    # Control Flow
    if operation == 'switchCase':
        value, cases, default = args
        for case, block in cases:
            if self._evaluate(value) == self._evaluate(case):
                return self._evaluate(block)
        return self._evaluate(default) if default else None

    # Variable Declaration
    if operation == 'letip':
        name, value = args
        self.variables[name] = self._evaluate(value)
        return self.variables[name]

    return None








def _evaluate_builtin_function(self, syntax):
    """
    Handles all built-in function evaluations
    """
    # Display Functions
    if syntax.get('name') == 'show':
        return self._show_plot(syntax.get('args', []))
        
    if syntax.get('name') == 'showshape':
        return self._show_shape(syntax.get('args', []))
        
    if syntax.get('name') == 'showcond':
        return self._show_condition(syntax.get('args', []))

    # Style Functions
    if syntax.get('name') == 'solid':
        return 'solid'
        
    if syntax.get('name') == 'dotted':
        return 'dotted'
        
    if syntax.get('name') == 'dashed':
        return 'dashed'

    # Font Functions
    if syntax.get('name') == 'fontFamilyDefault':
        return 'default'
        
    if syntax.get('name') == 'fontFamilyMonospace':
        return 'monospace'

    # Extension Functions
    if syntax.get('name') == 'extendBoth':
        return 'both'
        
    if syntax.get('name') == 'extendLeft':
        return 'left'
        
    if syntax.get('name') == 'extendNone':
        return 'none'
        
    if syntax.get('name') == 'extendRight':
        return 'right'

    # Line Style Functions
    if syntax.get('name') == 'hlineStyleDashed':
        return 'dashed'
        
    if syntax.get('name') == 'hlineStyleDotted':
        return 'dotted'
        
    if syntax.get('name') == 'hlineStyleSolid':
        return 'solid'

        # Alert Functions
    if syntax.get('name') == 'alertFunc':
        return self._handle_alert(syntax.get('args', []))
        
    if syntax.get('name') == 'alertConditionFunc':
        return self._handle_alert_condition(syntax.get('args', []))

    # Array Functions
    if syntax.get('name') in ['arrAbs', 'arrAvg', 'arrBinarySearch', 'arrBinarySearchLeftmost', 
                             'arrBinarySearchRightmost', 'arrClear', 'arrConcat', 'arrCopy', 
                             'arrCovariance', 'arrEvery', 'arrFill', 'arrFirst', 'arrFrom', 
                             'arrGet', 'arrIncludes', 'arrIndexOf', 'arrInsert', 'arrJoin', 
                             'arrLast', 'arrLastIndexOf', 'arrMax', 'arrMedian', 'arrMin', 
                             'arrMode', 'arrNewBool', 'arrNewBox', 'arrNewFloat', 'arrNewInt', 
                             'arrNewLabel', 'arrNewLine', 'arrNewLineFill', 'arrNewString', 
                             'arrNewTable', 'arrNewType', 'arrPercentileLinearInterpolation', 
                             'arrPercentileNearestRank', 'arrPercentRank', 'arrPop', 'arrPush', 
                             'arrRange', 'arrRemove', 'arrReverse', 'arrSet', 'arrShift', 
                             'arrSize', 'arrSlice', 'arrSome', 'arrSort', 'arrSortIndices', 
                             'arrStandardize', 'arrStdev', 'arrSum', 'arrUnshift', 'arrVariance']:
        return self._handle_array_function(syntax.get('name'), syntax.get('args', []))

    # Math Functions
    if syntax.get('name') in ['mathAbs', 'mathAcos', 'mathAsin', 'mathAtan', 'mathAvg', 
                             'mathCeil', 'mathCos', 'mathExp', 'mathFloor', 'mathLog', 
                             'mathLog10', 'mathMax', 'mathMin', 'mathPow', 'mathRandom', 
                             'mathRound', 'mathRoundToMinTick', 'mathSign', 'mathSin', 
                             'mathSqrt', 'mathSum', 'mathTan', 'mathToDegrees', 'mathToRadians']:
        return self._handle_math_function(syntax.get('name'), syntax.get('args', []))

    # String Functions
    if syntax.get('name') in ['strContains', 'strEndsWith', 'strFormat', 'strFormatTime', 
                             'strLength', 'strLower', 'strMatch', 'strPos', 'strRepeat', 
                             'strReplace', 'strReplaceAll', 'strSplit', 'strStartsWith', 
                             'strSubstring', 'strToNumber', 'strToString', 'strTrim', 'strUpper']:
        return self._handle_string_function(syntax.get('name'), syntax.get('args', []))

    # Request Functions
    if syntax.get('name') in ['requestCurrencyRate', 'requestDividends', 'requestEarnings', 
                             'requestEconomic', 'requestFinancial', 'requestQuandl', 
                             'requestSecurity', 'requestSecurityLowerTf', 'requestSeed', 
                             'requestSplits']:
        return self._handle_request_function(syntax.get('name'), syntax.get('args', []))

    return None








def _calculate_price_averages(self, calc_type):
    """
    Handles all price average calculations
    """
    # Simple Moving Averages
    if calc_type == 'sma':
        period = self.current_args.get('period', 14)
        source = self.current_args.get('source', 'close')
        return sum(getattr(bar, source) for bar in self.price_history[-period:]) / period

    # Exponential Moving Average
    if calc_type == 'ema':
        period = self.current_args.get('period', 14)
        source = self.current_args.get('source', 'close')
        alpha = 2 / (period + 1)
        ema = getattr(self.price_history[-period], source)
        for bar in self.price_history[-period+1:]:
            ema = (getattr(bar, source) * alpha) + (ema * (1 - alpha))
        return ema

    # Weighted Moving Average
    if calc_type == 'wma':
        period = self.current_args.get('period', 14)
        source = self.current_args.get('source', 'close')
        weight_sum = (period * (period + 1)) / 2
        weighted_sum = sum(getattr(bar, source) * (i + 1) 
                         for i, bar in enumerate(self.price_history[-period:]))
        return weighted_sum / weight_sum

    # Volume Weighted Average Price
    if calc_type == 'vwap':
        period = self.current_args.get('period', len(self.price_history))
        volume_sum = sum(bar.volume for bar in self.price_history[-period:])
        if volume_sum == 0:
            return None
        return sum((bar.high + bar.low + bar.close) / 3 * bar.volume 
                  for bar in self.price_history[-period:]) / volume_sum

    return None










def _calculate_strategy_metrics(self):
    """
    Handles all strategy metrics calculations
    """
    # Account Metrics
    if self.current_syntax == 'strategyAccountCurrency':
        return self.strategy.account_currency
        
    if self.current_syntax == 'strategyInitialCapital':
        return self.strategy.initial_capital
        
    if self.current_syntax == 'strategyEquity':
        return self.strategy.equity

    # Trade Performance
    if self.current_syntax == 'strategyAvgLosingTrade':
        return self.strategy.avg_losing_trade
        
    if self.current_syntax == 'strategyAvgLosingTradePercent':
        return self.strategy.avg_losing_trade_percent
        
    if self.current_syntax == 'strategyAvgTrade':
        return self.strategy.avg_trade
        
    if self.current_syntax == 'strategyAvgTradePercent':
        return self.strategy.avg_trade_percent
        
    if self.current_syntax == 'strategyAvgWinningTrade':
        return self.strategy.avg_winning_trade
        
    if self.current_syntax == 'strategyAvgWinningTradePercent':
        return self.strategy.avg_winning_trade_percent

    # Trade Statistics
    if self.current_syntax == 'strategyClosedTrades':
        return self.strategy.closed_trades
        
    if self.current_syntax == 'strategyClosedTradesFirstIndex':
        return self.strategy.closed_trades_first_index
        
    if self.current_syntax == 'strategyEvenTrades':
        return self.strategy.even_trades
        
    if self.current_syntax == 'strategyLossTrades':
        return self.strategy.loss_trades
        
    if self.current_syntax == 'strategyWinTrades':
        return self.strategy.win_trades

    # Profit/Loss Metrics
    if self.current_syntax == 'strategyGrossLoss':
        return self.strategy.gross_loss
        
    if self.current_syntax == 'strategyGrossLossPercent':
        return self.strategy.gross_loss_percent
        
    if self.current_syntax == 'strategyGrossProfit':
        return self.strategy.gross_profit
        
    if self.current_syntax == 'strategyGrossProfitPercent':
        return self.strategy.gross_profit_percent
        
    if self.current_syntax == 'strategyNetProfit':
        return self.strategy.net_profit
        
    if self.current_syntax == 'strategyNetProfitPercent':
        return self.strategy.net_profit_percent

    # Position Metrics
    if self.current_syntax == 'strategyOpenProfit':
        return self.strategy.open_profit
        
    if self.current_syntax == 'strategyOpenProfitPercent':
        return self.strategy.open_profit_percent
        
    if self.current_syntax == 'strategyOpenTrades':
        return self.strategy.open_trades
        
    if self.current_syntax == 'strategyOpenTradesCapitalHeld':
        return self.strategy.open_trades_capital_held

    # Position Details
    if self.current_syntax == 'strategyPositionAvgPrice':
        return self.strategy.position_avg_price
        
    if self.current_syntax == 'strategyPositionEntryName':
        return self.strategy.position_entry_name
        
    if self.current_syntax == 'strategyPositionSize':
        return self.strategy.position_size

    return None







def constant(self, name):
    """
    Handles all constant values
    """
    # Mathematical Constants
    if name == 'mathE':
        return 2.718281828459045
        
    if name == 'mathPhi':
        return 1.618033988749895
        
    if name == 'mathPi':
        return 3.141592653589793
        
    if name == 'mathRPhi':
        return 0.618033988749895

    # Boolean Constants
    if name == 'trueValue':
        return True
        
    if name == 'falseValue':
        return False
        
    if name == 'na':
        return None

    # Location Constants
    if name == 'locationAboveBar':
        return 'above'
        
    if name == 'locationAbsolute':
        return 'absolute'
        
    if name == 'locationBelowBar':
        return 'below'
        
    if name == 'locationBottom':
        return 'bottom'
        
    if name == 'locationTop':
        return 'top'

    return None





def _handle_array_operation(self, operation, args):
    """
    Handles all array operations
    """
    # Array Creation
    if operation == 'arrNewBool':
        return [False] * args[0]
        
    if operation == 'arrNewFloat':
        return [0.0] * args[0]
        
    if operation == 'arrNewInt':
        return [0] * args[0]
        
    if operation == 'arrNewString':
        return [''] * args[0]

    # Array Manipulation
    if operation == 'arrPush':
        array, value = args
        array.append(value)
        return array
        
    if operation == 'arrPop':
        return args[0].pop()
        
    if operation == 'arrShift':
        return args[0].pop(0)
        
    if operation == 'arrUnshift':
        array, value = args
        array.insert(0, value)
        return array

    # Array Search
    if operation == 'arrIndexOf':
        array, value = args
        return array.index(value) if value in array else -1
        
    if operation == 'arrLastIndexOf':
        array, value = args
        return len(array) - 1 - array[::-1].index(value) if value in array else -1
        
    if operation == 'arrIncludes':
        array, value = args
        return value in array

    # Array Transformation
    if operation == 'arrConcat':
        return args[0] + args[1]
        
    if operation == 'arrSlice':
        array, start, end = args
        return array[start:end]
        
    if operation == 'arrJoin':
        array, separator = args
        return separator.join(map(str, array))
        
    if operation == 'arrReverse':
        return args[0][::-1]
        
    if operation == 'arrSort':
        return sorted(args[0])

    # Array Statistics
    if operation == 'arrSum':
        return sum(args[0])
        
    if operation == 'arrAvg':
        return sum(args[0]) / len(args[0])
        
    if operation == 'arrMin':
        return min(args[0])
        
    if operation == 'arrMax':
        return max(args[0])
        
    if operation == 'arrStdev':
        return self._calculate_stdev(args[0])

    # Array Utility
    if operation == 'arrClear':
        args[0].clear()
        return args[0]
        
    if operation == 'arrSize':
        return len(args[0])
        
    if operation == 'arrCopy':
        return args[0].copy()

        # Array Advanced Statistics
    if operation == 'arrMedian':
        sorted_arr = sorted(args[0])
        n = len(sorted_arr)
        mid = n // 2
        return sorted_arr[mid] if n % 2 else (sorted_arr[mid-1] + sorted_arr[mid]) / 2
        
    if operation == 'arrMode':
        from statistics import mode
        return mode(args[0])
        
    if operation == 'arrVariance':
        return self._calculate_variance(args[0])
        
    if operation == 'arrCovariance':
        return self._calculate_covariance(args[0], args[1])

    # Array Search Advanced
    if operation == 'arrBinarySearch':
        return self._binary_search(args[0], args[1])
        
    if operation == 'arrBinarySearchLeftmost':
        return self._binary_search_leftmost(args[0], args[1])
        
    if operation == 'arrBinarySearchRightmost':
        return self._binary_search_rightmost(args[0], args[1])

    # Array Testing
    if operation == 'arrEvery':
        return all(args[0])
        
    if operation == 'arrSome':
        return any(args[0])

    # Array Manipulation Advanced
    if operation == 'arrFill':
        array, value = args
        for i in range(len(array)):
            array[i] = value
        return array
        
    if operation == 'arrInsert':
        array, index, value = args
        array.insert(index, value)
        return array
        
    if operation == 'arrRemove':
        array, index = args
        return array.pop(index)

    # Array Creation Advanced
    if operation == 'arrFrom':
        return list(args[0])
        
    if operation == 'arrRange':
        start, end, step = args if len(args) == 3 else (args[0], args[1], 1)
        return list(range(start, end, step))

    # Array Element Access
    if operation == 'arrFirst':
        return args[0][0] if args[0] else None
        
    if operation == 'arrLast':
        return args[0][-1] if args[0] else None
        
    if operation == 'arrGet':
        array, index = args
        return array[index]
        
    if operation == 'arrSet':
        array, index, value = args
        array[index] = value
        return array

    # Array Sorting Advanced
    if operation == 'arrSortIndices':
        return sorted(range(len(args[0])), key=lambda k: args[0][k])
        
    if operation == 'arrStandardize':
        return self._standardize_array(args[0])

    # Array Percentile Operations
    if operation == 'arrPercentileLinearInterpolation':
        return self._percentile_linear(args[0], args[1])
        
    if operation == 'arrPercentileNearestRank':
        return self._percentile_nearest(args[0], args[1])
        
    if operation == 'arrPercentRank':
        return self._percent_rank(args[0], args[1])

        # Chart Object Arrays
    if operation == 'arrNewBox':
        return [{'type': 'box', 'props': {}} for _ in range(args[0])]
        
    if operation == 'arrNewLabel':
        return [{'type': 'label', 'props': {}} for _ in range(args[0])]
        
    if operation == 'arrNewLine':
        return [{'type': 'line', 'props': {}} for _ in range(args[0])]
        
    if operation == 'arrNewLineFill':
        return [{'type': 'linefill', 'props': {}} for _ in range(args[0])]

    # Data Structure Arrays
    if operation == 'arrNewTable':
        return [{'type': 'table', 'data': {}} for _ in range(args[0])]
        
    if operation == 'arrNewType':
        return [{'type': args[1], 'value': None} for _ in range(args[0])]

    # Array Type Conversion
    if operation == 'arrToString':
        return [str(x) for x in args[0]]
        
    if operation == 'arrToFloat':
        return [float(x) for x in args[0]]
        
    if operation == 'arrToInt':
        return [int(x) for x in args[0]]
        
    if operation == 'arrToBool':
        return [bool(x) for x in args[0]]

    return None





def _handle_box_operation(self, operation, args):
    """
    Handles all box operations
    """
    # Box Creation
    if operation == 'boxNew':
        return {'type': 'box', 'props': {}}
        
    if operation == 'boxAdd':
        left, top, right, bottom = args
        return {'type': 'box', 'props': {
            'left': left,
            'top': top,
            'right': right,
            'bottom': bottom
        }}

    # Box Properties
    if operation == 'boxSetBgColor':
        box, color = args
        box['props']['bgcolor'] = color
        return box
        
    if operation == 'boxSetBorderColor':
        box, color = args
        box['props']['border_color'] = color
        return box
        
    if operation == 'boxSetBorderStyle':
        box, style = args
        box['props']['border_style'] = style
        return box
        
    if operation == 'boxSetBorderWidth':
        box, width = args
        box['props']['border_width'] = width
        return box
        
    if operation == 'boxSetLeftBottom':
        box, x, y = args
        box['props']['left'] = x
        box['props']['bottom'] = y
        return box
        
    if operation == 'boxSetRightTop':
        box, x, y = args
        box['props']['right'] = x
        box['props']['top'] = y
        return box
        
    if operation == 'boxSetText':
        box, text = args
        box['props']['text'] = text
        return box
        
    if operation == 'boxSetTextColor':
        box, color = args
        box['props']['text_color'] = color
        return box
        
    if operation == 'boxSetTextHalign':
        box, align = args
        box['props']['text_halign'] = align
        return box
        
    if operation == 'boxSetTextSize':
        box, size = args
        box['props']['text_size'] = size
        return box
        
    if operation == 'boxSetTextValign':
        box, align = args
        box['props']['text_valign'] = align
        return box

    # Box State
    if operation == 'boxDelete':
        return {'action': 'delete', 'box': args[0]}
        
    if operation == 'boxGet':
        return {'action': 'get', 'id': args[0]}

        # Box Visibility
    if operation == 'boxSetVisible':
        box, visible = args
        box['props']['visible'] = visible
        return box
        
    if operation == 'boxIsVisible':
        return args[0]['props'].get('visible', True)

    # Box Coordinates
    if operation == 'boxGetBottom':
        return args[0]['props'].get('bottom')
        
    if operation == 'boxGetLeft':
        return args[0]['props'].get('left')
        
    if operation == 'boxGetRight':
        return args[0]['props'].get('right')
        
    if operation == 'boxGetTop':
        return args[0]['props'].get('top')

    # Box Text Properties
    if operation == 'boxGetText':
        return args[0]['props'].get('text', '')
        
    if operation == 'boxSetTextFont':
        box, font = args
        box['props']['text_font'] = font
        return box
        
    if operation == 'boxSetTextWrap':
        box, wrap = args
        box['props']['text_wrap'] = wrap
        return box

    # Box Style Properties
    if operation == 'boxSetExtend':
        box, extend = args
        box['props']['extend'] = extend
        return box
        
    if operation == 'boxSetOpacity':
        box, opacity = args
        box['props']['opacity'] = opacity
        return box

    return None






def _handle_chart_operation(self, operation, args):
    """
    Handles all chart operations
    """
    # Chart Properties
    if operation == 'chartSetBarStyle':
        return {'action': 'set_bar_style', 'style': args[0]}
        
    if operation == 'chartSetBgColor':
        return {'action': 'set_bgcolor', 'color': args[0]}
        
    if operation == 'chartSetGridColor':
        return {'action': 'set_grid_color', 'color': args[0]}
        
    if operation == 'chartSetTextColor':
        return {'action': 'set_text_color', 'color': args[0]}

    # Chart Layout
    if operation == 'chartSetLayout':
        return {'action': 'set_layout', 'layout': args[0]}
        
    if operation == 'chartSetOverlay':
        return {'action': 'set_overlay', 'overlay': args[0]}
        
    if operation == 'chartSetScale':
        return {'action': 'set_scale', 'scale': args[0]}
        
    if operation == 'chartSetZoom':
        return {'action': 'set_zoom', 'zoom': args[0]}

    # Chart Time Properties
    if operation == 'chartSetTimeZone':
        return {'action': 'set_timezone', 'timezone': args[0]}
        
    if operation == 'chartSetSession':
        return {'action': 'set_session', 'session': args[0]}

    # Chart Data Properties
    if operation == 'chartSetSymbol':
        return {'action': 'set_symbol', 'symbol': args[0]}
        
    if operation == 'chartSetResolution':
        return {'action': 'set_resolution', 'resolution': args[0]}
        
    if operation == 'chartSetRange':
        return {'action': 'set_range', 'from': args[0], 'to': args[1]}

    # Chart State
    if operation == 'chartClear':
        return {'action': 'clear'}
        
    if operation == 'chartRefresh':
        return {'action': 'refresh'}

    return None








def _handle_input_operation(self, operation, args):
    """
    Handles all input operations
    """
    # Basic Inputs
    if operation == 'inputBool':
        title, defval = args
        return {'type': 'bool', 'title': title, 'defval': defval}
        
    if operation == 'inputInt':
        title, defval = args
        return {'type': 'int', 'title': title, 'defval': defval}
        
    if operation == 'inputFloat':
        title, defval = args
        return {'type': 'float', 'title': title, 'defval': defval}
        
    if operation == 'inputString':
        title, defval = args
        return {'type': 'string', 'title': title, 'defval': defval}

    # Range Inputs
    if operation == 'inputTimeRange':
        title, defval = args
        return {'type': 'time_range', 'title': title, 'defval': defval}
        
    if operation == 'inputPriceRange':
        title, defval = args
        return {'type': 'price_range', 'title': title, 'defval': defval}

    # Selection Inputs
    if operation == 'inputOptions':
        title, options, defval = args
        return {'type': 'options', 'title': title, 'options': options, 'defval': defval}
        
    if operation == 'inputSymbol':
        title, defval = args
        return {'type': 'symbol', 'title': title, 'defval': defval}
        
    if operation == 'inputResolution':
        title, defval = args
        return {'type': 'resolution', 'title': title, 'defval': defval}

    # Advanced Inputs
    if operation == 'inputColor':
        title, defval = args
        return {'type': 'color', 'title': title, 'defval': defval}
        
    if operation == 'inputSession':
        title, defval = args
        return {'type': 'session', 'title': title, 'defval': defval}
        
    if operation == 'inputSource':
        title, defval = args
        return {'type': 'source', 'title': title, 'defval': defval}

        # Input with Constraints
    if operation == 'inputIntStep':
        title, defval, minval, maxval, step = args
        return {
            'type': 'int_step',
            'title': title,
            'defval': defval,
            'minval': minval,
            'maxval': maxval,
            'step': step
        }
        
    if operation == 'inputFloatStep':
        title, defval, minval, maxval, step = args
        return {
            'type': 'float_step',
            'title': title,
            'defval': defval,
            'minval': minval,
            'maxval': maxval,
            'step': step
        }

    # Group Inputs
    if operation == 'inputGroup':
        title, inputs = args
        return {'type': 'group', 'title': title, 'inputs': inputs}
        
    if operation == 'inputSection':
        title = args[0]
        return {'type': 'section', 'title': title}

    # Specialized Inputs
    if operation == 'inputBarState':
        title, defval = args
        return {'type': 'bar_state', 'title': title, 'defval': defval}
        
    if operation == 'inputDatetime':
        title, defval = args
        return {'type': 'datetime', 'title': title, 'defval': defval}
        
    if operation == 'inputStyle':
        title, defval = args
        return {'type': 'style', 'title': title, 'defval': defval}
        
    if operation == 'inputTextArea':
        title, defval = args
        return {'type': 'textarea', 'title': title, 'defval': defval}

    return None






def _handle_label_operation(self, operation, args):
    """
    Handles all label operations
    """
    # Label Creation
    if operation == 'labelNew':
        x, y, text = args
        return {'type': 'label', 'props': {
            'x': x,
            'y': y,
            'text': text
        }}

    # Label Properties
    if operation == 'labelSetColor':
        label, color = args
        label['props']['color'] = color
        return label
        
    if operation == 'labelSetStyle':
        label, style = args
        label['props']['style'] = style
        return label
        
    if operation == 'labelSetText':
        label, text = args
        label['props']['text'] = text
        return label
        
    if operation == 'labelSetTextColor':
        label, color = args
        label['props']['text_color'] = color
        return label
        
    if operation == 'labelSetXY':
        label, x, y = args
        label['props']['x'] = x
        label['props']['y'] = y
        return label
        
    if operation == 'labelSetSize':
        label, size = args
        label['props']['size'] = size
        return label
        
    if operation == 'labelSetTooltip':
        label, tooltip = args
        label['props']['tooltip'] = tooltip
        return label

    # Label Alignment
    if operation == 'labelSetHAlign':
        label, align = args
        label['props']['halign'] = align
        return label
        
    if operation == 'labelSetVAlign':
        label, align = args
        label['props']['valign'] = align
        return label

    # Label State
    if operation == 'labelDelete':
        return {'action': 'delete', 'label': args[0]}
        
    if operation == 'labelGet':
        return {'action': 'get', 'id': args[0]}

        # Label Text Properties
    if operation == 'labelSetFont':
        label, font = args
        label['props']['font'] = font
        return label
        
    if operation == 'labelSetTextWrap':
        label, wrap = args
        label['props']['text_wrap'] = wrap
        return label

    # Label Visibility
    if operation == 'labelSetVisible':
        label, visible = args
        label['props']['visible'] = visible
        return label
        
    if operation == 'labelIsVisible':
        return args[0]['props'].get('visible', True)

    # Label Position
    if operation == 'labelGetX':
        return args[0]['props'].get('x')
        
    if operation == 'labelGetY':
        return args[0]['props'].get('y')
        
    if operation == 'labelGetText':
        return args[0]['props'].get('text', '')

    # Label Style Properties
    if operation == 'labelSetBorderColor':
        label, color = args
        label['props']['border_color'] = color
        return label
        
    if operation == 'labelSetBorderWidth':
        label, width = args
        label['props']['border_width'] = width
        return label
        
    if operation == 'labelSetBgColor':
        label, color = args
        label['props']['bgcolor'] = color
        return label
        
    if operation == 'labelSetOpacity':
        label, opacity = args
        label['props']['opacity'] = opacity
        return label

    return None






def _handle_line_operation(self, operation, args):
    """
    Handles all line operations
    """
    # Line Creation
    if operation == 'lineNew':
        x1, y1, x2, y2 = args
        return {'type': 'line', 'props': {
            'x1': x1,
            'y1': y1,
            'x2': x2,
            'y2': y2
        }}

    # Line Properties
    if operation == 'lineSetColor':
        line, color = args
        line['props']['color'] = color
        return line
        
    if operation == 'lineSetStyle':
        line, style = args
        line['props']['style'] = style
        return line
        
    if operation == 'lineSetWidth':
        line, width = args
        line['props']['width'] = width
        return line
        
    if operation == 'lineSetXY1':
        line, x1, y1 = args
        line['props']['x1'] = x1
        line['props']['y1'] = y1
        return line
        
    if operation == 'lineSetXY2':
        line, x2, y2 = args
        line['props']['x2'] = x2
        line['props']['y2'] = y2
        return line

    # Line State
    if operation == 'lineDelete':
        return {'action': 'delete', 'line': args[0]}
        
    if operation == 'lineGet':
        return {'action': 'get', 'id': args[0]}

        # Line Visibility
    if operation == 'lineSetVisible':
        line, visible = args
        line['props']['visible'] = visible
        return line
        
    if operation == 'lineIsVisible':
        return args[0]['props'].get('visible', True)

    # Line Coordinates
    if operation == 'lineGetX1':
        return args[0]['props'].get('x1')
        
    if operation == 'lineGetY1':
        return args[0]['props'].get('y1')
        
    if operation == 'lineGetX2':
        return args[0]['props'].get('x2')
        
    if operation == 'lineGetY2':
        return args[0]['props'].get('y2')

    # Line Extensions
    if operation == 'lineSetExtend':
        line, extend = args
        line['props']['extend'] = extend
        return line
        
    if operation == 'lineGetExtend':
        return args[0]['props'].get('extend', 'none')

    # Line Style Properties
    if operation == 'lineSetOpacity':
        line, opacity = args
        line['props']['opacity'] = opacity
        return line
        
    if operation == 'lineSetDash':
        line, dash = args
        line['props']['dash'] = dash
        return line

    return None










def _handle_log_operation(self, operation, args):
    """
    Handles all logging operations
    """
    # Basic Logging
    if operation == 'log':
        message = args[0]
        return {'action': 'log', 'message': message, 'level': 'info'}
        
    if operation == 'logDebug':
        message = args[0]
        return {'action': 'log', 'message': message, 'level': 'debug'}
        
    if operation == 'logError':
        message = args[0]
        return {'action': 'log', 'message': message, 'level': 'error'}
        
    if operation == 'logInfo':
        message = args[0]
        return {'action': 'log', 'message': message, 'level': 'info'}
        
    if operation == 'logWarn':
        message = args[0]
        return {'action': 'log', 'message': message, 'level': 'warn'}

    # Formatted Logging
    if operation == 'logFormat':
        template, *values = args
        return {'action': 'log', 'message': template.format(*values), 'level': 'info'}

    # Trade Logging
    if operation == 'logTrade':
        trade_info = args[0]
        return {'action': 'log', 'message': trade_info, 'level': 'trade'}

        # Advanced Logging
    if operation == 'logTrace':
        message = args[0]
        return {'action': 'log', 'message': message, 'level': 'trace'}
        
    if operation == 'logVerbose':
        message = args[0]
        return {'action': 'log', 'message': message, 'level': 'verbose'}
        
    if operation == 'logCritical':
        message = args[0]
        return {'action': 'log', 'message': message, 'level': 'critical'}

    # Structured Logging
    if operation == 'logJson':
        data = args[0]
        return {'action': 'log', 'message': data, 'level': 'info', 'format': 'json'}
        
    if operation == 'logTable':
        table_data = args[0]
        return {'action': 'log', 'message': table_data, 'level': 'info', 'format': 'table'}

    # Log Control
    if operation == 'logClear':
        return {'action': 'log_clear'}
        
    if operation == 'logSetLevel':
        level = args[0]
        return {'action': 'log_set_level', 'level': level}

    return None








def _handle_map_operation(self, operation, args):
    """
    Handles all map operations
    """
    # Map Creation and Basic Operations
    if operation == 'mapNew':
        return {}
        
    if operation == 'mapSet':
        map_obj, key, value = args
        map_obj[key] = value
        return map_obj
        
    if operation == 'mapGet':
        map_obj, key = args
        return map_obj.get(key)
        
    if operation == 'mapDelete':
        map_obj, key = args
        if key in map_obj:
            del map_obj[key]
        return map_obj
        
    if operation == 'mapClear':
        args[0].clear()
        return args[0]

    # Map Information
    if operation == 'mapSize':
        return len(args[0])
        
    if operation == 'mapContains':
        map_obj, key = args
        return key in map_obj
        
    if operation == 'mapEmpty':
        return len(args[0]) == 0

    # Map Keys and Values
    if operation == 'mapKeys':
        return list(args[0].keys())
        
    if operation == 'mapValues':
        return list(args[0].values())
        
    if operation == 'mapItems':
        return list(args[0].items())

    # Map Operations
    if operation == 'mapCopy':
        return args[0].copy()
        
    if operation == 'mapMerge':
        map1, map2 = args
        map1.update(map2)
        return map1
        
    if operation == 'mapReverse':
        return {v: k for k, v in args[0].items()}

        # Map Type Operations
    if operation == 'mapToArray':
        return [{'key': k, 'value': v} for k, v in args[0].items()]
        
    if operation == 'mapFromArray':
        return {item['key']: item['value'] for item in args[0]}
        
    if operation == 'mapToJson':
        return json.dumps(args[0])
        
    if operation == 'mapFromJson':
        return json.loads(args[0])

    # Map Filtering
    if operation == 'mapFilter':
        map_obj, predicate = args
        return {k: v for k, v in map_obj.items() if predicate(k, v)}
        
    if operation == 'mapFind':
        map_obj, predicate = args
        return next((k for k, v in map_obj.items() if predicate(k, v)), None)

    # Map Transformation
    if operation == 'mapTransform':
        map_obj, transform_func = args
        return {k: transform_func(v) for k, v in map_obj.items()}
        
    if operation == 'mapTransformKeys':
        map_obj, transform_func = args
        return {transform_func(k): v for k, v in map_obj.items()}

    # Map Validation
    if operation == 'mapValidate':
        map_obj, schema = args
        return self._validate_map(map_obj, schema)
        
    if operation == 'mapHasAllKeys':
        map_obj, keys = args
        return all(key in map_obj for key in keys)

    return None




def _handle_math_operation(self, operation, args):
    """
    Handles all mathematical operations
    """
    # Basic Math
    if operation == 'mathAbs':
        return abs(args[0])
        
    if operation == 'mathAdd':
        return args[0] + args[1]
        
    if operation == 'mathCeil':
        return math.ceil(args[0])
        
    if operation == 'mathFloor':
        return math.floor(args[0])
        
    if operation == 'mathMax':
        return max(args)
        
    if operation == 'mathMin':
        return min(args)
        
    if operation == 'mathMod':
        return args[0] % args[1]
        
    if operation == 'mathPow':
        return math.pow(args[0], args[1])
        
    if operation == 'mathRound':
        return round(args[0])
        
    if operation == 'mathSign':
        return -1 if args[0] < 0 else 1 if args[0] > 0 else 0
        
    if operation == 'mathSqrt':
        return math.sqrt(args[0])

    # Trigonometry
    if operation == 'mathAcos':
        return math.acos(args[0])
        
    if operation == 'mathAsin':
        return math.asin(args[0])
        
    if operation == 'mathAtan':
        return math.atan(args[0])
        
    if operation == 'mathAtan2':
        return math.atan2(args[0], args[1])
        
    if operation == 'mathCos':
        return math.cos(args[0])
        
    if operation == 'mathSin':
        return math.sin(args[0])
        
    if operation == 'mathTan':
        return math.tan(args[0])

    # Logarithmic
    if operation == 'mathLog':
        return math.log(args[0])
        
    if operation == 'mathLog10':
        return math.log10(args[0])
        
    if operation == 'mathExp':
        return math.exp(args[0])

    return None



bisect.bisect_left(args[0], args[1])

def calculate_syntax(self, syntax_list, *args):
    syntax_info = self.registry['syntax_registry']['elements'].get(syntax_list['name'])
    
    if syntax_info:
        if syntax_list['name'] == 'arrAbs':
            return [abs(x) for x in args[0]]
        elif syntax_list['name'] == 'arrAvg':
            return sum(args[0]) / len(args[0])
        elif syntax_list['name'] == 'arrBinarySearch':
            return bisect.bisect_left(args[0], args[1])
        elif syntax_list['name'] == 'arrBinarySearchLeftmost':
            return bisect.bisect_left(args[0], args[1])
        elif syntax_list['name'] == 'arrBinarySearchRightmost':
            return bisect.bisect_right(args[0], args[1])
        elif syntax_list['name'] == 'arrClear':
            args[0].clear()
            return args[0]
        elif syntax_list['name'] == 'arrConcat':
            return args[0] + args[1]
        elif syntax_list['name'] == 'arrCopy':
            return args[0].copy()
        elif syntax_list['name'] == 'arrCovariance':
            return np.cov(args[0], args[1])[0][1]
        elif syntax_list['name'] == 'arrEvery':
            return all(args[1](x) for x in args[0])
        elif syntax_list['name'] == 'arrFill':
            return [args[1]] * len(args[0])
        elif syntax_list['name'] == 'arrFirst':
            return args[0][0] if args[0] else None
        elif syntax_list['name'] == 'arrFrom':
            return list(args[0])
        elif syntax_list['name'] == 'arrGet':
            return args[0][args[1]]
        elif syntax_list['name'] == 'arrIncludes':
            return args[1] in args[0]
        elif syntax_list['name'] == 'arrIndexOf':
            return args[0].index(args[1]) if args[1] in args[0] else -1
        elif syntax_list['name'] == 'arrInsert':
            args[0].insert(args[1], args[2])
            return args[0]
        elif syntax_list['name'] == 'arrJoin':
            return args[1].join(map(str, args[0]))
        elif syntax_list['name'] == 'arrLast':
            return args[0][-1] if args[0] else None
        elif syntax_list['name'] == 'arrLastIndexOf':
            return len(args[0]) - 1 - args[0][::-1].index(args[1]) if args[1] in args[0] else -1
        elif syntax_list['name'] == 'arrMax':
            return max(args[0])
        elif syntax_list['name'] == 'arrMedian':
            return statistics.median(args[0])
        elif syntax_list['name'] == 'arrMin':
            return min(args[0])
        elif syntax_list['name'] == 'arrMode':
            return statistics.mode(args[0])
        elif syntax_list['name'] == 'arrNewBool':
            return [False] * args[0]
        elif syntax_list['name'] == 'arrNewBox':
            return [None] * args[0]
        elif syntax_list['name'] == 'arrNewFloat':
            return [0.0] * args[0]
        elif syntax_list['name'] == 'arrNewInt':
            return [0] * args[0]
        elif syntax_list['name'] == 'arrNewLabel':
            return [None] * args[0]
        elif syntax_list['name'] == 'arrNewLine':
            return [None] * args[0]
        elif syntax_list['name'] == 'arrNewLineFill':
            return [None] * args[0]
        elif syntax_list['name'] == 'arrNewString':
            return [''] * args[0]
        elif syntax_list['name'] == 'arrNewTable':
            return [None] * args[0]
        elif syntax_list['name'] == 'arrNewType':
            return [None] * args[0]
        elif syntax_list['name'] == 'arrPercentileLinearInterpolation':
            return np.percentile(args[0], args[1])
        elif syntax_list['name'] == 'arrPercentileNearestRank':
            return np.percentile(args[0], args[1], interpolation='nearest')
        elif syntax_list['name'] == 'arrPercentRank':
            return [sum(x < val for x in args[0]) / len(args[0]) for val in args[0]]
        elif syntax_list['name'] == 'arrPop':
            return args[0].pop()
        elif syntax_list['name'] == 'arrPush':
            args[0].append(args[1])
            return args[0]
        elif syntax_list['name'] == 'arrRange':
            return list(range(args[0], args[1], args[2] if len(args) > 2 else 1))
        elif syntax_list['name'] == 'arrRemove':
            args[0].remove(args[1])
            return args[0]
        elif syntax_list['name'] == 'arrReverse':
            return args[0][::-1]
        elif syntax_list['name'] == 'arrSet':
            args[0][args[1]] = args[2]
            return args[0]
        elif syntax_list['name'] == 'arrShift':
            return args[0].pop(0) if args[0] else None
        elif syntax_list['name'] == 'arrSize':
            return len(args[0])
        elif syntax_list['name'] == 'arrSlice':
            return args[0][args[1]:args[2]]
        elif syntax_list['name'] == 'arrSome':
            return any(args[1](x) for x in args[0])
        elif syntax_list['name'] == 'arrSort':
            return sorted(args[0], reverse=args[1] if len(args) > 1 else False)
        elif syntax_list['name'] == 'arrSortIndices':
            return sorted(range(len(args[0])), key=lambda k: args[0][k], reverse=args[1] if len(args) > 1 else False)
        elif syntax_list['name'] == 'arrStandardize':
            mean = sum(args[0]) / len(args[0])
            std = (sum((x - mean) ** 2 for x in args[0]) / len(args[0])) ** 0.5
            return [(x - mean) / std for x in args[0]]
        elif syntax_list['name'] == 'arrStdev':
            return statistics.stdev(args[0])
        elif syntax_list['name'] == 'arrSum':
            return sum(args[0])
        elif syntax_list['name'] == 'arrUnshift':
            args[0].insert(0, args[1])
            return args[0]
        elif syntax_list['name'] == 'arrVariance':
            return statistics.variance(args[0])














def calculate_syntax(self, syntax_list, *args):
    syntax_info = self.registry['syntax_registry']['elements'].get(syntax_list['name'])
    
    if syntax_info:
        if syntax_list['name'] == 'arrAbs':
            return [abs(x) for x in args[0]]
            
        elif syntax_list['name'] == 'arrAvg':
            return sum(args[0]) / len(args[0])
            
        elif syntax_list['name'] == 'arrBinarySearch':
            left, right = 0, len(args[0]) - 1
            while left <= right:
                mid = (left + right) // 2
                if args[0][mid] == args[1]:
                    return mid
                elif args[0][mid] < args[1]:
                    left = mid + 1
                else:
                    right = mid - 1
            return left
            
        elif syntax_list['name'] == 'arrBinarySearchLeftmost':
            left, right = 0, len(args[0])
            while left < right:
                mid = (left + right) // 2
                if args[0][mid] < args[1]:
                    left = mid + 1
                else:
                    right = mid
            return left
            
        elif syntax_list['name'] == 'arrBinarySearchRightmost':
            left, right = 0, len(args[0])
            while left < right:
                mid = (left + right) // 2
                if args[0][mid] <= args[1]:
                    left = mid + 1
                else:
                    right = mid
            return left
            
        elif syntax_list['name'] == 'arrClear':
            args[0] = []
            return args[0]
            
        elif syntax_list['name'] == 'arrConcat':
            result = []
            for x in args[0]:
                result.append(x)
            for x in args[1]:
                result.append(x)
            return result
            
        elif syntax_list['name'] == 'arrCopy':
            result = []
            for x in args[0]:
                result.append(x)
            return result
            
        elif syntax_list['name'] == 'arrCovariance':
            mean1 = sum(args[0]) / len(args[0])
            mean2 = sum(args[1]) / len(args[1])
            sum_of_products = sum((x - mean1) * (y - mean2) for x, y in zip(args[0], args[1]))
            return sum_of_products / len(args[0])
            
        elif syntax_list['name'] == 'arrEvery':
            for x in args[0]:
                if not args[1](x):
                    return False
            return True
            
        elif syntax_list['name'] == 'arrFill':
            result = []
            for _ in range(len(args[0])):
                result.append(args[1])
            return result
            
        elif syntax_list['name'] == 'arrFirst':
            if len(args[0]) > 0:
                return args[0][0]
            return None
            
        elif syntax_list['name'] == 'arrFrom':
            result = []
            for x in args[0]:
                result.append(x)
            return result
            
        elif syntax_list['name'] == 'arrGet':
            return args[0][args[1]]
            
        elif syntax_list['name'] == 'arrIncludes':
            for x in args[0]:
                if x == args[1]:
                    return True
            return False
            
        elif syntax_list['name'] == 'arrIndexOf':
            for i in range(len(args[0])):
                if args[0][i] == args[1]:
                    return i
            return -1
            
        elif syntax_list['name'] == 'arrInsert':
            result = []
            for i in range(len(args[0])):
                if i == args[1]:
                    result.append(args[2])
                result.append(args[0][i])
            if args[1] >= len(args[0]):
                result.append(args[2])
            return result
            
        elif syntax_list['name'] == 'arrJoin':
            result = str(args[0][0]) if args[0] else ""
            for x in args[0][1:]:
                result += args[1] + str(x)
            return result
            
        elif syntax_list['name'] == 'arrLast':
            if len(args[0]) > 0:
                return args[0][-1]
            return None
            
        elif syntax_list['name'] == 'arrLastIndexOf':
            for i in range(len(args[0])-1, -1, -1):
                if args[0][i] == args[1]:
                    return i
            return -1
            
        elif syntax_list['name'] == 'arrMax':
            if not args[0]:
                return None
            max_val = args[0][0]
            for x in args[0][1:]:
                if x > max_val:
                    max_val = x
            return max_val
            
        elif syntax_list['name'] == 'arrMedian':
            sorted_arr = []
            for x in args[0]:
                sorted_arr.append(x)
            for i in range(len(sorted_arr)):
                for j in range(len(sorted_arr)-1-i):
                    if sorted_arr[j] > sorted_arr[j+1]:
                        sorted_arr[j], sorted_arr[j+1] = sorted_arr[j+1], sorted_arr[j]
            n = len(sorted_arr)
            if n % 2 == 0:
                return (sorted_arr[n//2-1] + sorted_arr[n//2]) / 2
            return sorted_arr[n//2]
            
        elif syntax_list['name'] == 'arrMin':
            if not args[0]:
                return None
            min_val = args[0][0]
            for x in args[0][1:]:
                if x < min_val:
                    min_val = x
            return min_val
            
        elif syntax_list['name'] == 'arrMode':
            if not args[0]:
                return None
            counts = {}
            for x in args[0]:
                if x in counts:
                    counts[x] += 1
                else:
                    counts[x] = 1
            max_count = 0
            mode = None
            for x, count in counts.items():
                if count > max_count:
                    max_count = count
                    mode = x
            return mode
            
        elif syntax_list['name'] == 'arrNewBox':
            result = []
            for _ in range(args[0]):
                result.append(None)
            return result
            
        elif syntax_list['name'] == 'aryNewCol':
            result = []
            for _ in range(args[0]):
                result.append([])
            return result
            
        elif syntax_list['name'] == 'arrNewLabel':
            result = []
            for _ in range(args[0]):
                result.append(None)
            return result
            
        elif syntax_list['name'] == 'arrNewLine':
            result = []
            for _ in range(args[0]):
                result.append(None)
            return result
            
        elif syntax_list['name'] == 'arrNewLineFill':
            result = []
            for _ in range(args[0]):
                result.append(None)
            return result
            
        elif syntax_list['name'] == 'arrNewTable':
            result = []
            for _ in range(args[0]):
                result.append(None)
            return result
            
        elif syntax_list['name'] == 'arrNewType':
            result = []
            for _ in range(args[0]):
                result.append(None)
            return result
            
        elif syntax_list['name'] == 'arrPercentileLinearInterpolation':
            sorted_arr = sorted(args[0])
            rank = args[1] * (len(sorted_arr) - 1) / 100
            lower_idx = int(rank)
            fraction = rank - lower_idx
            if lower_idx >= len(sorted_arr) - 1:
                return sorted_arr[-1]
            return sorted_arr[lower_idx] + fraction * (sorted_arr[lower_idx + 1] - sorted_arr[lower_idx])
            
        elif syntax_list['name'] == 'arrPercentileNearestRank':
            sorted_arr = sorted(args[0])
            rank = round(args[1] * (len(sorted_arr) - 1) / 100)
            return sorted_arr[rank]
            
        elif syntax_list['name'] == 'arrRemove':
            result = []
            for x in args[0]:
                if x != args[1]:
                    result.append(x)
            return result
            
        elif syntax_list['name'] == 'arrSome':
            for x in args[0]:
                if args[1](x):
                    return True
            return False
            
        elif syntax_list['name'] == 'arrSortIndices':
            indices = list(range(len(args[0])))
            for i in range(len(indices)):
                for j in range(len(indices)-1-i):
                    if args[0][indices[j]] > args[0][indices[j+1]]:
                        indices[j], indices[j+1] = indices[j+1], indices[j]
            return indices

        elif syntax_list['name'] == 'arrNewBool':
            result = []
            for _ in range(args[0]):
                result.append(False)
            return result
            
        elif syntax_list['name'] == 'arrNewFloat':
            result = []
            for _ in range(args[0]):
                result.append(0.0)
            return result
            
        elif syntax_list['name'] == 'arrNewInt':
            result = []
            for _ in range(args[0]):
                result.append(0)
            return result
            
        elif syntax_list['name'] == 'arrNewString':
            result = []
            for _ in range(args[0]):
                result.append("")
            return result
            
        elif syntax_list['name'] == 'arrPercentRank':
            result = []
            for val in args[0]:
                count = 0
                for x in args[0]:
                    if x < val:
                        count += 1
                result.append(count / len(args[0]))
            return result
            
        elif syntax_list['name'] == 'arrPop':
            if len(args[0]) > 0:
                last_val = args[0][-1]
                args[0] = args[0][:-1]
                return last_val
            return None
            
        elif syntax_list['name'] == 'arrPush':
            args[0].append(args[1])
            return len(args[0])
            
        elif syntax_list['name'] == 'arrRange':
            start = args[0]
            end = args[1]
            step = args[2] if len(args) > 2 else 1
            result = []
            current = start
            while (step > 0 and current < end) or (step < 0 and current > end):
                result.append(current)
                current += step
            return result
            
        elif syntax_list['name'] == 'arrReverse':
            result = []
            for i in range(len(args[0])-1, -1, -1):
                result.append(args[0][i])
            return result
            
        elif syntax_list['name'] == 'arrSet':
            args[0][args[1]] = args[2]
            return args[0]
            
        elif syntax_list['name'] == 'arrShift':
            if len(args[0]) > 0:
                first_val = args[0][0]
                args[0] = args[0][1:]
                return first_val
            return None
            
        elif syntax_list['name'] == 'arrSize':
            count = 0
            for _ in args[0]:
                count += 1
            return count
            
        elif syntax_list['name'] == 'arrSlice':
            result = []
            start = args[1]
            end = args[2]
            for i in range(start, end):
                result.append(args[0][i])
            return result
            
        elif syntax_list['name'] == 'arrSort':
            result = args[0].copy()
            for i in range(len(result)):
                for j in range(len(result)-1-i):
                    if result[j] > result[j+1]:
                        result[j], result[j+1] = result[j+1], result[j]
            return result
            
        elif syntax_list['name'] == 'arrStandardize':
            mean = sum(args[0]) / len(args[0])
            squared_diff_sum = sum((x - mean) ** 2 for x in args[0])
            std_dev = (squared_diff_sum / len(args[0])) ** 0.5
            return [(x - mean) / std_dev for x in args[0]]
            
        elif syntax_list['name'] == 'arrStdev':
            mean = sum(args[0]) / len(args[0])
            squared_diff_sum = sum((x - mean) ** 2 for x in args[0])
            return (squared_diff_sum / (len(args[0]) - 1)) ** 0.5
            
        elif syntax_list['name'] == 'arrSum':
            total = 0
            for x in args[0]:
                total += x
            return total
            
        elif syntax_list['name'] == 'arrUnshift':
            result = [args[1]]
            for x in args[0]:
                result.append(x)
            return result
            
        elif syntax_list['name'] == 'arrVariance':
            mean = sum(args[0]) / len(args[0])
            squared_diff_sum = sum((x - mean) ** 2 for x in args[0])
            return squared_diff_sum / (len(args[0]) - 1)












        elif syntax_list['name'] == 'boxFunc':
            return {
                'left': 0,
                'top': 0,
                'right': 0,
                'bottom': 0,
                'text': '',
                'bgColor': '#FFFFFF',
                'borderColor': '#000000',
                'borderWidth': 1,
                'borderStyle': 'solid',
                'textColor': '#000000',
                'textSize': 12,
                'textAlign': 'center',
                'textVAlign': 'middle',
                'textWrap': 'none',
                'textFontFamily': 'Arial'
            }
            
        elif syntax_list['name'] == 'boxCopyFunc':
            return {
                'left': args[0]['left'],
                'top': args[0]['top'],
                'right': args[0]['right'],
                'bottom': args[0]['bottom'],
                'text': args[0]['text'],
                'bgColor': args[0]['bgColor'],
                'borderColor': args[0]['borderColor'],
                'borderWidth': args[0]['borderWidth'],
                'borderStyle': args[0]['borderStyle'],
                'textColor': args[0]['textColor'],
                'textSize': args[0]['textSize'],
                'textAlign': args[0]['textAlign'],
                'textVAlign': args[0]['textVAlign'],
                'textWrap': args[0]['textWrap'],
                'textFontFamily': args[0]['textFontFamily']
            }
            
        elif syntax_list['name'] == 'boxDeleteFunc':
            args[0] = None
            return True
            
        elif syntax_list['name'] == 'boxGetBottomFunc':
            return args[0]['bottom']
            
        elif syntax_list['name'] == 'boxGetLeftFunc':
            return args[0]['left']
            
        elif syntax_list['name'] == 'boxGetRightFunc':
            return args[0]['right']
            
        elif syntax_list['name'] == 'boxGetTopFunc':
            return args[0]['top']
            
        elif syntax_list['name'] == 'boxNewFunc':
            return {
                'left': args[0],
                'top': args[1],
                'right': args[2],
                'bottom': args[3]
            }
            
        elif syntax_list['name'] == 'boxSetBgColFunc':
            args[0]['bgColor'] = args[1]
            return args[0]
            
        elif syntax_list['name'] == 'boxSetBorderColFunc':
            args[0]['borderColor'] = args[1]
            return args[0]
            
        elif syntax_list['name'] == 'boxSetBorderStyleFunc':
            args[0]['borderStyle'] = args[1]
            return args[0]
            
        elif syntax_list['name'] == 'boxSetBorderWidthFunc':
            args[0]['borderWidth'] = args[1]
            return args[0]
            
        elif syntax_list['name'] == 'boxSetBottomFunc':
            args[0]['bottom'] = args[1]
            return args[0]
            
        elif syntax_list['name'] == 'boxSetBottomRightPointFunc':
            args[0]['bottom'] = args[1]
            args[0]['right'] = args[2]
            return args[0]
            
        elif syntax_list['name'] == 'boxSetExtendFunc':
            args[0]['extend'] = args[1]
            return args[0]
            
        elif syntax_list['name'] == 'boxSetLeftFunc':
            args[0]['left'] = args[1]
            return args[0]
            
        elif syntax_list['name'] == 'boxSetLeftTopFunc':
            args[0]['left'] = args[1]
            args[0]['top'] = args[2]
            return args[0]
            
        elif syntax_list['name'] == 'boxSetRightFunc':
            args[0]['right'] = args[1]
            return args[0]
            
        elif syntax_list['name'] == 'boxSetRightBottomFunc':
            args[0]['right'] = args[1]
            args[0]['bottom'] = args[2]
            return args[0]
            
        elif syntax_list['name'] == 'boxSetTextFunc':
            args[0]['text'] = args[1]
            return args[0]
            
        elif syntax_list['name'] == 'boxSetTextColFunc':
            args[0]['textColor'] = args[1]
            return args[0]
            
        elif syntax_list['name'] == 'boxSetTextFontFamilyFunc':
            args[0]['textFontFamily'] = args[1]
            return args[0]
            
        elif syntax_list['name'] == 'boxSetTextHAlignFunc':
            args[0]['textAlign'] = args[1]
            return args[0]
            
        elif syntax_list['name'] == 'boxSetTextSizeFunc':
            args[0]['textSize'] = args[1]
            return args[0]
            
        elif syntax_list['name'] == 'boxSetTextVAlignFunc':
            args[0]['textVAlign'] = args[1]
            return args[0]
            
        elif syntax_list['name'] == 'boxSetTextWrapFunc':
            args[0]['textWrap'] = args[1]
            return args[0]
            
        elif syntax_list['name'] == 'boxSetTopFunc':
            args[0]['top'] = args[1]
            return args[0]
            
        elif syntax_list['name'] == 'boxSetTopLeftPointFunc':
            args[0]['top'] = args[1]
            args[0]['left'] = args[2]
            return args[0]
