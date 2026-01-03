"""
Model training for multi-signal state classification.
"""

import numpy as np
import pandas as pd
from typing import Tuple, Dict, Any
import logging
import pickle

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.metrics import (
    f1_score, accuracy_score, precision_score, recall_score,
    classification_report, confusion_matrix
)

try:
    import xgboost as xgb
    HAS_XGBOOST = True
except ImportError:
    HAS_XGBOOST = False

try:
    import lightgbm as lgb
    HAS_LIGHTGBM = True
except ImportError:
    HAS_LIGHTGBM = False

logger = logging.getLogger(__name__)


class BaselineModels:
    """Train baseline models for comparison."""
    
    @staticmethod
    def train_random_forest(X_train, y_train, n_estimators=100, random_state=42):
        """Train Random Forest baseline."""
        model = RandomForestClassifier(
            n_estimators=n_estimators,
            random_state=random_state,
            n_jobs=-1,
            max_depth=15,
            min_samples_split=5
        )
        model.fit(X_train, y_train)
        return model
    
    @staticmethod
    def train_xgboost(X_train, y_train, n_estimators=100, random_state=42):
        """Train XGBoost baseline."""
        if not HAS_XGBOOST:
            raise ImportError("XGBoost not installed")
        
        # Convert labels to numeric
        unique_classes = np.unique(y_train)
        label_map = {label: idx for idx, label in enumerate(unique_classes)}
        y_train_numeric = np.array([label_map[y] for y in y_train])
        
        model = xgb.XGBClassifier(
            n_estimators=n_estimators,
            random_state=random_state,
            n_jobs=-1,
            max_depth=6,
            learning_rate=0.1,
            verbosity=0
        )
        model.fit(X_train, y_train_numeric)
        model.label_map = label_map
        return model
    
    @staticmethod
    def train_lightgbm(X_train, y_train, n_estimators=100, random_state=42):
        """Train LightGBM baseline."""
        if not HAS_LIGHTGBM:
            raise ImportError("LightGBM not installed")
        
        # Convert labels to numeric
        unique_classes = np.unique(y_train)
        label_map = {label: idx for idx, label in enumerate(unique_classes)}
        y_train_numeric = np.array([label_map[y] for y in y_train])
        
        model = lgb.LGBMClassifier(
            n_estimators=n_estimators,
            random_state=random_state,
            n_jobs=-1,
            max_depth=8,
            learning_rate=0.1,
            verbosity=-1
        )
        model.fit(X_train, y_train_numeric)
        model.label_map = label_map
        return model


class EnsembleClassifier:
    """Weighted ensemble of multiple classifiers."""
    
    def __init__(self, weights: Dict[str, float] = None):
        """
        Initialize ensemble.
        
        Args:
            weights: Dictionary of model weights (must sum to 1)
        """
        self.weights = weights or {
            'lightgbm': 0.40,
            'xgboost': 0.35,
            'random_forest': 0.25
        }
        self.models = {}
        self.label_map = None
    
    def train(self, X_train, y_train, X_val=None, y_val=None, random_state=42):
        """
        Train ensemble models.
        
        Args:
            X_train: Training features
            y_train: Training labels
            X_val: Validation features (optional)
            y_val: Validation labels (optional)
            random_state: Random seed
        """
        logger.info("Training ensemble models...")
        
        # Create label mapping (sorted for consistency with sklearn)
        unique_classes = sorted(np.unique(y_train))
        self.label_map = {label: idx for idx, label in enumerate(unique_classes)}
        self.reverse_label_map = {idx: label for label, idx in self.label_map.items()}
        
        # Train Random Forest
        logger.info("Training Random Forest...")
        self.models['random_forest'] = BaselineModels.train_random_forest(
            X_train, y_train, random_state=random_state
        )
        
        # Train XGBoost if available
        if HAS_XGBOOST and self.weights.get('xgboost', 0) > 0:
            logger.info("Training XGBoost...")
            try:
                self.models['xgboost'] = BaselineModels.train_xgboost(
                    X_train, y_train, random_state=random_state
                )
            except Exception as e:
                logger.warning(f"XGBoost training failed: {e}")
        
        # Train LightGBM if available
        if HAS_LIGHTGBM and self.weights.get('lightgbm', 0) > 0:
            logger.info("Training LightGBM...")
            try:
                self.models['lightgbm'] = BaselineModels.train_lightgbm(
                    X_train, y_train, random_state=random_state
                )
            except Exception as e:
                logger.warning(f"LightGBM training failed: {e}")
        
        logger.info(f"Trained {len(self.models)} models")
    
    def predict(self, X, return_proba=False):
        """
        Make predictions using ensemble.
        
        Args:
            X: Features
            return_proba: Return probability estimates
        
        Returns:
            Predictions or (predictions, probabilities)
        """
        # Get ensemble's class order (sorted for consistency)
        ensemble_classes = sorted(self.label_map.keys())
        n_classes = len(ensemble_classes)
        n_samples = X.shape[0] if hasattr(X, 'shape') else len(X)
        
        # Collect predictions and probabilities from all models
        predictions = []
        probabilities = []
        
        for model_name, model in self.models.items():
            # Get raw predictions
            pred = model.predict(X)
            
            # Convert to string labels if needed
            if model_name in ['xgboost', 'lightgbm'] and hasattr(model, 'label_map'):
                # XGBoost/LightGBM return numeric predictions
                reverse_map = {v: k for k, v in model.label_map.items()}
                pred = np.array([reverse_map.get(int(p), str(p)) for p in pred])
            elif hasattr(model, 'classes_') and isinstance(model.classes_[0], (int, np.integer)):
                # If sklearn model uses numeric classes, map them
                if hasattr(model, 'label_map'):
                    reverse_map = {v: k for k, v in model.label_map.items()}
                    pred = np.array([reverse_map.get(int(p), str(p)) for p in pred])
            
            predictions.append(pred)
            
            if return_proba:
                # Get probabilities from model
                proba = model.predict_proba(X)
                
                # Align probabilities to ensemble's class order
                aligned_proba = np.zeros((n_samples, n_classes), dtype=float)
                
                if model_name in ['xgboost', 'lightgbm'] and hasattr(model, 'label_map'):
                    # XGBoost/LightGBM: map from model's label_map to ensemble's
                    for model_idx, model_label in enumerate(sorted(model.label_map.keys())):
                        if model_label in self.label_map:
                            ensemble_idx = self.label_map[model_label]
                            aligned_proba[:, ensemble_idx] = proba[:, model_idx]
                elif hasattr(model, 'classes_'):
                    # sklearn models: map from model.classes_ to ensemble order
                    for model_idx, model_class in enumerate(model.classes_):
                        if model_class in self.label_map:
                            ensemble_idx = self.label_map[model_class]
                            aligned_proba[:, ensemble_idx] = proba[:, model_idx]
                else:
                    # Fallback: assume same order
                    aligned_proba = proba
                
                probabilities.append(aligned_proba)
        
        # Weighted voting with probabilities
        if return_proba and probabilities:
            weighted_proba = np.zeros((n_samples, n_classes), dtype=float)
            
            # Weight and sum probabilities
            for i, (model_name, model) in enumerate(self.models.items()):
                weight = self.weights.get(model_name, 1.0 / len(self.models))
                weighted_proba += weight * probabilities[i]
            
            # Get final predictions from weighted probabilities
            final_preds = np.argmax(weighted_proba, axis=1)
            final_preds = np.array([self.reverse_label_map[p] for p in final_preds])
            
            return final_preds, weighted_proba
        
        # Simple voting (when return_proba=False)
        final_preds = []
        for col in range(n_samples):
            pred_col = [pred[col] for pred in predictions]
            # Get most common prediction
            unique, counts = np.unique(pred_col, return_counts=True)
            final_preds.append(unique[np.argmax(counts)])
        
        return np.array(final_preds)
    
    def predict_proba(self, X):
        """Get probability estimates for each class."""
        _, probabilities = self.predict(X, return_proba=True)
        return probabilities
    
    def save(self, filepath: str):
        """Save ensemble to file."""
        with open(filepath, 'wb') as f:
            pickle.dump(self, f)
        logger.info(f"Ensemble saved to {filepath}")
    
    @staticmethod
    def load(filepath: str):
        """Load ensemble from file."""
        with open(filepath, 'rb') as f:
            ensemble = pickle.load(f)
        logger.info(f"Ensemble loaded from {filepath}")
        return ensemble


def evaluate_model(model, X_test, y_test, model_name="Model"):
    """
    Evaluate model performance.
    
    Args:
        model: Trained model
        X_test: Test features
        y_test: Test labels
        model_name: Name for logging
    
    Returns:
        Dictionary of metrics
    """
    y_pred = model.predict(X_test)
    
    metrics = {
        'accuracy': accuracy_score(y_test, y_pred),
        'f1_weighted': f1_score(y_test, y_pred, average='weighted', zero_division=0),
        'f1_macro': f1_score(y_test, y_pred, average='macro', zero_division=0),
        'precision': precision_score(y_test, y_pred, average='weighted', zero_division=0),
        'recall': recall_score(y_test, y_pred, average='weighted', zero_division=0),
    }
    
    logger.info(f"\n{model_name} Performance:")
    logger.info(f"Accuracy: {metrics['accuracy']:.4f}")
    logger.info(f"F1-Score (macro): {metrics['f1_macro']:.4f}")
    logger.info(f"F1-Score (weighted): {metrics['f1_weighted']:.4f}")
    logger.info(f"Precision: {metrics['precision']:.4f}")
    logger.info(f"Recall: {metrics['recall']:.4f}")
    
    # Per-class metrics
    logger.info(f"\nClassification Report:\n{classification_report(y_test, y_pred)}")
    
    # Confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    logger.info(f"\nConfusion Matrix:\n{cm}")
    
    metrics['confusion_matrix'] = cm
    metrics['classification_report'] = classification_report(y_test, y_pred)
    
    return metrics


def split_data_time_series(
    X: pd.DataFrame,
    y: np.ndarray,
    train_ratio: float = 0.70,
    val_ratio: float = 0.15,
    test_ratio: float = 0.15
) -> Tuple[tuple, tuple, tuple]:
    """
    Split data chronologically (time-series aware).
    
    Args:
        X: Features dataframe
        y: Labels array
        train_ratio: Training set ratio
        val_ratio: Validation set ratio
        test_ratio: Test set ratio
    
    Returns:
        Tuples of (X_train, y_train), (X_val, y_val), (X_test, y_test)
    """
    n = len(X)
    train_idx = int(n * train_ratio)
    val_idx = int(n * (train_ratio + val_ratio))
    
    X_train, y_train = X[:train_idx], y[:train_idx]
    X_val, y_val = X[train_idx:val_idx], y[train_idx:val_idx]
    X_test, y_test = X[val_idx:], y[val_idx:]
    
    logger.info(f"Data split - Train: {len(X_train)}, Val: {len(X_val)}, Test: {len(X_test)}")
    
    return (X_train, y_train), (X_val, y_val), (X_test, y_test)


