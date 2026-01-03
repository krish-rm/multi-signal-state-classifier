"""
Main training script for the multi-signal state classifier.
"""

import os
import sys
import logging
import pandas as pd
import numpy as np

from src.data import load_or_generate_data
from src.data.feature_engineering import FeaturePipeline
from src.models import EnsembleClassifier, split_data_time_series, evaluate_model

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main training pipeline."""
    
    logger.info("=" * 80)
    logger.info("Multi-Signal State Classifier - Training Pipeline")
    logger.info("=" * 80)
    
    # Step 1: Load data
    logger.info("\n[Step 1] Loading Data...")
    output_path = "data/processed/unified_signals.parquet"
    df, labels = load_or_generate_data(output_path, n_samples=2500, force_generate=True)
    
    logger.info(f"Dataset shape: {df.shape}")
    logger.info(f"State distribution:\n{pd.Series(labels).value_counts()}")
    
    # Step 2: Feature Engineering
    logger.info("\n[Step 2] Feature Engineering...")
    feature_pipeline = FeaturePipeline()
    X, feature_names = feature_pipeline.fit_transform(df)
    
    logger.info(f"Engineered features shape: {X.shape}")
    logger.info(f"Number of features: {len(feature_names)}")
    
    # Step 3: Shuffle data to ensure balanced class distribution in splits
    # (Data is generated sequentially by state, so we need to shuffle)
    logger.info("\n[Step 3] Shuffling data for balanced splits...")
    indices = np.arange(len(X))
    np.random.seed(42)
    np.random.shuffle(indices)
    if isinstance(X, pd.DataFrame):
        X = X.iloc[indices].reset_index(drop=True)
    else:
        X = X[indices]
    labels = labels[indices]
    
    logger.info(f"State distribution after shuffle:\n{pd.Series(labels).value_counts()}")
    
    # Step 4: Split Data
    logger.info("\n[Step 4] Splitting Data (Time-Series Aware)...")
    (X_train, y_train), (X_val, y_val), (X_test, y_test) = split_data_time_series(
        X, labels, train_ratio=0.70, val_ratio=0.15, test_ratio=0.15
    )
    
    logger.info(f"Train set state distribution:\n{pd.Series(y_train).value_counts()}")
    logger.info(f"Val set state distribution:\n{pd.Series(y_val).value_counts()}")
    logger.info(f"Test set state distribution:\n{pd.Series(y_test).value_counts()}")
    
    # Step 5: Train Ensemble Model
    logger.info("\n[Step 5] Training Ensemble Model...")
    ensemble = EnsembleClassifier(weights={
        'lightgbm': 0.40,
        'xgboost': 0.35,
        'random_forest': 0.25
    })
    
    ensemble.train(X_train, y_train, X_val, y_val, random_state=42)
    
    # Step 6: Evaluate on Validation Set
    logger.info("\n[Step 6] Evaluating on Validation Set...")
    val_metrics = evaluate_model(ensemble, X_val, y_val, "Validation Set")
    
    # Step 7: Evaluate on Test Set
    logger.info("\n[Step 7] Evaluating on Test Set...")
    test_metrics = evaluate_model(ensemble, X_test, y_test, "Test Set")
    
    # Step 8: Save Model
    logger.info("\n[Step 8] Saving Model...")
    os.makedirs("models", exist_ok=True)
    model_path = "models/ensemble_model.pkl"
    ensemble.save(model_path)
    
    # Save feature pipeline
    import pickle
    with open("models/feature_pipeline.pkl", 'wb') as f:
        pickle.dump(feature_pipeline, f)
    logger.info("Feature pipeline saved")
    
    # Summary
    logger.info("\n" + "=" * 80)
    logger.info("Training Complete!")
    logger.info("=" * 80)
    logger.info(f"Test F1-Score (macro): {test_metrics['f1_macro']:.4f}")
    logger.info(f"Test Accuracy: {test_metrics['accuracy']:.4f}")
    logger.info(f"Model saved to: {model_path}")
    logger.info("=" * 80)
    
    return ensemble, feature_pipeline, test_metrics


if __name__ == "__main__":
    main()


