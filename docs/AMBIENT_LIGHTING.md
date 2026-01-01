# Ambient Lighting & Timeline Rationale

Why hourly data collection is essential for meaningful ambient lighting control.

## 💡 Why Hourly Data Collection for Ambient Lighting?

### The Problem with Daily Collection

If we classify states **once per day**, the ambient lighting would:
- ❌ Change only once per day (at midnight or end of trading day)
- ❌ Not reflect real-time conditions throughout the day
- ❌ Miss important intraday state changes
- ❌ Provide minimal value as a real-time monitoring tool

**Example**: If a risk state occurs at 2 PM, but we only classify at end-of-day, the lighting wouldn't warn you until the next day - too late!

---

## ✅ Solution: Hourly Data Collection

### Why Hourly Makes Sense

**1. Real-Time Responsiveness**
- Lighting updates **every hour** based on current state
- Can reflect changing conditions throughout the day
- Provides timely visual feedback

**2. Realistic for Both Use Cases**

**Trading (Intraday)**:
- Hourly snapshots of price movements, volatility, volume
- RSI can be calculated hourly
- Common in swing trading and intraday analysis
- 2,500 samples = ~104 days of hourly trading data

**Plant Health (IoT Sensors)**:
- Hourly sensor readings are standard for IoT monitoring
- Soil moisture, temperature, stress sensors typically read hourly
- Allows for timely intervention when issues arise
- 2,500 samples = ~104 days of hourly sensor data

**3. Meaningful Lighting Updates**
- Lighting can change throughout the day as conditions change
- Morning: calm state → warm light
- Afternoon: risk detected → red warning light
- Evening: flow state → optimal blue-white light
- **This makes the lighting system actually useful!**

---

## 🎯 How Ambient Lighting Works with Hourly Classification

### Real-World Scenario

**8:00 AM** - System starts in **calm** state
- Trading: Stable overnight, low volatility
- Plant: Good moisture, comfortable temperature
- **Lighting**: Warm white (3000K, 50%, steady)

**10:00 AM** - State changes to **alert**
- Trading: Price drop detected, volatility increasing
- Plant: Temperature rising, moisture decreasing
- **Lighting**: Bright white (4000K, 70%, gentle pulsing) ⚠️

**2:00 PM** - State escalates to **risk**
- Trading: Significant price drop, high volatility
- Plant: High temperature, low moisture, high stress
- **Lighting**: Red-orange (2000K, 85%, urgent pulsing) 🚨

**4:00 PM** - State improves to **flow**
- Trading: Recovery, positive trend
- Plant: Conditions optimal
- **Lighting**: Blue-white (5000K, 80%, steady smooth) ✨

**6:00 PM** - Back to **calm**
- Trading: Market closed, stable
- Plant: Evening conditions good
- **Lighting**: Warm white (3000K, 50%, steady)

### Key Benefits

✅ **Timely Warnings**: Lighting changes within hours, not days
✅ **Real-Time Monitoring**: Reflects current conditions
✅ **Actionable**: You can respond to issues as they develop
✅ **Meaningful**: Lighting actually provides value throughout the day

---

## 📊 Timeline Details

### Data Collection: **Hourly**

- **Frequency**: 1 sample per hour
- **Start**: January 1, 2023, 00:00:00
- **Coverage**: 2,500 samples = ~104 days (~3.5 months)
- **Trading Hours**: Can filter to market hours (9:30 AM - 4:00 PM EST)
- **Plant Health**: Continuous 24/7 monitoring

### Rolling Windows (Historical Context)

With hourly data, rolling windows provide short-term context:

- **3 hours**: Recent trend (last 3 hours)
- **5 hours**: Short-term pattern (last 5 hours)
- **10 hours**: Medium-term trend (last 10 hours = ~1 work day)
- **20 hours**: Daily pattern (last 20 hours = ~1 day)

**Why This Matters**:
- A single hour's spike might be noise
- But 3-5 hours of consistent signals = real pattern
- Lighting responds to **patterns**, not just single data points

---

## 🔄 Classification & Lighting Update Flow

### Hourly Update Cycle

```
Hour 1 (8:00 AM)
├── Collect signals (trading + plant health)
├── Extract features (current + rolling windows)
├── Classify state → "calm"
└── Update lighting → Warm white (3000K, 50%)

Hour 2 (9:00 AM)
├── Collect new signals
├── Extract features (includes Hour 1 in rolling window)
├── Classify state → "alert" (conditions changed)
└── Update lighting → Bright white (4000K, 70%, pulsing)

Hour 3 (10:00 AM)
├── Collect new signals
├── Extract features (includes Hours 1-2 in rolling window)
├── Classify state → "risk" (trend confirmed)
└── Update lighting → Red-orange (2000K, 85%, urgent)
```

### State Persistence

- States can persist across multiple hours
- If conditions remain stable, state stays the same
- Lighting reflects current state, not just changes
- Smooth transitions prevent flickering

---

## 🎨 Lighting Behavior Examples

### Scenario 1: Normal Day

| Time | Trading State | Plant State | Combined State | Lighting |
|------|--------------|------------|----------------|----------|
| 8 AM | Stable | Good | **calm** | Warm white, steady |
| 12 PM | Stable | Good | **calm** | Warm white, steady |
| 4 PM | Stable | Good | **calm** | Warm white, steady |
| 8 PM | Closed | Good | **calm** | Warm white, steady |

**Result**: Lighting stays consistent throughout the day

### Scenario 2: Problem Detected

| Time | Trading State | Plant State | Combined State | Lighting |
|------|--------------|------------|----------------|----------|
| 8 AM | Stable | Good | **calm** | Warm white, steady |
| 10 AM | Volatile | Warming | **alert** | Bright white, pulsing ⚠️ |
| 12 PM | Dropping | Hot, dry | **risk** | Red-orange, urgent 🚨 |
| 2 PM | Dropping | Hot, dry | **risk** | Red-orange, urgent 🚨 |
| 4 PM | Recovering | Improving | **alert** | Bright white, pulsing ⚠️ |
| 6 PM | Stable | Good | **calm** | Warm white, steady |

**Result**: Lighting provides timely warning and recovery feedback

### Scenario 3: Optimal Conditions

| Time | Trading State | Plant State | Combined State | Lighting |
|------|--------------|------------|----------------|----------|
| 8 AM | Positive | Optimal | **flow** | Blue-white, smooth ✨ |
| 12 PM | Positive | Optimal | **flow** | Blue-white, smooth ✨ |
| 4 PM | Positive | Optimal | **flow** | Blue-white, smooth ✨ |

**Result**: Lighting indicates everything is optimal

---

## 📈 Data Interpretation

### Trading Signals (Hourly)

**price_change**: Hour-over-hour price movement
- Can be calculated from hourly price snapshots
- Shows intraday trends

**volatility**: Hourly volatility measure
- Rolling standard deviation of hourly returns
- Shows intraday risk

**volume**: Hourly trading volume
- Volume traded in that hour
- Shows intraday activity

**rsi**: Hourly RSI calculation
- Can be calculated from hourly price data
- Shows intraday momentum

### Plant Health Signals (Hourly)

**soil_moisture**: Hourly sensor reading
- Standard IoT sensor frequency
- Shows moisture trends

**temperature**: Hourly sensor reading
- Standard IoT sensor frequency
- Shows temperature patterns

**stress_score**: Hourly calculated stress
- Can be calculated from multiple sensor inputs
- Shows plant health trends

---

## 🎯 Why This Makes Sense for ML Zoomcamp

### Real-World Application

✅ **Practical Use Case**: Ambient lighting that actually responds to conditions
✅ **Real-Time Monitoring**: Useful throughout the day, not just once
✅ **Actionable Insights**: Can respond to issues as they develop
✅ **Demonstrates ML Value**: Shows how ML can drive real-time systems

### Technical Demonstration

✅ **Time-Series ML**: Rolling windows, temporal patterns
✅ **Multi-Source Fusion**: Combining different data sources
✅ **Real-Time Inference**: API can handle hourly updates
✅ **State Classification**: Meaningful state changes

---

## 🔧 Implementation Summary

**Current Configuration**:
- **Collection Frequency**: Hourly (1 sample per hour)
- **Timeline**: 2,500 samples = ~104 days (~3.5 months)
- **Rolling Windows**: 3, 5, 10, 20 hours
- **Lighting Updates**: Every hour based on current state
- **Real-Time Capability**: API can process new data hourly

**Code**:
```python
# Hourly timestamps
timestamps = [start_date + timedelta(hours=i) for i in range(len(unified_df))]
```

**Result**: Ambient lighting that provides meaningful, real-time visual feedback throughout the day! 💡

---

## 💡 Key Takeaway

**Daily classification** → Lighting changes once per day → Not useful for real-time monitoring

**Hourly classification** → Lighting updates every hour → Provides timely, actionable feedback

The hourly approach makes the ambient lighting application **actually meaningful** as a real-time monitoring and alerting system!

---

## Related Documentation

- [Data Documentation](DATA.md) - Data structure and generation
- [API Documentation](API.md) - API endpoints for predictions
- [Development Guide](DEVELOPMENT.md) - Working with the codebase

---

**Last Updated**: January 2025

