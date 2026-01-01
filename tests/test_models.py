"""
Tests for model training and prediction.
"""

import pytest
import numpy as np
from src.data import SignalDataGenerator
from src.data.feature_engineering import FeaturePipeline
from src.models import (
    BaselineModels, EnsembleClassifier, split_data_time_series, evaluate_model
)


class TestBaselineModels:
    """Test baseline model training."""
    
    @pytest.fixture
    def sample_data(self):
        """Create sample training data."""
        gen = SignalDataGenerator(seed=42)
        df, labels = gen.create_unified_dataset(n_samples=200)
        pipeline = FeaturePipeline()
        X, _ = pipeline.fit_transform(df)
        return X, labels
    
    def test_random_forest_training(self, sample_data):
        """Test Random Forest model training."""
        X, y = sample_data
        model = BaselineModels.train_random_forest(X, y)
        
        assert model is not None
        preds = model.predict(X)
        assert len(preds) == len(y)
    
    def test_xgboost_training(self, sample_data):
        """Test XGBoost model training."""
        try:
            X, y = sample_data
            model = BaselineModels.train_xgboost(X, y)
            assert model is not None
        except ImportError:
            pytest.skip("XGBoost not installed")
    
    def test_lightgbm_training(self, sample_data):
        """Test LightGBM model training."""
        try:
            X, y = sample_data
            model = BaselineModels.train_lightgbm(X, y)
            assert model is not None
        except ImportError:
            pytest.skip("LightGBM not installed")


class TestEnsembleClassifier:
    """Test ensemble classifier."""
    
    @pytest.fixture
    def sample_data(self):
        """Create sample training data."""
        gen = SignalDataGenerator(seed=42)
        df, labels = gen.create_unified_dataset(n_samples=200)
        pipeline = FeaturePipeline()
        X, _ = pipeline.fit_transform(df)
        return X, labels
    
    def test_ensemble_initialization(self):
        """Test ensemble initialization."""
        ensemble = EnsembleClassifier()
        assert ensemble is not None
        assert len(ensemble.weights) > 0
    
    def test_ensemble_training(self, sample_data):
        """Test ensemble training."""
        X, y = sample_data
        ensemble = EnsembleClassifier()
        ensemble.train(X[:160], y[:160], X[160:], y[160:])
        
        assert len(ensemble.models) > 0
    
    def test_ensemble_prediction(self, sample_data):
        """Test ensemble prediction."""
        X, y = sample_data
        
        # Split and train
        train_test_split = int(0.8 * len(X))
        X_train, X_test = X[:train_test_split], X[train_test_split:]
        y_train, y_test = y[:train_test_split], y[train_test_split:]
        
        # Create and train
        ensemble = EnsembleClassifier()
        ensemble.train(X_train, y_train)
        
        # Predict
        preds = ensemble.predict(X_test)
        assert len(preds) == len(y_test)
    
    def test_ensemble_predict_proba(self, sample_data):
        """Test ensemble probability prediction."""
        X, y = sample_data
        
        train_test_split = int(0.8 * len(X))
        X_train, X_test = X[:train_test_split], X[train_test_split:]
        y_train = y[:train_test_split]
        
        ensemble = EnsembleClassifier()
        ensemble.train(X_train, y_train)
        
        preds, probas = ensemble.predict(X_test, return_proba=True)
        assert len(preds) == len(X_test)
        assert probas.shape[0] == len(X_test)


class TestDataSplitting:
    """Test data splitting."""
    
    def test_time_series_split(self):
        """Test time-series aware data splitting."""
        X = np.random.randn(100, 10)
        y = np.array(['calm'] * 50 + ['alert'] * 30 + ['risk'] * 20)
        
        (X_train, y_train), (X_val, y_val), (X_test, y_test) = split_data_time_series(
            X, y, train_ratio=0.7, val_ratio=0.15, test_ratio=0.15
        )
        
        assert len(X_train) == 70
        assert len(X_val) == 15
        assert len(X_test) == 15
        assert len(y_train) + len(y_val) + len(y_test) == 100


class TestModelEvaluation:
    """Test model evaluation."""
    
    @pytest.fixture
    def trained_model(self):
        """Create and train a model."""
        gen = SignalDataGenerator(seed=42)
        df, labels = gen.create_unified_dataset(n_samples=200)
        pipeline = FeaturePipeline()
        X, _ = pipeline.fit_transform(df)
        
        ensemble = EnsembleClassifier()
        ensemble.train(X[:150], labels[:150], X[150:], labels[150:])
        
        return ensemble, X[150:], labels[150:]
    
    def test_evaluate_model(self, trained_model):
        """Test model evaluation."""
        model, X_test, y_test = trained_model
        metrics = evaluate_model(model, X_test, y_test)
        
        assert 'accuracy' in metrics
        assert 'f1_macro' in metrics
        assert 'f1_weighted' in metrics
        assert metrics['accuracy'] >= 0.0
        assert metrics['accuracy'] <= 1.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])


