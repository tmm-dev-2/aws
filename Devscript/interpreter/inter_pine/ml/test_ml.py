import unittest
import numpy as np
import pandas as pd
from engine import MLEngine
import talib


class TestMLStrategy(unittest.TestCase):
    def setUp(self):
        # Create synthetic market data
        np.random.seed(42)
        dates = pd.date_range(start='2020-01-01', end='2023-12-31', freq='D')
        n_points = len(dates)
        
        # Generate price series with trend and noise
        trend = np.linspace(100, 200, n_points)
        noise = np.random.normal(0, 5, n_points)
        prices = trend + noise
        
        self.market_data = pd.DataFrame({
            'date': dates,
            'open': prices,
            'high': prices + np.random.uniform(0, 2, n_points),
            'low': prices - np.random.uniform(0, 2, n_points),
            'close': prices + np.random.normal(0, 1, n_points),
            'volume': np.random.uniform(1000000, 5000000, n_points)
        })
        
        self.ml_engine = MLEngine()

    def test_ema_strategy(self):
        # Define custom EMA crossover feature
        def ema_cross_feature(data, fast_period=12, slow_period=26):
            fast_ema = talib.EMA(data['close'], timeperiod=fast_period)
            slow_ema = talib.EMA(data['close'], timeperiod=slow_period)
            return fast_ema - slow_ema
        
        # Add feature and create feature set
        self.ml_engine.add_feature('ema_cross', ema_cross_feature)
        self.ml_engine.create_feature_set('ema_ml_strategy', [
            'ema_cross',
            'rsi',
            'macd',
            'volume_ma',
            'volatility'
        ])
        
        # Calculate features
        features = self.ml_engine.calculate_features(self.market_data, 'ema_ml_strategy')
        
        # Prepare training data (predict next day's return)
        X = features[:-1].values
        returns = self.market_data['close'].pct_change()
        y = (returns.shift(-1) > 0)[:-1].values  # Binary labels for positive/negative returns
        
        # Train and evaluate model
        results = self.ml_engine.train_model(
            model_id='ema_ml_test',
            model_type='direction_prediction',
            algorithm='random_forest',
            X=X,
            y=y,
            validation_split=0.2
        )
        
        # Get model evaluation metrics
        metrics = self.ml_engine.evaluate_model('ema_ml_test', X, y)
        
        # Test predictions
        latest_features = features.iloc[-10:].values
        predictions = self.ml_engine.predict('ema_ml_test', latest_features)
        
        # Assertions
        self.assertTrue('train_score' in results)
        self.assertTrue('validation_score' in results)
        self.assertTrue('accuracy' in metrics)
        self.assertTrue(len(predictions) == 10)
        
        print("\nStrategy Test Results:")
        print(f"Training Score: {results['train_score']:.4f}")
        print(f"Validation Score: {results['validation_score']:.4f}")
        print(f"Accuracy: {metrics['accuracy']:.4f}")
        print(f"Precision: {metrics['precision']:.4f}")
        print(f"Recent Predictions: {predictions}")
        
        # Get feature importance
        importance = self.ml_engine.feature_importance('ema_ml_test', 
                                                     ['ema_cross', 'rsi', 'macd', 'volume_ma', 'volatility'])
        print("\nFeature Importance:")
        for feature, score in importance.items():
            print(f"{feature}: {score:.4f}")

def run_ml_tests():
    print("Starting ML Strategy Tests...")
    unittest.main(argv=[''], verbosity=2, exit=False)

if __name__ == "__main__":
    run_ml_tests()
