"""
Prediction module for state classification.
"""

import numpy as np
import pandas as pd
import pickle
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class StateClassifier:
    """Main state classifier for inference."""
    
    def __init__(self, model_path: str, feature_pipeline=None):
        """
        Initialize classifier.
        
        Args:
            model_path: Path to trained model
            feature_pipeline: Feature engineering pipeline for new data
        """
        self.model = self._load_model(model_path)
        self.feature_pipeline = feature_pipeline
        self.model_version = "1.0.0"
    
    @staticmethod
    def _load_model(model_path: str):
        """Load trained model from file."""
        try:
            with open(model_path, 'rb') as f:
                model = pickle.load(f)
            logger.info(f"Model loaded from {model_path}")
            return model
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise
    
    def predict(self, features: np.ndarray) -> Dict[str, Any]:
        """
        Predict state with confidence scores.
        
        Args:
            features: Input features (1D or 2D array)
        
        Returns:
            Dictionary with prediction, confidence, and probabilities
        """
        if isinstance(features, pd.DataFrame):
            features = features.values
        
        # Handle single sample
        if features.ndim == 1:
            features = features.reshape(1, -1)
        
        # Get probabilities first - this is the source of truth
        try:
            probabilities = self.model.predict_proba(features)[0]
            
            # Get classes - check for reverse_label_map first (for EnsembleClassifier)
            if hasattr(self.model, 'reverse_label_map'):
                # Model uses numeric indices, map them to string labels
                classes = [self.model.reverse_label_map[i] for i in range(len(probabilities))]
            elif hasattr(self.model, 'label_map'):
                classes = sorted(self.model.label_map.keys())
            elif hasattr(self.model, 'classes_'):
                classes = self.model.classes_
                # If classes are numeric, try to map them
                if isinstance(classes[0], (int, np.integer)) and hasattr(self.model, 'reverse_label_map'):
                    classes = [self.model.reverse_label_map[int(c)] for c in classes]
            else:
                classes = ['calm', 'alert', 'risk', 'flow', 'deviation']
            
            # Create probability dict
            prob_dict = {cls: float(prob) for cls, prob in zip(classes, probabilities)}
            confidence = float(max(probabilities))
            
            # Determine state from probabilities (highest probability wins)
            # This ensures state matches what's shown in the probability chart
            max_prob_idx = int(np.argmax(probabilities))
            prediction = classes[max_prob_idx]
        except Exception as e:
            logger.warning(f"Error getting probabilities: {e}")
            # Fallback: use predict() if predict_proba() fails
            prediction = self.model.predict(features)[0]
            
            # Try to convert prediction to string label
            if hasattr(self.model, 'reverse_label_map'):
                if isinstance(prediction, (int, np.integer)):
                    prediction = self.model.reverse_label_map[int(prediction)]
                elif isinstance(prediction, str) and prediction.isdigit():
                    prediction = self.model.reverse_label_map[int(prediction)]
            
            prob_dict = {str(prediction): 1.0}
            confidence = 1.0
        
        return {
            'state': str(prediction),
            'confidence': confidence,
            'probabilities': prob_dict
        }
    
    def predict_batch(self, features_list: list) -> list:
        """
        Batch prediction for multiple samples.
        
        Args:
            features_list: List of feature vectors
        
        Returns:
            List of prediction dictionaries
        """
        predictions = []
        for features in features_list:
            predictions.append(self.predict(features))
        return predictions
    
    def predict_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Predict for dataframe of samples.
        
        Args:
            df: DataFrame with samples
        
        Returns:
            DataFrame with predictions
        """
        results = []
        
        for idx, row in df.iterrows():
            pred = self.predict(row.values)
            pred['index'] = idx
            results.append(pred)
        
        return pd.DataFrame(results)


