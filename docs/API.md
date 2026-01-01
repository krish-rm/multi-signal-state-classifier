# API Documentation

Complete API reference for the Multi-Signal State Classifier.

## Base URL

- **Local**: `http://localhost:8000`
- **Production**: Configure based on deployment

## Interactive Documentation

Visit `http://localhost:8000/docs` for Swagger UI interactive documentation.

## Endpoints

### POST `/predict`

Single prediction endpoint.

**Request:**
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
  },
  "request_id": "optional-request-id"
}
```

**Response:**
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
  "timestamp": "2025-01-15T10:30:00Z",
  "request_id": "optional-request-id"
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
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
  }'
```

---

### POST `/predict/batch`

Batch prediction endpoint for multiple samples.

**Request:**
```json
[
  {
    "timestamp": "2025-01-15T10:30:00Z",
    "signals": {
      "trading": { ... },
      "plant_health": { ... }
    }
  },
  {
    "timestamp": "2025-01-15T11:30:00Z",
    "signals": {
      "trading": { ... },
      "plant_health": { ... }
    }
  }
]
```

**Response:**
```json
[
  {
    "state": "calm",
    "confidence": 0.87,
    "probabilities": { ... },
    "lighting_control": { ... },
    "model_version": "1.0.0",
    "inference_time_ms": 45.2,
    "timestamp": "2025-01-15T10:30:00Z"
  },
  {
    "state": "alert",
    "confidence": 0.75,
    "probabilities": { ... },
    "lighting_control": { ... },
    "model_version": "1.0.0",
    "inference_time_ms": 48.1,
    "timestamp": "2025-01-15T11:30:00Z"
  }
]
```

---

### GET `/health`

Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "predictions_served": 42,
  "uptime_seconds": 3600.5,
  "timestamp": "2025-01-15T10:30:00Z"
}
```

**Example:**
```bash
curl http://localhost:8000/health
```

---

### GET `/metrics`

Performance metrics endpoint.

**Response:**
```json
{
  "total_predictions": 100,
  "total_errors": 2,
  "average_latency_ms": 45.3,
  "uptime_seconds": 7200.0,
  "timestamp": "2025-01-15T10:30:00Z"
}
```

**Example:**
```bash
curl http://localhost:8000/metrics
```

---

### GET `/lighting-info/{state}`

Get lighting configuration for a specific state.

**Path Parameters:**
- `state`: One of `calm`, `alert`, `risk`, `flow`, `deviation`

**Response:**
```json
{
  "state": "calm",
  "lighting_config": {
    "color_temperature": 3000,
    "brightness": 50,
    "pattern": "steady",
    "description": "Stable state - no action needed",
    "urgency": "low"
  },
  "description": "Stable state - no action needed (Medium brightness) - Steady, stable lighting"
}
```

**Example:**
```bash
curl http://localhost:8000/lighting-info/calm
```

---

### GET `/info`

Get API information.

**Response:**
```json
{
  "name": "Multi-Signal State Classifier API",
  "version": "1.0.0",
  "description": "ML pipeline for multi-source signal fusion",
  "states": ["calm", "alert", "risk", "flow", "deviation"],
  "endpoints": {
    "predict": "POST /predict",
    "batch_predict": "POST /predict/batch",
    "health": "GET /health",
    "metrics": "GET /metrics",
    "lighting_info": "GET /lighting-info/{state}",
    "docs": "GET /docs"
  }
}
```

---

### GET `/docs`

Swagger UI interactive documentation.

Open in browser: `http://localhost:8000/docs`

---

## Request/Response Models

### Trading Signals

```json
{
  "price_change": 0.02,      // float: Price movement percentage
  "volatility": 0.15,        // float: Volatility indicator
  "volume": 1000000,          // float: Trading volume
  "rsi": 65.5                 // float (optional): RSI (0-100)
}
```

### Plant Health Signals

```json
{
  "soil_moisture": 0.65,     // float: Moisture level (0-1)
  "temperature": 22.5,        // float: Temperature in Celsius
  "stress_score": 0.3         // float (optional): Stress indicator (0-1)
}
```

### Lighting Control

```json
{
  "color_temperature": 3000,  // int: Color temperature in Kelvin
  "brightness": 50,           // int: Brightness percentage (0-100)
  "pattern": "steady",        // string: Lighting pattern
  "description": "...",       // string: Human-readable description
  "urgency": "low"           // string: Urgency level
}
```

---

## States

| State | Meaning | Lighting |
|-------|---------|----------|
| **calm** | System stable, no action | 3000K, 50%, steady |
| **alert** | Attention required | 4000K, 70%, gentle pulsing |
| **risk** | Problem detected | 2000K, 85%, urgent pulsing |
| **flow** | Everything optimal | 5000K, 80%, steady smooth |
| **deviation** | Anomaly present | Variable, 60-90%, flashing |

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Invalid state. Must be one of ['calm', 'alert', 'risk', 'flow', 'deviation']"
}
```

### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "signals", "trading", "price_change"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

### 500 Internal Server Error
```json
{
  "detail": "Error message describing the issue"
}
```

### 503 Service Unavailable
```json
{
  "detail": "Model not loaded. Service unavailable."
}
```

---

## Rate Limiting

Currently no rate limiting is implemented. For production, consider:
- API key authentication
- Rate limiting (e.g., 100 requests/minute)
- Request throttling

---

## Performance

- **Average Latency**: <50ms
- **P95 Latency**: <100ms
- **Throughput**: >100 requests/second
- **Model Loading**: ~2-3 seconds on startup

---

## Authentication

Currently no authentication is required. For production:
- Add API key/token authentication
- Implement OAuth2 if needed
- Use HTTPS/SSL

---

## Versioning

Current API version: **1.0.0**

Version is included in all responses. Future versions may include versioning in the URL path (e.g., `/v1/predict`).

---

## Support

For API issues:
1. Check the [Troubleshooting Guide](TROUBLESHOOTING.md)
2. Review the [Deployment Guide](DEPLOYMENT.md)
3. Check server logs
4. Verify model is loaded: `GET /health`

