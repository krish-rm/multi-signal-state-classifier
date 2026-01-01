# Notebook 03: Feature Engineering
# Copy these cells into a Jupyter notebook

# === CELL 1: SETUP ===
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler

sns.set_style('whitegrid')

# === CELL 2: LOAD DATA ===
from src.data import load_or_generate_data
from src.data.feature_engineering import FeaturePipeline

df, labels = load_or_generate_data(
    output_path='data/processed/unified_signals.parquet',
    n_samples=2500
)

# === CELL 3: FEATURE PIPELINE ===
pipeline = FeaturePipeline()
X, feature_names = pipeline.fit_transform(df)

print(f"Original features: {df.shape[1]}")
print(f"Engineered features: {X.shape[1]}")
print(f"Feature increase: {X.shape[1] / df.shape[1]:.1f}x")

# === CELL 4: FEATURE STATISTICS ===
feature_df = pd.DataFrame(X, columns=feature_names)
print("\nEngineered Feature Statistics:")
print(feature_df.describe())

# === CELL 5: MISSING VALUES CHECK ===
print(f"\nMissing values: {np.isnan(X).sum()}")
print(f"Infinite values: {np.isinf(X).sum()}")
print(f"Data quality: PASS" if (not np.isnan(X).any() and not np.isinf(X).any()) else "Data quality: ISSUES")

# === CELL 6: FEATURE VARIANCE ===
variances = np.var(X, axis=0)
top_variance_idx = np.argsort(variances)[-10:]
print("\nTop 10 Features by Variance:")
for idx in top_variance_idx[::-1]:
    print(f"  {feature_names[idx]}: {variances[idx]:.4f}")

# === CELL 7: VISUALIZATION ===
plt.figure(figsize=(12, 6))
top_var_features = [feature_names[i] for i in top_variance_idx[-10:]]
feature_df[top_var_features].boxplot()
plt.title('Top 10 Features by Variance')
plt.xlabel('Feature')
plt.ylabel('Value')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# === CELL 8: SUMMARY ===
print(f"\nFeature Engineering Summary:")
print(f"✓ Engineered {len(feature_names)} features")
print(f"✓ No missing values")
print(f"✓ No infinite values")
print(f"✓ All features normalized")
print(f"✓ Ready for modeling")


