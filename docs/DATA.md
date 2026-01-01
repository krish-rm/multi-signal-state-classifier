# Data Documentation

Complete documentation of data generation, datapoints, and feature engineering.

## Overview

The Multi-Signal State Classifier uses synthetic data to demonstrate multi-source signal fusion. The dataset combines signals from two different industries (trading + plant health) as a proof of concept.

## Data Collection Timeline

**Frequency**: **Hourly** (1 sample per hour)
- Enables real-time ambient lighting updates throughout the day
- Realistic for both intraday trading snapshots and IoT sensor readings
- 2,500 samples = ~104 days (~3.5 months) of hourly data
- Lighting updates every hour based on current state classification

**Why Hourly?** See [Ambient Lighting Documentation](AMBIENT_LIGHTING.md) for detailed rationale.

---

## Financial/Trading Use Case Datapoints

The trading signals module generates **4 datapoints** for each sample:

### 1. **price_change** (float)
- **Description**: Hour-over-hour price movement percentage
- **Range**: Typically -0.10 to +0.10 (can vary by state)
- **Distribution**: Normal distribution
- **State-Specific Values**:
  - **calm**: `normal(0.001, 0.005)` - Very small, stable changes
  - **alert**: `normal(-0.01, 0.02)` - Moderate negative movement
  - **risk**: `normal(-0.05, 0.03)` - Large negative movement
  - **flow**: `normal(0.03, 0.01)` - Positive trend
  - **deviation**: `normal(0.0, 0.08)` - Erratic, high variance

### 2. **volatility** (float)
- **Description**: Market volatility indicator (standard deviation of returns)
- **Range**: Typically 0.05 to 0.50
- **Distribution**: Normal distribution
- **State-Specific Values**:
  - **calm**: `normal(0.08, 0.02)` - Low volatility (stable market)
  - **alert**: `normal(0.18, 0.03)` - Moderate volatility
  - **risk**: `normal(0.35, 0.05)` - High volatility (turbulent market)
  - **flow**: `normal(0.10, 0.02)` - Low volatility with positive trend
  - **deviation**: `normal(0.25, 0.10)` - Variable, unpredictable volatility

### 3. **volume** (float)
- **Description**: Trading volume (number of shares/contracts traded)
- **Range**: Typically 500,000 to 3,000,000
- **Distribution**: Normal distribution
- **State-Specific Values**:
  - **calm**: `normal(1,000,000, 100,000)` - Normal trading volume
  - **alert**: `normal(1,500,000, 200,000)` - Increased volume
  - **risk**: `normal(2,500,000, 500,000)` - High volume (panic selling/buying)
  - **flow**: `normal(900,000, 100,000)` - Slightly below normal
  - **deviation**: `normal(2,000,000, 800,000)` - Highly variable volume

### 4. **rsi** (Relative Strength Index) (float)
- **Description**: Technical indicator measuring momentum (0-100)
- **Range**: 0 to 100 (clipped)
- **Distribution**: Normal distribution (except deviation uses uniform)
- **State-Specific Values**:
  - **calm**: `normal(50, 5)` - Neutral momentum (~50)
  - **alert**: `normal(45, 8)` - Slightly oversold
  - **risk**: `normal(35, 10)` - Oversold territory
  - **flow**: `normal(60, 5)` - Positive momentum
  - **deviation**: `uniform(20, 80)` - Random, erratic values

---

## Plant Health Use Case Datapoints

The plant health signals module generates **3 datapoints** for each sample:

### 1. **soil_moisture** (float)
- **Description**: Soil moisture level as a percentage
- **Range**: 0.0 to 1.0 (clipped)
- **Distribution**: Normal distribution (except deviation uses choice)
- **State-Specific Values**:
  - **calm**: `normal(0.60, 0.05)` - Good moisture level (~60%)
  - **alert**: `normal(0.45, 0.08)` - Moderate moisture deficit
  - **risk**: `normal(0.30, 0.08)` - Low moisture (drought conditions)
  - **flow**: `normal(0.65, 0.03)` - Optimal moisture level
  - **deviation**: `choice([normal(0.20, 0.05), normal(0.85, 0.05)])` - Either very dry or very wet (anomalous)

### 2. **temperature** (float)
- **Description**: Temperature in Celsius
- **Range**: Typically 15°C to 30°C
- **Distribution**: Normal distribution (except deviation uses uniform)
- **State-Specific Values**:
  - **calm**: `normal(21, 1)` - Comfortable temperature (~21°C)
  - **alert**: `normal(24, 2)` - Slightly elevated temperature
  - **risk**: `normal(28, 2)` - High temperature (heat stress)
  - **flow**: `normal(22.5, 1)` - Optimal temperature
  - **deviation**: `uniform(15, 30)` - Random temperature (anomalous)

### 3. **stress_score** (float)
- **Description**: Plant stress indicator (0 = no stress, 1 = maximum stress)
- **Range**: 0.0 to 1.0 (clipped)
- **Distribution**: Normal distribution (except deviation uses uniform)
- **State-Specific Values**:
  - **calm**: `normal(0.25, 0.05)` - Low stress (~25%)
  - **alert**: `normal(0.40, 0.08)` - Moderate stress
  - **risk**: `normal(0.75, 0.08)` - High stress (urgent attention needed)
  - **flow**: `normal(0.15, 0.05)` - Minimal stress (optimal conditions)
  - **deviation**: `uniform(0.0, 1.0)` - Random stress level (anomalous)

---

## Complete Dataset Structure

When combined, the unified dataset contains:

### Total Features: **7 Raw Datapoints**

**Trading Signals (4):**
1. `price_change`
2. `volatility`
3. `volume`
4. `rsi`

**Plant Health Signals (3):**
5. `soil_moisture`
6. `temperature`
7. `stress_score`

### Additional Metadata:
- `timestamp` - Sequential timestamps starting from 2023-01-01 (hourly intervals)
- `state` - Target label (calm, alert, risk, flow, deviation)

---

## State-Specific Characteristics Summary

### **calm** State
- **Trading**: Stable prices, low volatility, normal volume, neutral RSI
- **Plant**: Good moisture, comfortable temperature, low stress

### **alert** State
- **Trading**: Negative price movement, moderate volatility, increased volume, oversold RSI
- **Plant**: Moderate moisture deficit, elevated temperature, moderate stress

### **risk** State
- **Trading**: Large negative price movement, high volatility, very high volume, oversold RSI
- **Plant**: Low moisture (drought), high temperature, high stress

### **flow** State
- **Trading**: Positive price trend, low volatility, slightly low volume, positive momentum RSI
- **Plant**: Optimal moisture, optimal temperature, minimal stress

### **deviation** State
- **Trading**: Erratic price changes, variable volatility, highly variable volume, random RSI
- **Plant**: Anomalous moisture (very dry OR very wet), random temperature, random stress

---

## Data Generation Parameters

### Default Settings:
- **Total Samples**: 2,500 (500 per state)
- **Seed**: 42 (for reproducibility)
- **Distribution**: Balanced across all 5 states
- **Data Format**: Pandas DataFrame with Parquet storage

### Generation Method:
- Uses `numpy.random` with state-specific normal distributions
- Each state has distinct parameter values (mean, std) for each feature
- Values are clipped to valid ranges (e.g., RSI: 0-100, moisture: 0-1)
- Timestamps are sequential (hourly intervals)

---

## Customization

You can customize the data generation by:

1. **Changing sample size**: `n_samples` parameter
2. **Adjusting state distribution**: `state_distribution` dictionary
3. **Modifying parameters**: Edit the normal distribution parameters in `SignalDataGenerator` class
4. **Changing seed**: `seed` parameter in `__init__`

---

## Feature Engineering

From these **7 raw datapoints**, the feature engineering pipeline creates **256 engineered features** including:

### Time-Series Features
- Rolling statistics (mean, std, min, max) over multiple windows (3, 5, 10, 20 hours)
- Trend indicators (slope, acceleration, change rate)
- Statistical features (skewness, kurtosis)

### Multi-Source Fusion
- Cross-source correlations
- Interaction terms
- Source-specific normalization
- Z-score features

### Engineered Features
- State-specific indicators
- Frequency domain features
- Normalized differences

**Result**: 256 engineered features with high predictive power

---

## Real-World Interpretation

### Trading Signals:
- **price_change**: Hour-over-hour return percentage
- **volatility**: Risk measure (higher = more volatile)
- **volume**: Market activity indicator
- **rsi**: Momentum indicator (30 = oversold, 70 = overbought)

### Plant Health Signals:
- **soil_moisture**: Water availability (0.4-0.7 = optimal)
- **temperature**: Environmental stress factor (20-25°C = optimal)
- **stress_score**: Overall plant health indicator (lower = healthier)

---

## Data Quality

- **Missing Values**: 0%
- **Infinite Values**: 0%
- **Data Quality**: Excellent
- **State Distribution**: Evenly balanced (500 samples per state)
- **Reproducibility**: Fixed seed (42) ensures reproducible generation

---

## Production Considerations

**Note**: These are synthetic datapoints designed to demonstrate the multi-source signal fusion concept. In production, you would replace these with real data sources from your trading platform and IoT sensors.

For production use:
1. Replace synthetic data generators with real data connectors
2. Implement data validation and quality checks
3. Set up data pipelines for continuous ingestion
4. Monitor data drift and distribution changes
5. Implement data versioning and lineage tracking

---

## Related Documentation

- [Ambient Lighting Documentation](AMBIENT_LIGHTING.md) - Why hourly data collection
- [Development Guide](DEVELOPMENT.md) - Working with data in development
- [API Documentation](API.md) - API request/response formats

