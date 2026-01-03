# Dashboard Test Combinations

Use these specific input combinations in the dashboard to see different states.

## 🌊 FLOW State (Optimal Conditions)

### Combination 1: Optimal Plant + FLOW Trading
**Plant Health:**
- Soil Moisture: **0.80** (High)
- Temperature: **22.5°C** (Optimal)
- Stress Score: **0.10** (Low)

**Trading Signals:**
- Price Change: **+0.05** (Positive)
- Volatility: **0.10** (Low)
- Volume: **900,000** (Slightly low)
- RSI: **60.0** (Positive momentum)

**Expected Result:** FLOW (69-75% confidence)

---

### Combination 2: Very Optimal All
**Plant Health:**
- Soil Moisture: **0.90** (Very High)
- Temperature: **20.0°C** (Comfortable)
- Stress Score: **0.05** (Very Low)

**Trading Signals:**
- Price Change: **+0.10** (Strong positive)
- Volatility: **0.05** (Very low)
- Volume: **800,000** (Low)
- RSI: **70.0** (Strong momentum)

**Expected Result:** FLOW (50-60% confidence, may show deviation)

---

## 😌 CALM State (Stable Conditions)

### Combination 3: Normal Plant + CALM Trading
**Plant Health:**
- Soil Moisture: **0.60** (Good)
- Temperature: **21.0°C** (Comfortable)
- Stress Score: **0.25** (Low)

**Trading Signals:**
- Price Change: **+0.02** (Slight positive)
- Volatility: **0.08** (Low)
- Volume: **1,000,000** (Normal)
- RSI: **50.0** (Neutral)

**Expected Result:** CALM (83-88% confidence)

---

### Combination 4: Very Neutral All
**Plant Health:**
- Soil Moisture: **0.50** (Mid-range)
- Temperature: **20.0°C** (Comfortable)
- Stress Score: **0.20** (Moderate)

**Trading Signals:**
- Price Change: **0.00** (No change)
- Volatility: **0.05** (Very low)
- Volume: **500,000** (Low)
- RSI: **50.0** (Neutral)

**Expected Result:** CALM (93-97% confidence)

---

## ⚠️ ALERT State (Attention Required) - ⚠️ DIFFICULT TO TRIGGER

**⚠️ IMPORTANT:** ALERT is the hardest state to trigger. The model typically defaults to CALM even with ALERT-like signals. However, you'll see ALERT probability increase in the distribution.

### Combination 5: Alert Plant + ALERT Trading
**Plant Health:**
- Soil Moisture: **0.45** (Moderate deficit)
- Temperature: **24.0°C** (Elevated)
- Stress Score: **0.40** (Moderate)

**Trading Signals:**
- Price Change: **-0.05** (Negative)
- Volatility: **0.18** (Moderate)
- Volume: **1,500,000** (Increased)
- RSI: **45.0** (Oversold)

**Expected Result:** CALM (62-63% confidence), but ALERT will be 34-36% (second highest)

**What to Look For:** Check the probability bar chart - ALERT should be the second-highest bar, showing the model recognizes the alert conditions even if it doesn't predict ALERT as the final state.

---

### Combination 6: More Moderate Stress
**Plant Health:**
- Soil Moisture: **0.40** (Low)
- Temperature: **25.0°C** (High)
- Stress Score: **0.45** (Moderate-High)

**Trading Signals:**
- Price Change: **-0.06** (Negative)
- Volatility: **0.19** (Moderate-High)
- Volume: **1,600,000** (High)
- RSI: **42.0** (Oversold)

**Expected Result:** CALM (59-60% confidence), ALERT 36% (second highest)

**Note:** ALERT state is in a "middle ground" between CALM and RISK, making it harder for the model to confidently predict. The model tends to lean toward CALM (safer) or RISK (more extreme) rather than ALERT.

---

## 🚨 RISK State (Urgent Action Needed)

### Combination 7: Extreme Plant Stress + RISK Trading
**Plant Health:**
- Soil Moisture: **0.15** (Very Low)
- Temperature: **35.0°C** (Very High)
- Stress Score: **0.95** (Very High)

**Trading Signals:**
- Price Change: **-0.15** (Large negative)
- Volatility: **0.35** (High)
- Volume: **2,500,000** (Very High)
- RSI: **30.0** (Oversold)

**Expected Result:** RISK (79-89% confidence)

---

### Combination 8: Maximum Stress All
**Plant Health:**
- Soil Moisture: **0.05** (Extremely Low)
- Temperature: **45.0°C** (Extremely High)
- Stress Score: **0.99** (Maximum)

**Trading Signals:**
- Price Change: **-0.20** (Extreme negative)
- Volatility: **0.40** (Very High)
- Volume: **3,000,000** (Maximum)
- RSI: **20.0** (Extremely Oversold)

**Expected Result:** RISK (79-89% confidence)

---

## 🔄 Testing Conflicting Signals

### Combination 9: FLOW Trading + RISK Plant (Conflict)
**Plant Health:**
- Soil Moisture: **0.15** (Very Low)
- Temperature: **35.0°C** (Very High)
- Stress Score: **0.95** (Very High)

**Trading Signals:**
- Price Change: **+0.05** (Positive)
- Volatility: **0.10** (Low)
- Volume: **900,000** (Low)
- RSI: **60.0** (Positive)

**Expected Result:** CALM (68-70% confidence) - Model defaults to CALM when signals conflict

---

### Combination 10: RISK Trading + FLOW Plant (Conflict)
**Plant Health:**
- Soil Moisture: **0.80** (High)
- Temperature: **22.5°C** (Optimal)
- Stress Score: **0.10** (Low)

**Trading Signals:**
- Price Change: **-0.15** (Large negative)
- Volatility: **0.35** (High)
- Volume: **2,500,000** (Very High)
- RSI: **30.0** (Oversold)

**Expected Result:** CALM (50-78% confidence) - Model defaults to CALM when signals conflict

---

## 📊 Quick Reference Table

| State | Plant Moisture | Plant Temp | Plant Stress | Price Change | Volatility | Volume | RSI | Reliability |
|-------|---------------|------------|--------------|-------------|------------|--------|-----|-------------|
| **FLOW** | 0.80 | 22.5°C | 0.10 | +0.05 | 0.10 | 900K | 60 | ✅ High |
| **CALM** | 0.60 | 21.0°C | 0.25 | +0.02 | 0.08 | 1.0M | 50 | ✅ Very High |
| **ALERT** | 0.45 | 24.0°C | 0.40 | -0.05 | 0.18 | 1.5M | 45 | ⚠️ Low (shows as CALM, ALERT 2nd) |
| **RISK** | 0.15 | 35.0°C | 0.95 | -0.15 | 0.35 | 2.5M | 30 | ✅ High |

---

## 💡 Tips for Testing

1. **For FLOW**: Use optimal plant health (high moisture, optimal temp, low stress) + positive trading signals
2. **For CALM**: Use normal/neutral values for both plant and trading
3. **For ALERT**: Use moderate stress in both plant and trading
4. **For RISK**: Use extreme values in both plant and trading - **both must be extreme** for RISK prediction

5. **Important**: The model requires **both signal types to agree** for non-CALM predictions. If only one is extreme, it will default to CALM.

6. **Check Probabilities**: Even if the predicted state is CALM, check the probability distribution - you'll see ALERT/RISK probabilities increase when you input extreme plant values.

---

## 🎯 Best Combinations to See Each State

- **FLOW**: Combination 1 or 2 ✅ (Reliable - 60-75% confidence)
- **CALM**: Combination 3 or 4 ✅ (Very Reliable - 83-97% confidence)
- **ALERT**: Combination 5 or 6 ⚠️ (Difficult - will show CALM but ALERT will be 2nd highest at 34-36%)
- **RISK**: Combination 7 or 8 ✅ (Reliable - 79-89% confidence)

## ⚠️ Important Notes About ALERT

**ALERT is the hardest state to trigger because:**
1. It's a "middle ground" between CALM and RISK
2. The model tends to prefer CALM (safer) or RISK (more extreme)
3. Even with ALERT-like signals, it often predicts CALM with ALERT as second choice

**What to look for when testing ALERT:**
- Don't just look at the final predicted state
- Check the **probability bar chart** - ALERT should be the **second-highest bar** (34-36%)
- This shows the model recognizes alert conditions even if it doesn't predict ALERT as final state
- The light bulb may show CALM, but the probability distribution tells the real story

---

## 📝 Notes

- The dashboard uses dropdowns, so select the closest available values
- If exact values aren't available, use the closest option
- The model is more sensitive to combined signals than single signal types
- Probability distributions are more informative than just the final state prediction

