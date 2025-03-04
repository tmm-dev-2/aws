from typing import Dict, List, Set

class SyntaxList:
    def __init__(self):
        # Core Market Data
        self.market_data = {
            'price': ['open', 'high', 'low', 'close', 'volume', 'hl2', 'hlc3', 'hlcc4', 'ohlc4', 
                     'typical_price', 'weighted_close', 'median_price', 'average_price'],
            'bar': ['bar_index', 'bar_time', 'bar_state', 'barStateIsConfirmed', 'barStateIsFirst', 
                   'barStateIsHistory', 'barStateIsLast', 'barStateIsLastConfirmedHistory', 
                   'barStateIsNew', 'barStateIsRealtime'],
            'tick': ['tick_volume', 'tick_price', 'tick_direction', 'tick_size', 'tick_id']
        }

        # Technical Analysis - Complete TA-Lib Integration
        self.technical = {
            'moving_averages': [
                'sma', 'ema', 'wma', 'dema', 'tema', 'trima', 'kama', 'mama', 'fama', 't3',
                'ma_adaptive', 'ma_weighted_time', 'ma_elastic', 'ma_hull', 'ma_arnaud_legoux',
                'ma_mcginley', 'ma_running', 'ma_arnaud', 'ma_geometric', 'ma_kaufman'
            ],
            'oscillators': [
                'rsi', 'stoch', 'stochf', 'stochrsi', 'macd', 'macdext', 'macdfix', 'ppo', 
                'apo', 'cmo', 'mom', 'roc', 'rocr', 'rocr100', 'trix', 'willr', 'cci', 'dmi',
                'dx', 'minus_di', 'minus_dm', 'plus_di', 'plus_dm', 'mfi', 'ultimate'
            ],
            'volatility': [
                'bbands', 'atr', 'natr', 'keltner', 'stdev', 'variance', 'standarddev',
                'chaikin_volatility', 'donchian', 'bollinger_bands_width', 'keltner_channels_width',
                'volatility_index', 'historical_volatility', 'parkinsons_volatility'
            ],
            'volume': [
                'obv', 'ad', 'adosc', 'mfi', 'volume_profile', 'volume_weighted_average_price',
                'volume_oscillator', 'volume_ratio', 'negative_volume_index', 'positive_volume_index',
                'price_volume_trend', 'volume_weighted_macd', 'volume_weighted_rsi'
            ],
            'momentum': [
                'adx', 'adxr', 'aroon', 'aroonosc', 'bop', 'cci', 'cmo', 'dx', 'macd', 'mfi',
                'minus_di', 'minus_dm', 'mom', 'plus_di', 'plus_dm', 'ppo', 'roc', 'rocp',
                'rocr', 'rocr100', 'rsi', 'stoch', 'stochf', 'stochrsi', 'trix', 'ultosc',
                'willr'
            ],
            'trend': [
                'adx', 'dmi', 'ichimoku', 'supertrend', 'zigzag', 'trend_strength', 'trend_direction',
                'trend_intensity', 'trend_score', 'trend_stability', 'trend_efficiency',
                'trend_quality', 'trend_fisher', 'trend_regression', 'trend_correlation'
            ],
            'cycle': [
                'ht_dcperiod', 'ht_dcphase', 'ht_phasor', 'ht_sine', 'ht_trendmode',
                'cycle_identifier', 'cycle_period', 'cycle_amplitude', 'cycle_phase',
                'cycle_forecast', 'cycle_momentum', 'cycle_strength'
            ],
            'statistic': [
                'beta', 'correl', 'linearreg', 'linearreg_angle', 'linearreg_intercept',
                'linearreg_slope', 'stddev', 'tsf', 'var', 'covariance', 'pearson',
                'spearman', 'kendall', 'regression_quality'
            ]
        }

        # Candlestick Patterns - Complete Set
        self.candlestick_patterns = {
            'single_candle': [
                'CDL_DOJI', 'CDL_DOJI_STAR', 'CDL_DRAGONFLY_DOJI', 'CDL_GRAVESTONE_DOJI',
                'CDL_HAMMER', 'CDL_HANGING_MAN', 'CDL_INVERTED_HAMMER', 'CDL_SHOOTING_STAR',
                'CDL_SPINNING_TOP', 'CDL_MARUBOZU', 'CDL_LONG_LINE', 'CDL_SHORT_LINE'
            ],
            'double_candle': [
                'CDL_ENGULFING', 'CDL_HARAMI', 'CDL_HARAMI_CROSS', 'CDL_PIERCING',
                'CDL_DARK_CLOUD_COVER', 'CDL_KICKING', 'CDL_MEETING_LINES', 'CDL_MATCHING_LOW',
                'CDL_COUNTERATTACK', 'CDL_SEPARATING_LINES'
            ],
            'triple_candle': [
                'CDL_MORNING_STAR', 'CDL_EVENING_STAR', 'CDL_MORNING_DOJI_STAR',
                'CDL_EVENING_DOJI_STAR', 'CDL_THREE_WHITE_SOLDIERS', 'CDL_THREE_BLACK_CROWS',
                'CDL_THREE_INSIDE', 'CDL_THREE_OUTSIDE', 'CDL_THREE_LINE_STRIKE',
                'CDL_THREE_STARS_IN_SOUTH'
            ],
            'multi_candle': [
                'CDL_ABANDONED_BABY', 'CDL_ADVANCE_BLOCK', 'CDL_BELT_HOLD', 'CDL_BREAKAWAY',
                'CDL_CONCEALING_BABY_SWALLOW', 'CDL_HIKKAKE', 'CDL_HIKKAKE_MOD',
                'CDL_IDENTICAL_THREE_CROWS', 'CDL_IN_NECK', 'CDL_LADDER_BOTTOM',
                'CDL_MATCHING_LOW', 'CDL_MAT_HOLD', 'CDL_ON_NECK', 'CDL_RICKSHAW_MAN',
                'CDL_RISE_FALL_THREE_METHODS', 'CDL_STICK_SANDWICH', 'CDL_TAKURI',
                'CDL_TASUKI_GAP', 'CDL_THRUSTING', 'CDL_TRISTAR', 'CDL_UNIQUE_THREE_RIVER',
                'CDL_UPSIDE_GAP_TWO_CROWS', 'CDL_XSIDE_GAP_THREE_METHODS'
            ]
        }

                # Strategy Components - Complete Trading System
        self.strategy = {
            'entry_exit': [
                'strategy_entry_long', 'strategy_entry_short', 'strategy_exit', 'strategy_close',
                'strategy_cancel', 'strategy_cancel_all', 'strategy_close_all', 'strategy_order',
                'strategy_order_cancel', 'strategy_risk_allow_entry'
            ],
            'position_management': [
                'strategy_position_size', 'strategy_position_avg_price', 'strategy_position_entry_name',
                'strategy_position_entry_bar', 'strategy_position_entry_time', 'strategy_position_entry_price',
                'strategy_position_entry_id', 'strategy_position_entry_comment'
            ],
            'risk_management': [
                'strategy_risk_max_position', 'strategy_risk_max_drawdown', 'strategy_risk_max_loss',
                'strategy_risk_max_trades', 'strategy_risk_max_loss_days', 'strategy_risk_max_correlation',
                'strategy_risk_max_exposure', 'strategy_risk_position_size'
            ],
            'performance_metrics': [
                'strategy_equity', 'strategy_net_profit', 'strategy_gross_profit', 'strategy_gross_loss',
                'strategy_profit_factor', 'strategy_max_drawdown', 'strategy_recovery_factor',
                'strategy_sharpe_ratio', 'strategy_sortino_ratio', 'strategy_calmar_ratio',
                'strategy_trades_total', 'strategy_trades_won', 'strategy_trades_lost',
                'strategy_win_rate', 'strategy_avg_trade', 'strategy_avg_winning_trade',
                'strategy_avg_losing_trade', 'strategy_largest_win', 'strategy_largest_loss',
                'strategy_max_contracts_held', 'strategy_max_leverage_used'
            ],
            'trade_management': [
                'strategy_margin_initial', 'strategy_margin_maintenance', 'strategy_commission_amount',
                'strategy_commission_percent', 'strategy_slippage_amount', 'strategy_slippage_percent',
                'strategy_rollover_fee', 'strategy_swap_long', 'strategy_swap_short'
            ]
        }

        # Symbol Information - Complete Market Data
        self.symbol_info = {
            'basic': [
                'syminfo_ticker', 'syminfo_description', 'syminfo_type', 'syminfo_root',
                'syminfo_prefix', 'syminfo_suffix', 'syminfo_currency', 'syminfo_exchange'
            ],
            'trading': [
                'syminfo_mintick', 'syminfo_minmove', 'syminfo_pointvalue', 'syminfo_pricescale',
                'syminfo_pipsize', 'syminfo_pipvalue', 'syminfo_minlot', 'syminfo_maxlot',
                'syminfo_lotstep', 'syminfo_margin_initial', 'syminfo_margin_maintenance'
            ],
            'session': [
                'syminfo_session', 'syminfo_session_regular', 'syminfo_session_extended',
                'syminfo_session_premarket', 'syminfo_session_postmarket', 'syminfo_timezone'
            ],
            'fundamental': [
                'syminfo_industry', 'syminfo_sector', 'syminfo_market_cap', 'syminfo_volume_avg',
                'syminfo_dividend_yield', 'syminfo_earnings_per_share', 'syminfo_price_earnings',
                'syminfo_shares_outstanding', 'syminfo_float_shares'
            ]
        }

        # Chart Elements - Complete Visualization System
        self.chart = {
            'styles': [
                'style_line', 'style_stepline', 'style_histogram', 'style_cross', 'style_circles',
                'style_area', 'style_columns', 'style_bars', 'style_candlesticks', 'style_renko',
                'style_kagi', 'style_pointfigure', 'style_linebreak'
            ],
            'colors': [
                'color_aqua', 'color_black', 'color_blue', 'color_fuchsia', 'color_gray',
                'color_green', 'color_lime', 'color_maroon', 'color_navy', 'color_olive',
                'color_orange', 'color_purple', 'color_red', 'color_silver', 'color_teal',
                'color_white', 'color_yellow', 'color_from_gradient'
            ],
            'drawing_tools': [
                'line_new', 'line_delete', 'line_set_xy1', 'line_set_xy2', 'line_set_color',
                'line_set_width', 'line_set_style', 'box_new', 'box_delete', 'box_set_bounds',
                'box_set_bgcolor', 'box_set_border_color', 'box_set_border_width',
                'label_new', 'label_delete', 'label_set_text', 'label_set_xy', 'label_set_color',
                'label_set_style', 'table_new', 'table_delete', 'table_cell_set', 'table_cell_get'
            ],
            'indicators': [
                'indicator_buffers', 'indicator_color', 'indicator_width', 'indicator_style',
                'indicator_maximum', 'indicator_minimum', 'indicator_overlay', 'indicator_separate'
            ]
        }


                # Time and Date Functions - Complete Time Management
        self.time = {
            'components': [
                'time', 'time_close', 'time_open', 'time_high', 'time_low', 'time_tradingday',
                'year', 'month', 'weekofyear', 'dayofmonth', 'dayofweek', 'hour', 'minute', 'second',
                'time_format', 'time_local', 'time_gmt', 'timestamp'
            ],
            'session_states': [
                'session_ismarket', 'session_ispremarket', 'session_ispostmarket',
                'session_isfirstbar', 'session_islastbar', 'session_isrealtime',
                'session_regular', 'session_extended', 'session_holidays'
            ],
            'time_conversions': [
                'time_to_string', 'time_from_string', 'time_to_unix', 'time_from_unix',
                'time_to_timezone', 'time_from_timezone', 'time_period_start', 'time_period_end'
            ]
        }

        # Array and Matrix Operations - Complete Data Structure Management
        self.arrays = {
            'creation': [
                'array_new_float', 'array_new_int', 'array_new_bool', 'array_new_string',
                'array_new_color', 'array_new_line', 'array_new_label', 'array_new_box'
            ],
            'manipulation': [
                'array_push', 'array_pop', 'array_insert', 'array_remove', 'array_shift',
                'array_unshift', 'array_slice', 'array_splice', 'array_join', 'array_reverse'
            ],
            'operations': [
                'array_sum', 'array_avg', 'array_median', 'array_mode', 'array_stdev',
                'array_variance', 'array_covariance', 'array_min', 'array_max', 'array_sort'
            ],
            'search': [
                'array_indexOf', 'array_lastIndexOf', 'array_includes', 'array_find',
                'array_findIndex', 'array_every', 'array_some', 'array_filter', 'array_map'
            ]
        }

        # Matrix Operations
        self.matrix = {
            'creation': [
                'matrix_new', 'matrix_new_from_arrays', 'matrix_new_identity',
                'matrix_new_zero', 'matrix_new_ones', 'matrix_new_random'
            ],
            'operations': [
                'matrix_add', 'matrix_subtract', 'matrix_multiply', 'matrix_divide',
                'matrix_transpose', 'matrix_inverse', 'matrix_determinant', 'matrix_eigenvalues'
            ],
            'manipulation': [
                'matrix_set', 'matrix_get', 'matrix_row', 'matrix_col', 'matrix_submatrix',
                'matrix_reshape', 'matrix_concat', 'matrix_decomposition'
            ]
        }

        # Advanced Mathematical Functions
        self.math = {
            'basic': [
                'abs', 'pow', 'sqrt', 'cbrt', 'exp', 'log', 'log10', 'floor', 'ceil',
                'round', 'sign', 'max', 'min', 'avg', 'sum', 'product'
            ],
            'trigonometric': [
                'sin', 'cos', 'tan', 'asin', 'acos', 'atan', 'atan2', 'sinh', 'cosh',
                'tanh', 'degrees', 'radians'
            ],
            'statistical': [
                'correlation', 'covariance', 'standarddev', 'variance', 'skew', 'kurtosis',
                'percentile', 'zscore', 'normal_cdf', 'normal_inverse'
            ],
            'financial': [
                'pv', 'fv', 'nper', 'pmt', 'irr', 'npv', 'xirr', 'xnpv', 'mirr',
                'rate', 'duration', 'modified_duration', 'convexity'
            ]
        }
                # Advanced Chart Patterns and Formations
        self.formations = {
            'elliott_wave': [
                'wave_degree', 'wave_position', 'wave_count', 'wave_pattern',
                'wave_validation', 'wave_projection', 'wave_retracement', 'wave_extension'
            ],
            'harmonic_patterns': [
                'pattern_gartley', 'pattern_butterfly', 'pattern_bat', 'pattern_crab',
                'pattern_shark', 'pattern_cypher', 'pattern_5o', 'pattern_wolfe_waves'
            ],
            'fibonacci': [
                'fib_retracement', 'fib_extension', 'fib_projection', 'fib_circles',
                'fib_spirals', 'fib_timezones', 'fib_channels', 'fib_expansion'
            ]
        }
        self.ml = {
        'models': [
            'train_model', 'predict', 'cross_validate',
            'optimize_params', 'feature_importance',
            'create_features', 'normalize_features'
        ],
        'algorithms': [
            'linear_regression', 'random_forest', 'svm',
            'neural_network', 'gradient_boost', 'kmeans',
            'isolation_forest'
        ],
        'evaluation': [
            'calculate_metrics', 'confusion_matrix',
            'precision_recall', 'roc_curve', 'learning_curve'
        ],
        'preprocessing': [
            'scale_features', 'pca_transform',
            'rolling_features', 'lag_features',
            'technical_features'
        ]
    }
        self.plot={    'plotting': {
        'basic_plots': [
            'plot', 'plotshape', 'plotchar', 'plotarrow', 'plotcandle',
            'plotbar', 'plothistogram', 'plotscatter', 'plotarea',
            'plotbubble', 'plotmap', 'plotcandlestick', 'plotvolume',
            'plotprofile', 'plotheatmap', 'plotzig', 'plotchart'
        ],
        'lines': [
            'hline', 'vline', 'line', 'trendline', 'rayline', 'polyline',
            'linefill', 'linebreak', 'linestyle', 'linewidth', 'linecolor'
        ],
        'shapes': [
            'box', 'rectangle', 'circle', 'triangle', 'diamond',
            'cross', 'arrowup', 'arrowdown', 'flag', 'square',
            'star', 'pentagon', 'hexagon', 'ellipse'
        ],
        'tables': [
            'table.new', 'table.set', 'table.cell', 'table.col',
            'table.row', 'table.merge', 'table.delete', 'table.clear',
            'table.style', 'table.border', 'table.align', 'table.format'
        ],
        'labels': [
            'label.new', 'label.set', 'label.delete', 'label.text',
            'label.style', 'label.color', 'label.size', 'label.align',
            'label.position', 'label.tooltip', 'label.format'
        ],
        'colors': [
            'bgcolor', 'barcolor', 'textcolor', 'fillcolor', 'bordercolor',
            'gradientcolor', 'transparencycolor', 'colorblend', 'colorrgb',
            'colorhsl', 'colorfade', 'colormix'
        ],
        'styles': [
            'style.solid', 'style.dotted', 'style.dashed', 'style.arrow',
            'style.circle', 'style.cross', 'style.diamond', 'style.square',
            'style.triangleup', 'style.triangledown', 'style.flag',
            'style.label', 'style.text', 'style.histogram'
        ],
        'chart_settings': [
            'chart.overlay', 'chart.separate', 'chart.same_scale',
            'chart.style', 'chart.theme', 'chart.grid', 'chart.background',
            'chart.selection', 'chart.zoom', 'chart.time_scale'
        ]
    }
        }
        # Market Microstructure
        self.microstructure = {
            'order_flow': [
                'volume_delta', 'volume_imbalance', 'order_flow_imbalance', 'trade_flow',
                'liquidity_analysis', 'market_depth', 'bid_ask_spread', 'tick_analysis'
            ],
            'auction': [
                'market_profile', 'volume_profile', 'time_price_opportunity', 'value_area',
                'point_of_control', 'balance_areas', 'excess_areas', 'auction_zones'
            ]
        }

        # Intermarket Analysis
        self.intermarket = {
            'correlations': [
                'asset_correlation', 'sector_correlation', 'market_correlation',
                'currency_correlation', 'commodity_correlation', 'cross_asset_analysis'
            ],
            'relative_strength': [
                'relative_rotation', 'relative_momentum', 'relative_strength_index',
                'comparative_strength', 'sector_rotation', 'market_breadth'
            ]
        }

        # Event Handling and Automation
        self.automation = {
            'alerts': [
                'alert_condition', 'alert_message', 'alert_email', 'alert_sms',
                'alert_webhook', 'alert_sound', 'alert_push', 'alert_telegram'
            ],
            'scheduling': [
                'schedule_daily', 'schedule_weekly', 'schedule_monthly',
                'schedule_custom', 'schedule_market', 'schedule_session'
            ]
        }

        self.risk = {
            'position_sizing': [
                'calculate_position_size', 'kelly_criterion',
                'optimal_f', 'fixed_fractional', 'fixed_ratio',
                'max_drawdown_limit'
            ],
            'risk_metrics': [
                'value_at_risk', 'expected_shortfall',
                'sharpe_ratio', 'sortino_ratio', 'calmar_ratio',
                'max_drawdown', 'risk_of_ruin'
            ],
            'portfolio': [
                'portfolio_var', 'correlation_risk',
                'beta_exposure', 'sector_exposure',
                'position_correlation'
            ],
            'limits': [
                'max_position_size', 'max_portfolio_risk',
                'max_correlation', 'max_leverage',
                'max_concentration'
            ]
        }   

        self.system = {
            'execution': [
                'place_order', 'modify_order', 'cancel_order',
                'get_positions', 'get_orders', 'get_fills'
            ],
            'monitoring': [
                'track_performance', 'monitor_risk_limits',
                'alert_conditions', 'system_health'
            ],
            'integration': [
                'connect_broker', 'connect_data_feed',
                'sync_positions', 'handle_websocket'
            ],
            'logging': [
                'log_trade', 'log_error', 'log_performance',
                'export_results', 'system_diagnostics'
            ]
        }

        # Data Integration and APIs
        self.integration = {
            'external_data': [
                'data_binance', 'data_coinbase', 'data_kraken', 'data_bitfinex',
                'data_bitmex', 'data_deribit', 'data_ftx', 'data_bybit'
            ],
            'api_interfaces': [
                'rest_api', 'websocket_api', 'fix_api', 'ccxt_api',
                'broker_api', 'exchange_api', 'data_api', 'trading_api'
            ]
        }

    def get_all_syntax(self) -> Dict:
        """Returns complete syntax dictionary including all categories"""
        return {
            'market_data': self.market_data,
            'technical': self.technical,
            'candlestick_patterns': self.candlestick_patterns,
            'strategy': self.strategy,
            'symbol_info': self.symbol_info,
            'chart': self.chart,
            'time': self.time,
            'arrays': self.arrays,
            'matrix': self.matrix,
            'math': self.math,
            'ml': self.ml,
            'risk': self.risk,
            'system': self.system,
            'formations': self.formations,
            'microstructure': self.microstructure,
            'intermarket': self.intermarket,
            'automation': self.automation,
            'integration': self.integration,
            'plot': self.plot
        }

    def get_flat_syntax_list(self) -> List[str]:
        """Returns flattened list of all syntax elements"""
        flat_list = []
        for category in self.get_all_syntax().values():
            if isinstance(category, dict):
                for subcategory in category.values():
                    flat_list.extend(subcategory)
            else:
                flat_list.extend(category)
        return list(set(flat_list))  # Remove duplicates

    def is_valid_syntax(self, syntax: str) -> bool:
        """Validates if a syntax element exists"""
        return syntax in self.get_flat_syntax_list()

    def get_category_for_syntax(self, syntax: str) -> str:
        """Returns the category a syntax element belongs to"""
        for category, content in self.get_all_syntax().items():
            if isinstance(content, dict):
                for subcategory, elements in content.items():
                    if syntax in elements:
                        return f"{category}.{subcategory}"
            elif syntax in content:
                return category
        return "unknown"
