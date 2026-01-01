"""
Tests for API endpoints.
"""

import pytest
import json
import os
from fastapi.testclient import TestClient
from src.api.predict_api import app, initialize_models

# Create test client
client = TestClient(app)

# Initialize models before tests if model exists
# Note: TestClient should trigger startup events, but we also initialize manually
# to ensure models are loaded for tests
@pytest.fixture(scope="session", autouse=True)
def setup_models():
    """Initialize models before running API tests."""
    # Only initialize if model file exists
    model_path = os.getenv('MODEL_PATH', 'models/ensemble_model.pkl')
    pipeline_path = os.getenv('PIPELINE_PATH', 'models/feature_pipeline.pkl')
    
    if os.path.exists(model_path) and os.path.exists(pipeline_path):
        try:
            # Initialize models manually (TestClient should also trigger startup event)
            initialize_models()
        except Exception as e:
            print(f"Warning: Could not initialize models for tests: {e}")
            print("Some API tests may fail. Run 'python train.py' first to generate models.")
    else:
        print(f"Warning: Model files not found at {model_path} or {pipeline_path}")
        print("Run 'python train.py' first to generate models for API tests.")


class TestAPIHealthCheck:
    """Test health check endpoints."""
    
    def test_health_check(self):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert 'status' in data
        assert data['status'] == 'healthy'
    
    def test_metrics_endpoint(self):
        """Test metrics endpoint."""
        response = client.get("/metrics")
        assert response.status_code == 200
        data = response.json()
        assert 'total_predictions' in data
        assert 'average_latency_ms' in data


class TestAPIPrediction:
    """Test prediction endpoints."""
    
    @pytest.fixture
    def sample_request(self):
        """Create sample prediction request."""
        return {
            "timestamp": "2025-01-15T10:30:00Z",
            "signals": {
                "trading": {
                    "price_change": 0.02,
                    "volatility": 0.15,
                    "volume": 1000000,
                    "rsi": 65.5
                },
                "plant_health": {
                    "soil_moisture": 0.65,
                    "temperature": 22.5,
                    "stress_score": 0.3
                }
            }
        }
    
    def test_predict_endpoint_structure(self, sample_request):
        """Test predict endpoint returns correct structure."""
        # Check if model is loaded
        health_response = client.get("/health")
        if health_response.status_code == 200:
            health_data = health_response.json()
            if not health_data.get('model_loaded', False):
                pytest.skip("Model not loaded. Run 'python train.py' first.")
        
        response = client.post("/predict", json=sample_request)
        assert response.status_code == 200
        data = response.json()
        
        assert 'state' in data
        assert 'confidence' in data
        assert 'probabilities' in data
        assert 'lighting_control' in data
        assert 'inference_time_ms' in data
    
    def test_predict_endpoint_values(self, sample_request):
        """Test predict endpoint values are valid."""
        # Check if model is loaded
        health_response = client.get("/health")
        if health_response.status_code == 200:
            health_data = health_response.json()
            if not health_data.get('model_loaded', False):
                pytest.skip("Model not loaded. Run 'python train.py' first.")
        
        response = client.post("/predict", json=sample_request)
        assert response.status_code == 200
        data = response.json()
        
        # Check state is valid
        valid_states = ['calm', 'alert', 'risk', 'flow', 'deviation']
        assert data['state'] in valid_states
        
        # Check confidence is valid
        assert 0.0 <= data['confidence'] <= 1.0
        
        # Check probabilities sum to ~1
        prob_sum = sum(data['probabilities'].values())
        assert 0.9 <= prob_sum <= 1.1
    
    def test_batch_prediction(self, sample_request):
        """Test batch prediction endpoint."""
        requests = [sample_request] * 3
        response = client.post("/predict/batch", json=requests)
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3


class TestAPIInfo:
    """Test info endpoints."""
    
    def test_info_endpoint(self):
        """Test info endpoint."""
        response = client.get("/info")
        assert response.status_code == 200
        data = response.json()
        assert 'name' in data
        assert 'version' in data
        assert 'endpoints' in data
    
    def test_lighting_info_endpoint(self):
        """Test lighting info endpoint."""
        for state in ['calm', 'alert', 'risk', 'flow', 'deviation']:
            response = client.get(f"/lighting-info/{state}")
            assert response.status_code == 200
            data = response.json()
            assert 'lighting_config' in data
            assert 'description' in data
    
    def test_invalid_state(self):
        """Test invalid state in lighting info."""
        response = client.get("/lighting-info/invalid_state")
        assert response.status_code == 400


class TestAPIValidation:
    """Test input validation."""
    
    def test_missing_fields(self):
        """Test request validation with missing fields."""
        invalid_request = {
            "signals": {
                "trading": {
                    "price_change": 0.02
                    # Missing other fields
                }
            }
        }
        response = client.post("/predict", json=invalid_request)
        assert response.status_code in [400, 422]  # Validation error


if __name__ == "__main__":
    pytest.main([__file__, "-v"])


