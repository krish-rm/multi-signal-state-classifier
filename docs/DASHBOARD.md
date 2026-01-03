# Interactive Dashboard Documentation

Complete guide for the Multi-Signal State Classifier Interactive Visualization Dashboard.

## 🎯 Overview

A beautiful, real-time React dashboard for visualizing multi-signal state classification predictions. Features animated light bulb visualization, probability distribution charts, and seamless API integration.

## 🎯 Features

- **Visual Input Controls**: Icon-based interface with dropdown selectors for all 7 input signals
  - Plant Sensors: Soil Moisture, Temperature, Stress Score
  - Trading Terminal: Price Change, Volatility, Volume, RSI
- **Animated Light Bulb Visualization** with 5 distinct states (calm, alert, risk, flow, deviation)
- **Probability Distribution Chart** showing confidence scores for each state
- **Real-time API Integration** with error handling and health monitoring
- **Loading States** and smooth animations
- **Responsive Design** that works on desktop, tablet, and mobile
- **High Performance** with <100ms prediction display
- **Beautiful Dark Theme** with gradient UI and smooth transitions

## 🚀 Quick Start

### Prerequisites

- Node.js 16+ and npm or yarn
- Python FastAPI server running on `http://localhost:8000` (see main project README)

### Installation

1. Navigate to the dashboard directory:
```bash
cd dashboard
```

2. Install dependencies:
```bash
npm install
```

### Development

Start the development server:
```bash
npm run dev
```

The dashboard will open automatically. The default port is `http://localhost:5173`, but if that port is in use, Vite will automatically use the next available port (e.g., 5174, 5175). Check the terminal output for the exact URL.

### Production Build

Build for production:
```bash
npm run build
```

Output will be in the `dist` folder.

## 📋 Input Signals

### Trading Signals (📈)

The dashboard provides dropdown selectors with preset values for:

- **Price Change (%)**: Percentage change in price
  - Options: Drop (-2.5%), Down (-1.0%), Slight Down (-0.5%), Stable (0%), Slight Rise (+0.02%), Slight Up (+0.5%), Up (+1.0%), Rise (+2.0%)
- **Volatility**: Volatility indicator (0 to 1)
  - Options: Very Low (0.05), Low (0.15), Medium (0.30), High (0.50), Very High (0.75), Extreme (0.90)
- **Volume**: Trading volume in shares
  - Options: Low (500K), Medium (1M), High (2.5M), Very High (5M), Extreme (10M)
- **RSI**: Relative Strength Index (0 to 100)
  - Options: Oversold (20), Low (35), Neutral (50), High (65.5), Overbought (75), Very High (85)

### Plant Health Signals (🌱)

- **Soil Moisture**: Moisture level (0 to 1)
  - Options: Low (15%), Low-Med (30%), Medium (50%), Medium-High (65%), High (80%), Very High (95%)
- **Temperature**: Temperature in Celsius
  - Options: Cool (15°C), Mild (20°C), Optimal (22.5°C), Warm (25°C), Hot (30°C), Very Hot (35°C)
- **Plant Stress Score**: Stress indicator (0 to 1)
  - Options: Low (0.1), Low-Med (0.3), Medium (0.5), High (0.7), Very High (0.9)

## 🎨 State Visualization

The dashboard displays predictions with visual feedback for each state:

| State | Color | Pattern | Meaning |
|-------|-------|---------|---------|
| **Calm** | 🔵 Blue | Steady | System stable, no action needed |
| **Alert** | 🟠 Amber | Gentle Pulsing | Attention required |
| **Risk** | 🔴 Red | Urgent Pulsing | Problem detected |
| **Flow** | 🟢 Green | Smooth Steady | Everything optimal |
| **Deviation** | 🟣 Purple | Flashing | Anomaly present |

## 🏗️ Architecture

```
dashboard/
├── src/
│   ├── components/
│   │   ├── InputForm.jsx              # Input controls & validation
│   │   ├── LightBulbVisualization.jsx # Animated light bulb
│   │   ├── ProbabilityChart.jsx       # Probability distribution chart
│   │   ├── ResultsPanel.jsx           # Prediction results display
│   │   └── ErrorAlert.jsx             # Error messages
│   ├── api/
│   │   └── prediction.js              # API integration
│   ├── App.jsx                        # Main application
│   ├── main.jsx                       # React entry point
│   └── index.css                      # Global styles
├── index.html                         # HTML template
├── package.json                       # Dependencies
├── vite.config.js                     # Vite configuration
└── tailwind.config.js                 # Tailwind CSS configuration
```

## 🔌 API Integration

The dashboard communicates with the FastAPI backend at `http://localhost:8000/predict`.

### Prediction Endpoint

**POST** `/predict`

Request:
```json
{
  "timestamp": "2025-01-15T10:30:00Z",
  "signals": {
    "trading": {
      "price_change": 0.02,
      "volatility": 0.15,
      "volume": 1000000,
      "rsi": 65.5
    },
    "plant_health": {
      "soil_moisture": 0.65,
      "temperature": 22.5,
      "stress_score": 0.3
    }
  }
}
```

Response:
```json
{
  "state": "calm",
  "confidence": 0.87,
  "probabilities": {
    "calm": 0.87,
    "alert": 0.08,
    "risk": 0.03,
    "flow": 0.01,
    "deviation": 0.01
  },
  "lighting_control": {
    "color_temperature": 3000,
    "brightness": 50,
    "pattern": "steady",
    "description": "Stable state - no action needed",
    "urgency": "low"
  },
  "model_version": "1.0.0",
  "inference_time_ms": 45.2,
  "timestamp": "2025-01-15T10:30:00Z"
}
```

## ⚙️ Configuration

### API Server URL

The default API URL is `http://localhost:8000`. To change it, edit `dashboard/src/api/prediction.js`:

```javascript
const API_BASE_URL = 'http://localhost:8000' // Change this
```

### Tailwind Theme

Customize colors and animations in `dashboard/tailwind.config.js`:

```javascript
theme: {
  extend: {
    colors: {
      calm: '#3B82F6',
      alert: '#F59E0B',
      risk: '#EF4444',
      flow: '#10B981',
      deviation: '#8B5CF6',
    }
  }
}
```

## 🧪 Testing

1. Start the FastAPI server:
```bash
# From project root
uvicorn src.api.predict_api:app --reload --port 8000
```

2. Start the dashboard:
```bash
cd dashboard
npm run dev
```

3. Adjust input signals using the dropdown selectors and click "Run Prediction"

4. Verify:
   - ✅ Predictions load in <100ms
   - ✅ Light bulb animates smoothly at 60fps
   - ✅ Probability chart displays correctly
   - ✅ Error messages appear when API is unavailable

## 🎬 Performance Targets

- **Page Load**: <2s
- **Prediction Display**: <100ms
- **Animation**: 60fps smooth
- **API Response**: <100ms

Verified with:
- Chrome DevTools Performance tab
- Lighthouse audit
- Network throttling tests

## 🛠️ Technology Stack

- **React 18**: UI framework
- **Vite**: Build tool & dev server
- **Tailwind CSS**: Styling
- **Recharts**: Charts & graphs
- **Lucide React**: Icons
- **Fetch API**: HTTP requests

## 📱 Browser Support

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Mobile browsers (iOS Safari 14+, Chrome Android 90+)

## 🐛 Troubleshooting

### "Cannot connect to API server"

1. Verify the FastAPI server is running:
```bash
curl http://localhost:8000/health
```

2. Check the API port in `dashboard/src/api/prediction.js`

3. Ensure CORS is enabled on the API (it is in the provided FastAPI setup)

### Page Loading Slowly

1. Check network throttling in DevTools
2. Clear browser cache: Ctrl+Shift+Delete
3. Rebuild: `npm run build`
4. Verify no background processes are consuming resources

### Animations Not Smooth

1. Disable hardware acceleration: DevTools → More Tools → Rendering → Uncheck "Paint flashing"
2. Check CPU usage (may be high on old devices)
3. Reduce browser tabs/background processes

### Predictions Taking Too Long

1. Ensure FastAPI server is responding: `curl http://localhost:8000/metrics`
2. Check server logs for errors
3. Verify network latency: Open DevTools → Network tab

## 🚀 Deployment

### Vercel (Recommended)

1. Push to GitHub
2. Connect repository to Vercel
3. Set environment variable: `VITE_API_URL=https://your-api.example.com`
4. Deploy

### Docker

```dockerfile
FROM node:18-alpine as builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:18-alpine
WORKDIR /app
RUN npm install -g serve
COPY --from=builder /app/dist ./dist
EXPOSE 3000
CMD ["serve", "-s", "dist", "-l", "3000"]
```

### Environment Variables

Create `dashboard/.env.production`:
```
VITE_API_URL=https://your-api-server.com
```

## 📚 Related Documentation

- [Main Project README](../README.md)
- [API Documentation](API.md)
- [Data Documentation](DATA.md)
- [Deployment Guide](DEPLOYMENT.md)
- [Troubleshooting Guide](TROUBLESHOOTING.md)

## 🎯 Future Enhancements

- [ ] WebSocket for real-time updates
- [ ] Historical predictions chart
- [ ] Prediction presets
- [ ] Export results (CSV/PDF)
- [ ] Dark/Light mode toggle
- [ ] Mobile app
- [ ] Analytics dashboard
- [ ] Multi-language support

---

For more information, see the [Main Project README](../README.md) or [Troubleshooting Guide](TROUBLESHOOTING.md).

