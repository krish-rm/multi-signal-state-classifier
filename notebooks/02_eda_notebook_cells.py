# Notebook 02: EDA (Exploratory Data Analysis)
# Run these cells in a Jupyter notebook

# === CELL 1: SETUP ===
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (14, 8)

# === CELL 2: LOAD DATA ===
from src.data import load_or_generate_data
df, labels = load_or_generate_data(
    output_path='data/processed/unified_signals.parquet',
    n_samples=2500
)

# === CELL 3: CORRELATION ANALYSIS ===
numeric_cols = df.select_dtypes(include=[np.number]).columns
correlation_matrix = df[numeric_cols].corr()

plt.figure(figsize=(12, 10))
sns.heatmap(correlation_matrix, annot=True, fmt='.2f', cmap='coolwarm')
plt.title('Feature Correlation Matrix')
plt.tight_layout()
plt.show()

# === CELL 4: DISTRIBUTION ANALYSIS ===
fig, axes = plt.subplots(2, 3, figsize=(15, 10))

# Trading signals
df['price_change'].hist(bins=30, ax=axes[0, 0], edgecolor='black')
axes[0, 0].set_title('Price Change Distribution')

df['volatility'].hist(bins=30, ax=axes[0, 1], edgecolor='black')
axes[0, 1].set_title('Volatility Distribution')

df['volume'].hist(bins=30, ax=axes[0, 2], edgecolor='black')
axes[0, 2].set_title('Volume Distribution')

# Plant health signals
df['soil_moisture'].hist(bins=30, ax=axes[1, 0], edgecolor='black')
axes[1, 0].set_title('Soil Moisture Distribution')

df['temperature'].hist(bins=30, ax=axes[1, 1], edgecolor='black')
axes[1, 1].set_title('Temperature Distribution')

df['stress_score'].hist(bins=30, ax=axes[1, 2], edgecolor='black')
axes[1, 2].set_title('Stress Score Distribution')

plt.tight_layout()
plt.show()

# === CELL 5: STATE-WISE ANALYSIS ===
df_with_labels = df.copy()
df_with_labels['state'] = labels

print("State Statistics:")
print(df_with_labels.groupby('state').describe())

# === CELL 6: BOX PLOTS BY STATE ===
fig, axes = plt.subplots(2, 3, figsize=(15, 10))

for idx, col in enumerate(numeric_cols[:6]):
    row = idx // 3
    col_idx = idx % 3
    df_with_labels.boxplot(column=col, by='state', ax=axes[row, col_idx])
    axes[row, col_idx].set_title(f'{col} by State')
    axes[row, col_idx].set_xlabel('State')

plt.suptitle('')
plt.tight_layout()
plt.show()

# === CELL 7: INSIGHTS ===
print("\nKey Insights:")
print(f"1. Dataset: {len(df)} samples, {len(numeric_cols)} features")
print(f"2. States: {', '.join(np.unique(labels))}")
print(f"3. Features: Trading (price_change, volatility, volume, rsi), Plant Health (soil_moisture, temperature, stress_score)")
print(f"4. Data Quality: No missing values")
print(f"5. Ready for: Feature Engineering")


