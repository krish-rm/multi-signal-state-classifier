"""
Tests for data loading and preprocessing.
"""

import pytest
import numpy as np
import pandas as pd
from src.data import SignalDataGenerator, load_or_generate_data
from src.data.feature_engineering import FeaturePipeline


class TestDataGenerator:
    """Test data generation."""
    
    def test_generate_trading_signals(self):
        """Test trading signal generation."""
        gen = SignalDataGenerator(seed=42)
        df, labels = gen.generate_trading_signals(n_samples=100)
        
        assert len(df) == 100
        assert len(labels) == 100
        assert set(labels).issubset(gen.STATES)
        assert 'price_change' in df.columns
        assert 'volatility' in df.columns
    
    def test_generate_plant_health_signals(self):
        """Test plant health signal generation."""
        gen = SignalDataGenerator(seed=42)
        df, labels = gen.generate_plant_health_signals(n_samples=100)
        
        assert len(df) == 100
        assert len(labels) == 100
        assert 'soil_moisture' in df.columns
        assert 'temperature' in df.columns
    
    def test_create_unified_dataset(self):
        """Test unified dataset creation."""
        gen = SignalDataGenerator(seed=42)
        df, labels = gen.create_unified_dataset(n_samples=100)
        
        assert len(df) == 100
        assert len(labels) == 100
        assert 'timestamp' in df.columns
        assert 'price_change' in df.columns
        assert 'soil_moisture' in df.columns
    
    def test_state_distribution(self):
        """Test state distribution."""
        gen = SignalDataGenerator(seed=42)
        distribution = {
            'calm': 50,
            'alert': 30,
            'risk': 20
        }
        df, labels = gen.generate_trading_signals(
            n_samples=100,
            state_distribution=distribution
        )
        
        unique, counts = np.unique(labels, return_counts=True)
        assert dict(zip(unique, counts))['calm'] == 50


class TestFeaturePipeline:
    """Test feature engineering pipeline."""
    
    def test_feature_pipeline_creation(self):
        """Test feature pipeline creation."""
        pipeline = FeaturePipeline()
        assert pipeline is not None
    
    def test_fit_transform(self):
        """Test fit and transform."""
        gen = SignalDataGenerator(seed=42)
        df, labels = gen.create_unified_dataset(n_samples=100)
        
        pipeline = FeaturePipeline()
        X, feature_names = pipeline.fit_transform(df)
        
        assert X.shape[0] == 100
        assert len(feature_names) > 0
        assert len(feature_names) == X.shape[1]
    
    def test_no_nan_values(self):
        """Test that pipeline doesn't produce NaN values."""
        gen = SignalDataGenerator(seed=42)
        df, labels = gen.create_unified_dataset(n_samples=100)
        
        pipeline = FeaturePipeline()
        X, _ = pipeline.fit_transform(df)
        
        # Convert DataFrame to numpy array for NaN check
        X_values = X.values if hasattr(X, 'values') else X
        assert not np.isnan(X_values).any()
        assert not np.isinf(X_values).any()


@pytest.mark.integration
class TestDataLoading:
    """Integration tests for data loading."""
    
    def test_load_or_generate_data(self):
        """Test data loading or generation."""
        df, labels = load_or_generate_data(
            output_path="data/test/test_signals.parquet",
            n_samples=100,
            force_generate=True
        )
        
        assert len(df) == 100
        assert len(labels) == 100


if __name__ == "__main__":
    pytest.main([__file__, "-v"])


