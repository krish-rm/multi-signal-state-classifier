# Notebook 04: Model Training
# Copy these cells into a Jupyter notebook

# === CELL 1: SETUP ===
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, classification_report

sns.set_style('whitegrid')

# === CELL 2: LOAD DATA ===
from src.data import load_or_generate_data
from src.data.feature_engineering import FeaturePipeline
from src.models import split_data_time_series, EnsembleClassifier, evaluate_model

df, labels = load_or_generate_data(n_samples=2500)
pipeline = FeaturePipeline()
X, feature_names = pipeline.fit_transform(df)

print(f"Features engineered: {X.shape}")
print(f"States: {np.unique(labels)}")

# === CELL 3: SPLIT DATA ===
(X_train, y_train), (X_val, y_val), (X_test, y_test) = split_data_time_series(
    X, labels, train_ratio=0.70, val_ratio=0.15, test_ratio=0.15
)

print(f"Train set: {X_train.shape}")
print(f"Val set: {X_val.shape}")
print(f"Test set: {X_test.shape}")

# === CELL 4: TRAIN ENSEMBLE ===
ensemble = EnsembleClassifier(weights={
    'lightgbm': 0.40,
    'xgboost': 0.35,
    'random_forest': 0.25
})

print("Training ensemble models...")
ensemble.train(X_train, y_train, X_val, y_val)
print("Training complete!")

# === CELL 5: VALIDATION EVALUATION ===
print("\n=== VALIDATION SET ===")
val_metrics = evaluate_model(ensemble, X_val, y_val, "Validation")

# === CELL 6: TEST EVALUATION ===
print("\n=== TEST SET ===")
test_metrics = evaluate_model(ensemble, X_test, y_test, "Test")

# === CELL 7: CONFUSION MATRIX ===
y_pred = ensemble.predict(X_test)
cm = confusion_matrix(y_test, y_pred)

plt.figure(figsize=(10, 8))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.title('Confusion Matrix - Test Set')
plt.ylabel('True')
plt.xlabel('Predicted')
plt.tight_layout()
plt.show()

# === CELL 8: SAVE MODEL ===
import os
os.makedirs('models', exist_ok=True)
ensemble.save('models/ensemble_model.pkl')
print("Model saved to models/ensemble_model.pkl")

# === CELL 9: SUMMARY ===
print(f"\n{'='*60}")
print(f"TRAINING SUMMARY")
print(f"{'='*60}")
print(f"Test Accuracy: {test_metrics['accuracy']:.4f}")
print(f"Test F1-Score (macro): {test_metrics['f1_macro']:.4f}")
print(f"Test F1-Score (weighted): {test_metrics['f1_weighted']:.4f}")
print(f"Test Precision: {test_metrics['precision']:.4f}")
print(f"Test Recall: {test_metrics['recall']:.4f}")
print(f"{'='*60}")


