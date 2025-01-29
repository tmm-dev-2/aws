import numpy as np
import pandas as pd
import requests
from typing import Dict, List, Any, Tuple, Optional
from scipy.stats import norm, linregress, pearsonr, kurtosis, skew
from scipy.signal import savgol_filter
from scipy.optimize import minimize
# Removed KernelReg import
from sklearn.preprocessing import StandardScaler

class KernelRegressionStrategy:
    def __init__(self):
        # Core Strategy Parameters
        self.lookback = 20  # Lookback period for regression
        self.bandwidth = 0.5  # Kernel bandwidth parameter
        self.kernel_type = 'gaussian'  # Type of kernel to use
        self.std_dev_multiplier = 2.0  # Standard deviation multiplier for bands
        
        # Technical Parameters
        self.momentum_period = 14  # Period for momentum calculations
        self.volatility_window = 20  # Window for volatility calculations
        self.trend_threshold = 0.02  # Threshold for trend determination
        self.smooth_window = 5  # Window for smoothing operations
        self.signal_threshold = 1.5  # Threshold for signal generation
        self.rsi_period = 14  # RSI period
        self.bollinger_period = 20  # Bollinger Bands period
        self.atr_period = 14  # Average True Range period
        
        # Advanced Parameters
        self.min_confidence = 0.7  # Minimum confidence for signal generation
        self.volume_factor = 1.5  # Volume significance factor
        self.noise_threshold = 0.1  # Noise filtering threshold
        self.trend_strength_threshold = 0.3  # Minimum trend strength
        self.mean_reversion_factor = 0.5  # Mean reversion strength

    def calculate_statistical_features(self, prices: np.ndarray, window: int = 20) -> Dict[str, np.ndarray]:
        """
        Calculate advanced statistical features
        
        Args:
            prices: Price series
            window: Rolling window size
            
        Returns:
            Dict containing statistical features
        """
        returns = np.log(prices[1:] / prices[:-1])
        returns = np.pad(returns, (1, 0), mode='edge')
        
        # Rolling statistics
        roll_mean = pd.Series(returns).rolling(window=window).mean().values
        roll_std = pd.Series(returns).rolling(window=window).std().values
        roll_skew = pd.Series(returns).rolling(window=window).skew().values
        roll_kurt = pd.Series(returns).rolling(window=window).apply(kurtosis).values
        
        # Normalize features
        scaler = StandardScaler()
        normalized_features = scaler.fit_transform(np.column_stack([
            roll_mean, roll_std, roll_skew, roll_kurt
        ]))
        
        return {
            'mean': normalized_features[:, 0],
            'std': normalized_features[:, 1],
            'skew': normalized_features[:, 2],
            'kurtosis': normalized_features[:, 3]
        }

    def calculate_technical_indicators(self, prices: np.ndarray, volumes: np.ndarray) -> Dict[str, np.ndarray]:
        """
        Calculate technical indicators
        
        Args:
            prices: Price series
            volumes: Volume series
            
        Returns:
            Dict containing technical indicators
        """
        # RSI calculation
        delta = np.diff(prices)
        delta = np.pad(delta, (1, 0), mode='edge')
        gains = np.where(delta > 0, delta, 0)
        losses = np.where(delta < 0, -delta, 0)
        
        avg_gains = pd.Series(gains).rolling(window=self.rsi_period).mean().values
        avg_losses = pd.Series(losses).rolling(window=self.rsi_period).mean().values
        rs = avg_gains / np.where(avg_losses == 0, 1e-10, avg_losses)
        rsi = 100 - (100 / (1 + rs))
        
        # Volume-weighted momentum
        momentum = np.zeros_like(prices)
        vol_weighted_price = prices * volumes
        for i in range(self.momentum_period, len(prices)):
            momentum[i] = (vol_weighted_price[i] - vol_weighted_price[i - self.momentum_period]) / \
                         vol_weighted_price[i - self.momentum_period]
        
        # Bollinger Bands
        sma = pd.Series(prices).rolling(window=self.bollinger_period).mean().values
        std = pd.Series(prices).rolling(window=self.bollinger_period).std().values
        upper_band = sma + (2 * std)
        lower_band = sma - (2 * std)
        
        # Average True Range
        high = prices + std
        low = prices - std
        tr = np.maximum(
            high - low,
            np.abs(high - np.roll(prices, 1)),
            np.abs(low - np.roll(prices, 1))
        )
        atr = pd.Series(tr).rolling(window=self.atr_period).mean().values
        
        return {
            'rsi': rsi,
            'momentum': momentum,
            'bollinger': {
                'upper': upper_band,
                'lower': lower_band,
                'middle': sma
            },
            'atr': atr
        }

    def calculate_market_regime(self, prices: np.ndarray, window: int = 50) -> Dict[str, np.ndarray]:
        """
        Determine market regime and characteristics
        
        Args:
            prices: Price series
            window: Analysis window
            
        Returns:
            Dict containing market regime indicators
        """
        # Trend strength using linear regression
        trend_strength = np.zeros(len(prices))
        r_squared = np.zeros(len(prices))
        
        for i in range(window, len(prices)):
            x = np.arange(window)
            y = prices[i-window:i]
            slope, _, r_value, _, _ = linregress(x, y)
            trend_strength[i] = slope
            r_squared[i] = r_value ** 2
        
        # Volatility regime
        returns = np.log(prices[1:] / prices[:-1])
        returns = np.pad(returns, (1, 0), mode='edge')
        volatility = pd.Series(returns).rolling(window=window).std().values
        
        # Market efficiency ratio
        price_path = np.sum(np.abs(np.diff(prices)))
        price_path = np.pad(price_path, (1, 0), mode='edge')
        direct_path = np.abs(prices - np.roll(prices, window))
        efficiency_ratio = direct_path / np.where(price_path == 0, 1e-10, price_path)
        
        return {
            'trend_strength': trend_strength,
            'r_squared': r_squared,
            'volatility_regime': volatility,
            'efficiency_ratio': efficiency_ratio
        }

    def generate_signals(self, 
                        prices: np.ndarray,
                        regression: np.ndarray,
                        confidence: np.ndarray,
                        stats: Dict[str, np.ndarray],
                        technicals: Dict[str, np.ndarray],
                        regime: Dict[str, np.ndarray]) -> np.ndarray:
        """
        Generate trading signals based on multiple factors
        
        Args:
            prices: Price series
            regression: Kernel regression values
            confidence: Regression confidence
            stats: Statistical features
            technicals: Technical indicators
            regime: Market regime indicators
            
        Returns:
            numpy array of signals (-1, 0, 1)
        """
        signals = np.zeros(len(prices))
        
        for i in range(1, len(prices)):
            # Price deviation from regression
            deviation = (prices[i] - regression[i]) / regression[i]
            
            # Trend conditions
            trend_aligned = (
                regime['trend_strength'][i] > self.trend_strength_threshold and
                regime['r_squared'][i] > self.min_confidence
            )
            
            # Technical conditions
            tech_signal = (
                technicals['rsi'][i] > 70 or technicals['rsi'][i] < 30 and
                abs(technicals['momentum'][i]) > self.trend_threshold
            )
            
            # Statistical conditions
            stat_signal = (
                abs(stats['skew'][i]) > 1.0 and
                stats['kurtosis'][i] > 3.0
            )
            
            # Volume and volatility filters
            volatility_filter = regime['volatility_regime'][i] < np.percentile(
                regime['volatility_regime'], 75
            )
            
            # Generate signals
            if (deviation > self.signal_threshold and
                trend_aligned and
                tech_signal and
                stat_signal and
                volatility_filter and
                confidence[i] > self.min_confidence):
                signals[i] = -1  # Sell signal
            elif (deviation < -self.signal_threshold and
                  trend_aligned and
                  tech_signal and
                  stat_signal and
                  volatility_filter and
                  confidence[i] > self.min_confidence):
                signals[i] = 1  # Buy signal
        
        return signals

    def calculate_strategy(self, data: Dict[str, List[float]]) -> Dict[str, Any]:
        """
        Enhanced main calculation function with comprehensive analytics
        """
        # Convert to numpy arrays
        closes = np.array(data['close'])
        highs = np.array(data['high'])
        lows = np.array(data['low'])
        volumes = np.array(data['volume'])
        times = np.array(data['time'])
        
        # Calculate kernel regression and bands
        regression, upper_band, lower_band, confidence = self.calculate_kernel_regression(closes, times)
        
        # Calculate additional features
        stats = self.calculate_statistical_features(closes)
        technicals = self.calculate_technical_indicators(closes, volumes)
        regime = self.calculate_market_regime(closes)
        
        # Generate signals
        signals = self.generate_signals(
            closes, regression, confidence, stats, technicals, regime
        )
        
        return {
            'regression': regression.tolist(),
            'upper_band': upper_band.tolist(),
            'lower_band': lower_band.tolist(),
            'confidence': confidence.tolist(),
            'signals': signals.tolist(),
            'statistics': {
                'mean': stats['mean'].tolist(),
                'std': stats['std'].tolist(),
                'skew': stats['skew'].tolist(),
                'kurtosis': stats['kurtosis'].tolist()
            },
            'technicals': {
                'rsi': technicals['rsi'].tolist(),
                'momentum': technicals['momentum'].tolist(),
                'bollinger_bands': {
                    'upper': technicals['bollinger']['upper'].tolist(),
                    'lower': technicals['bollinger']['lower'].tolist(),
                    'middle': technicals['bollinger']['middle'].tolist()
                },
                'atr': technicals['atr'].tolist()
            },
            'market_regime': {
                'trend_strength': regime['trend_strength'].tolist(),
                'r_squared': regime['r_squared'].tolist(),
                'volatility': regime['volatility_regime'].tolist(),
                'efficiency': regime['efficiency_ratio'].tolist()
            },
            'timestamps': times.tolist(),
            'metadata': {
                'signal_count': int(np.sum(np.abs(signals))),
                'average_confidence': float(np.mean(confidence)),
                'trend_quality': float(np.mean(regime['r_squared']))
            },
            'visualization': {
                'colors': {
                    'regression': '#2196F3',
                    'upper_band': '#4CAF50',
                    'lower_band': '#F44336',
                    'signal_buy': '#00FF00',
                    'signal_sell': '#FF0000',
                    'neutral': '#9E9E9E'
                }
            }
        }