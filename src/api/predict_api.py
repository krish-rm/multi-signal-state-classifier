"""
FastAPI application for multi-signal state classification.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import logging
import os
import time
import pandas as pd
import numpy as np
from datetime import datetime

from src.models.predict import StateClassifier
from src.data.feature_engineering import FeaturePipeline
from src.api import map_state_to_lighting, describe_lighting_pattern

logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Multi-Signal State Classifier API",
    description="Production-ready ML pipeline for multi-source signal fusion and state classification",
    version="1.0.0"
)

# Add CORS middleware to allow cross-origin requests from the dashboard
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state
classifier = None
feature_pipeline = None
model_stats = {
    'predictions_served': 0,
    'errors': 0,
    'total_latency_ms': 0,
    'start_time': datetime.now()
}


# Pydantic models for request/response
class TradingSignals(BaseModel):
    """Trading market signals."""
    price_change: float
    volatility: float
    volume: float
    rsi: Optional[float] = None


class PlantHealthSignals(BaseModel):
    """Plant health sensor signals."""
    soil_moisture: float
    temperature: float
    stress_score: Optional[float] = None


class SignalInput(BaseModel):
    """Combined signals input."""
    trading: TradingSignals
    plant_health: PlantHealthSignals


class PredictionRequest(BaseModel):
    """Prediction request model."""
    timestamp: Optional[str] = None
    signals: SignalInput
    request_id: Optional[str] = None


class LightingConfig(BaseModel):
    """Lighting control configuration."""
    color_temperature: Any
    brightness: Any
    pattern: str
    description: str
    urgency: str


class PredictionResponse(BaseModel):
    """Prediction response model."""
    state: str
    confidence: float
    probabilities: Dict[str, float]
    lighting_control: LightingConfig
    model_version: str
    inference_time_ms: float
    timestamp: str
    request_id: Optional[str] = None


class HealthCheckResponse(BaseModel):
    """Health check response."""
    status: str
    model_loaded: bool
    predictions_served: int
    uptime_seconds: float
    timestamp: str


class MetricsResponse(BaseModel):
    """Metrics response."""
    total_predictions: int
    total_errors: int
    average_latency_ms: float
    uptime_seconds: float
    timestamp: str


def initialize_models():
    """Initialize classifier and feature pipeline."""
    global classifier, feature_pipeline
    
    try:
        model_path = os.getenv('MODEL_PATH', 'models/ensemble_model.pkl')
        pipeline_path = os.getenv('PIPELINE_PATH', 'models/feature_pipeline.pkl')
        
        # Load feature pipeline if it exists
        if os.path.exists(pipeline_path):
            import pickle
            with open(pipeline_path, 'rb') as f:
                feature_pipeline = pickle.load(f)
            logger.info(f"Feature pipeline loaded from {pipeline_path}")
        else:
            logger.warning(f"Feature pipeline not found at {pipeline_path}. Creating new one.")
            feature_pipeline = FeaturePipeline()
        
        # Try to load model if it exists
        if os.path.exists(model_path):
            classifier = StateClassifier(model_path, feature_pipeline)
            logger.info(f"Model loaded from {model_path}")
        else:
            logger.warning(f"Model not found at {model_path}. Using dummy classifier.")
            classifier = None
            
    except Exception as e:
        logger.error(f"Failed to initialize models: {e}")
        classifier = None
        feature_pipeline = None


@app.on_event("startup")
async def startup_event():
    """Initialize on startup."""
    logger.info("Starting Multi-Signal State Classifier API")
    initialize_models()


@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest) -> PredictionResponse:
    """
    Single prediction endpoint.
    
    Args:
        request: Prediction request with signals
    
    Returns:
        Prediction response with state, confidence, and lighting control
    """
    start_time = time.time()
    
    try:
        if classifier is None:
            raise HTTPException(
                status_code=503,
                detail="Model not loaded. Service unavailable."
            )
        
        if feature_pipeline is None:
            raise HTTPException(
                status_code=503,
                detail="Feature pipeline not loaded. Service unavailable."
            )
        
        # Prepare raw features as DataFrame
        raw_features = pd.DataFrame({
            'price_change': [request.signals.trading.price_change],
            'volatility': [request.signals.trading.volatility],
            'volume': [request.signals.trading.volume],
            'rsi': [request.signals.trading.rsi or 50.0],
            'soil_moisture': [request.signals.plant_health.soil_moisture],
            'temperature': [request.signals.plant_health.temperature],
            'stress_score': [request.signals.plant_health.stress_score or 0.0],
        })
        
        # Transform using feature pipeline
        engineered_features = feature_pipeline.transform(raw_features)
        
        # Fill any NaN values (from rolling stats on single row) with 0
        engineered_features = engineered_features.fillna(0)
        
        # Debug: Log raw plant health values to verify they're being used
        logger.debug(f"Raw plant health values: soil_moisture={request.signals.plant_health.soil_moisture}, "
                    f"temperature={request.signals.plant_health.temperature}, "
                    f"stress_score={request.signals.plant_health.stress_score}")
        
        # Check if plant health features are in the engineered features
        plant_feature_cols = [col for col in engineered_features.columns 
                             if any(p in col for p in ['soil_moisture', 'temperature', 'stress_score'])]
        if plant_feature_cols:
            logger.debug(f"Plant health features found: {len(plant_feature_cols)} features")
            # Log a sample of plant health feature values
            sample_plant_features = {col: engineered_features[col].iloc[0] 
                                   for col in plant_feature_cols[:5]}  # First 5
            logger.debug(f"Sample plant feature values: {sample_plant_features}")
        
        # Convert to numpy array for prediction
        feature_array = engineered_features.values
        
        # Make prediction
        prediction = classifier.predict(feature_array)
        
        # Get lighting control
        lighting_config = map_state_to_lighting(
            prediction['state'],
            prediction['confidence']
        )
        
        # Calculate latency
        latency_ms = (time.time() - start_time) * 1000
        
        # Update stats
        model_stats['predictions_served'] += 1
        model_stats['total_latency_ms'] += latency_ms
        
        response = PredictionResponse(
            state=prediction['state'],
            confidence=prediction['confidence'],
            probabilities=prediction['probabilities'],
            lighting_control=LightingConfig(**lighting_config),
            model_version="1.0.0",
            inference_time_ms=latency_ms,
            timestamp=request.timestamp or datetime.now().isoformat(),
            request_id=request.request_id
        )
        
        return response
        
    except Exception as e:
        model_stats['errors'] += 1
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/predict/batch")
async def predict_batch(requests: List[PredictionRequest]):
    """
    Batch prediction endpoint for multiple samples.
    
    Args:
        requests: List of prediction requests
    
    Returns:
        List of prediction responses
    """
    responses = []
    for request in requests:
        try:
            response = await predict(request)
            responses.append(response)
        except Exception as e:
            logger.error(f"Batch prediction error: {e}")
            responses.append({"error": str(e)})
    
    return responses


@app.get("/health", response_model=HealthCheckResponse)
async def health_check() -> HealthCheckResponse:
    """
    Health check endpoint.
    
    Returns:
        Health status and metrics
    """
    uptime = (datetime.now() - model_stats['start_time']).total_seconds()
    
    return HealthCheckResponse(
        status="healthy",
        model_loaded=classifier is not None,
        predictions_served=model_stats['predictions_served'],
        uptime_seconds=uptime,
        timestamp=datetime.now().isoformat()
    )


@app.get("/metrics", response_model=MetricsResponse)
async def get_metrics() -> MetricsResponse:
    """
    Get performance metrics.
    
    Returns:
        Metrics about predictions and system
    """
    uptime = (datetime.now() - model_stats['start_time']).total_seconds()
    avg_latency = (
        model_stats['total_latency_ms'] / model_stats['predictions_served']
        if model_stats['predictions_served'] > 0
        else 0
    )
    
    return MetricsResponse(
        total_predictions=model_stats['predictions_served'],
        total_errors=model_stats['errors'],
        average_latency_ms=avg_latency,
        uptime_seconds=uptime,
        timestamp=datetime.now().isoformat()
    )


@app.get("/lighting-info/{state}")
async def get_lighting_info(state: str):
    """
    Get lighting configuration for a specific state.
    
    Args:
        state: State name (calm, alert, risk, flow, deviation)
    
    Returns:
        Lighting configuration and description
    """
    valid_states = ['calm', 'alert', 'risk', 'flow', 'deviation']
    
    if state not in valid_states:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid state. Must be one of {valid_states}"
        )
    
    lighting_config = map_state_to_lighting(state)
    description = describe_lighting_pattern(state)
    
    return {
        'state': state,
        'lighting_config': lighting_config,
        'description': description
    }


@app.get("/info")
async def get_info():
    """Get API information."""
    return {
        'name': 'Multi-Signal State Classifier API',
        'version': '1.0.0',
        'description': 'ML pipeline for multi-source signal fusion',
        'states': ['calm', 'alert', 'risk', 'flow', 'deviation'],
        'endpoints': {
            'predict': 'POST /predict',
            'batch_predict': 'POST /predict/batch',
            'health': 'GET /health',
            'metrics': 'GET /metrics',
            'lighting_info': 'GET /lighting-info/{state}',
            'docs': 'GET /docs'
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


