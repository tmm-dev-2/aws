from typing import Dict, Any, List, Optional, Callable, Union
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
from sklearn.model_selection import train_test_split, cross_val_score, TimeSeriesSplit
from sklearn.linear_model import LinearRegression, LogisticRegression, Ridge, Lasso
from sklearn.ensemble import (
    RandomForestRegressor, RandomForestClassifier,
    GradientBoostingRegressor, GradientBoostingClassifier,
    IsolationForest, AdaBoostRegressor, AdaBoostClassifier
)
from sklearn.svm import SVR, SVC
from sklearn.neural_network import MLPRegressor, MLPClassifier
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from sklearn.metrics import (
    precision_score, recall_score, confusion_matrix, 
    roc_curve, auc, mean_squared_error, r2_score,
    accuracy_score, f1_score
)
import talib

class MLEngine:
    def __init__(self):
        self.models: Dict[str, Any] = {}
        self.scalers: Dict[str, Any] = {}
        self.features: Dict[str, Callable] = {}
        self.feature_sets: Dict[str, List[str]] = {}
        self.predictions: Dict[str, np.ndarray] = {}
        
        # Available algorithms by type
        self.algorithms = {
            'direction_prediction': {
                'random_forest': RandomForestClassifier,
                'gradient_boost': GradientBoostingClassifier,
                'svm': SVC,
                'neural_network': MLPClassifier,
                'logistic': LogisticRegression,
                'adaboost': AdaBoostClassifier
            },
            'price_prediction': {
                'random_forest': RandomForestRegressor,
                'gradient_boost': GradientBoostingRegressor,
                'svm': SVR,
                'neural_network': MLPRegressor,
                'linear': LinearRegression,
                'ridge': Ridge,
                'lasso': Lasso,
                'adaboost': AdaBoostRegressor
            },
            'anomaly_detection': {
                'isolation_forest': IsolationForest,
                'dbscan': DBSCAN
            },
            'clustering': {
                'kmeans': KMeans,
                'hierarchical': AgglomerativeClustering
            }
        }
        
        # Initialize default feature functions
        self._init_default_features()

    def _init_default_features(self):
        """Initialize default technical analysis features"""
        self.features.update({
            # Trend Indicators
            'sma': lambda data, period=20: talib.SMA(data['close'], timeperiod=period),
            'ema': lambda data, period=20: talib.EMA(data['close'], timeperiod=period),
            'macd': lambda data: talib.MACD(data['close'])[0],
            'adx': lambda data: talib.ADX(data['high'], data['low'], data['close']),
            
            # Momentum Indicators
            'rsi': lambda data: talib.RSI(data['close']),
            'stoch': lambda data: talib.STOCH(data['high'], data['low'], data['close'])[0],
            'cci': lambda data: talib.CCI(data['high'], data['low'], data['close']),
            'mfi': lambda data: talib.MFI(data['high'], data['low'], data['close'], data['volume']),
            
            # Volatility Indicators
            'bbands': lambda data: talib.BBANDS(data['close']),
            'atr': lambda data: talib.ATR(data['high'], data['low'], data['close']),
            
            # Volume Indicators
            'obv': lambda data: talib.OBV(data['close'], data['volume']),
            'ad': lambda data: talib.AD(data['high'], data['low'], data['close'], data['volume']),
            
            # Price Transforms
            'returns': lambda data: data['close'].pct_change(),
            'log_returns': lambda data: np.log(data['close']/data['close'].shift(1)),
            
            # Custom Features
            'volatility': lambda data, period=20: data['close'].pct_change().rolling(period).std(),
            'volume_ma': lambda data, period=20: data['volume'].rolling(period).mean(),
            'price_range': lambda data: (data['high'] - data['low']) / data['close'],
            'gap': lambda data: (data['open'] - data['close'].shift(1)) / data['close'].shift(1)
        })

    def add_feature(self, name: str, feature_func: Callable) -> None:
        """Add a custom feature calculation function"""
        self.features[name] = feature_func

    def create_feature_set(self, set_name: str, feature_names: List[str]) -> None:
        """Create a named set of features for use in models"""
        self.feature_sets[set_name] = feature_names

    def calculate_features(self, data: pd.DataFrame, feature_set: str) -> pd.DataFrame:
        """Calculate features for a given feature set"""
        if feature_set not in self.feature_sets:
            raise ValueError(f"Feature set {feature_set} not found")
            
        features = pd.DataFrame()
        for feature_name in self.feature_sets[feature_set]:
            if feature_name in self.features:
                feature_value = self.features[feature_name](data)
                if isinstance(feature_value, tuple):
                    for i, val in enumerate(feature_value):
                        features[f"{feature_name}_{i}"] = val
                else:
                    features[feature_name] = feature_value
                    
        return features.fillna(method='ffill')

    def train_model(self, 
                   model_id: str, 
                   model_type: str,
                   algorithm: str, 
                   X: np.ndarray, 
                   y: np.ndarray, 
                   params: Dict = None,
                   validation_split: float = 0.2) -> Dict[str, Any]:
        """Train a model with specified algorithm and parameters"""
        if model_type not in self.algorithms or algorithm not in self.algorithms[model_type]:
            raise ValueError(f"Invalid model type or algorithm")
            
        # Split data
        X_train, X_val, y_train, y_val = train_test_split(
            X, y, test_size=validation_split, shuffle=False
        )
        
        # Create and train model
        model_class = self.algorithms[model_type][algorithm]
        model = model_class(**(params or {}))
        model.fit(X_train, y_train)
        
        # Store model
        self.models[model_id] = {
            'model': model,
            'type': model_type,
            'algorithm': algorithm,
            'params': params
        }
        
        # Calculate metrics
        train_score = model.score(X_train, y_train)
        val_score = model.score(X_val, y_val)
        
        return {
            'train_score': train_score,
            'validation_score': val_score,
            'model_id': model_id
        }

    def predict(self, model_id: str, X: np.ndarray) -> np.ndarray:
        """Generate predictions using a trained model"""
        if model_id not in self.models:
            raise ValueError(f"Model {model_id} not found")
            
        model = self.models[model_id]['model']
        predictions = model.predict(X)
        self.predictions[model_id] = predictions
        return predictions

    def evaluate_model(self, 
                      model_id: str, 
                      X: np.ndarray, 
                      y: np.ndarray) -> Dict[str, Any]:
        """Evaluate model performance with multiple metrics"""
        if model_id not in self.models:
            raise ValueError(f"Model {model_id} not found")
            
        model = self.models[model_id]['model']
        model_type = self.models[model_id]['type']
        predictions = model.predict(X)
        
        metrics = {}
        if model_type in ['direction_prediction']:
            metrics.update({
                'accuracy': accuracy_score(y, predictions),
                'precision': precision_score(y, predictions, average='weighted'),
                'recall': recall_score(y, predictions, average='weighted'),
                'f1': f1_score(y, predictions, average='weighted'),
                'confusion_matrix': confusion_matrix(y, predictions).tolist()
            })
        elif model_type in ['price_prediction']:
            metrics.update({
                'mse': mean_squared_error(y, predictions),
                'rmse': np.sqrt(mean_squared_error(y, predictions)),
                'r2': r2_score(y, predictions)
            })
            
        return metrics

    def optimize_hyperparameters(self, 
                               model_type: str,
                               algorithm: str, 
                               X: np.ndarray, 
                               y: np.ndarray, 
                               param_grid: Dict,
                               cv: int = 5) -> Dict[str, Any]:
        """Optimize model hyperparameters using grid search"""
        from sklearn.model_selection import GridSearchCV
        
        if model_type not in self.algorithms or algorithm not in self.algorithms[model_type]:
            raise ValueError(f"Invalid model type or algorithm")
            
        model_class = self.algorithms[model_type][algorithm]
        cv = TimeSeriesSplit(n_splits=cv)
        
        grid_search = GridSearchCV(
            model_class(), 
            param_grid, 
            cv=cv,
            scoring='neg_mean_squared_error' if model_type == 'price_prediction' else 'accuracy',
            n_jobs=-1
        )
        
        grid_search.fit(X, y)
        
        return {
            'best_params': grid_search.best_params_,
            'best_score': grid_search.best_score_,
            'cv_results': grid_search.cv_results_
        }

    def feature_importance(self, model_id: str, feature_names: List[str]) -> Dict[str, float]:
        """Get feature importance scores for supported models"""
        if model_id not in self.models:
            raise ValueError(f"Model {model_id} not found")
            
        model = self.models[model_id]['model']
        
        if hasattr(model, 'feature_importances_'):
            importances = model.feature_importances_
            return dict(zip(feature_names, importances))
        elif hasattr(model, 'coef_'):
            importances = np.abs(model.coef_)
            return dict(zip(feature_names, importances))
            
        return {}

    def save_model(self, model_id: str, filepath: str) -> bool:
        """Save model to file"""
        import joblib
        if model_id in self.models:
            joblib.dump(self.models[model_id], filepath)
            return True
        return False

    def load_model(self, model_id: str, filepath: str) -> bool:
        """Load model from file"""
        import joblib
        try:
            self.models[model_id] = joblib.load(filepath)
            return True
        except:
            return False
