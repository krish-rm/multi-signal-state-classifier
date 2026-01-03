# Deployment Guide

Comprehensive guide for deploying the Multi-Signal State Classifier as a production-ready service.

## Table of Contents

1. [Local Development](#local-development)
2. [Docker Deployment](#docker-deployment)
3. [Docker Compose](#docker-compose)
4. [Testing & Validation](#testing--validation)
5. [Monitoring & Logging](#monitoring--logging)
6. [Advanced Deployment](#advanced-deployment)
7. [Production Checklist](#production-checklist)
8. [Security Considerations](#security-considerations)

---

## Local Development

### Prerequisites

- Python 3.10+
- pip package manager
- Virtual environment (recommended)

### Setup Steps

```bash
# 1. Clone repository
git clone <your-repo-url>
cd multi-signal-state-classifier

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Generate initial data and train model
python train.py

# 5. Run tests
pytest tests/ -v --cov=src

# 6. Start API server
uvicorn src.api.predict_api:app --reload --port 8000
```

### Verify Installation

Navigate to `http://localhost:8000/docs` to see the interactive API documentation.

---

## Docker Deployment

### Prerequisites

**Important**: Before building the Docker image, ensure you have:
1. Trained the model: `python train.py` (creates `models/ensemble_model.pkl` and `models/feature_pipeline.pkl`)
2. Docker and Docker Compose installed
3. Models directory exists with trained model files

### Build Docker Image

```bash
# Build the image
docker build -t multi-signal-classifier:latest .

# Verify build
docker images | grep multi-signal-classifier
```

### Run Docker Container

```bash
# Run container
docker run -p 8000:8000 \
  -e MODEL_PATH=/app/models/ensemble_model.pkl \
  -e LOG_LEVEL=INFO \
  -v $(pwd)/models:/app/models \
  -v $(pwd)/logs:/app/logs \
  multi-signal-classifier:latest

# Check if container is running
curl http://localhost:8000/health
```

### Docker Flags Explained

- `-p 8000:8000`: Map port 8000 from container to host
- `-e KEY=VALUE`: Set environment variables
- `-v HOST:CONTAINER`: Mount volumes
- `--name`: Give container a friendly name
- `-d`: Run in detached mode (background)

### Example with All Options

```bash
docker run \
  --name ml-classifier \
  -p 8000:8000 \
  -e MODEL_PATH=/app/models/ensemble_model.pkl \
  -e LOG_LEVEL=INFO \
  -v $(pwd)/models:/app/models \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/logs:/app/logs \
  -d \
  multi-signal-classifier:latest
```

---

## Docker Compose

### Start Services

```bash
# Start all services
docker-compose up

# Start in background
docker-compose up -d

# View logs
docker-compose logs -f api

# Stop services
docker-compose down
```

### Configuration

The `docker-compose.yml` file defines:
- API service running on port 8000
- Volume mounts for models, data, and logs
- Health checks
- Network configuration

### Custom Compose File

```bash
# Use alternative compose file
docker-compose -f docker-compose.prod.yml up

# Override settings
docker-compose -f docker-compose.yml \
  -e API_PORT=9000 up
```

---

## Testing & Validation

### Health Checks

```bash
# Health check endpoint
curl http://localhost:8000/health

# Expected response:
# {
#   "status": "healthy",
#   "model_loaded": true,
#   "predictions_served": 0,
#   "uptime_seconds": 1.23,
#   "timestamp": "2025-01-15T10:30:00Z"
# }
```

### Test Predictions

```bash
# Single prediction
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

### Performance Testing

```bash
# Load testing with Apache Bench
ab -n 1000 -c 10 http://localhost:8000/health

# Load testing with wrk
wrk -t12 -c400 -d30s http://localhost:8000/health
```

---

## Monitoring & Logging

### Viewing Logs

```bash
# Docker container logs
docker logs ml-classifier
docker logs -f ml-classifier  # Follow logs

# Local logs
tail -f logs/ml_classifier.log

# With grep
docker logs ml-classifier | grep ERROR
```

### Metrics Endpoint

```bash
curl http://localhost:8000/metrics

# Response includes:
# - Total predictions served
# - Error count
# - Average latency
# - Uptime
```

### Prometheus Metrics

To expose Prometheus metrics, add to API:

```python
from prometheus_client import Counter, Histogram

prediction_counter = Counter('predictions_total', 'Total predictions')
prediction_latency = Histogram('prediction_latency_seconds', 'Prediction latency')
```

## Monitoring Best Practices

1. **Log Aggregation**: Use ELK stack or similar
2. **Metrics Collection**: Use Prometheus
3. **Alerting**: Set up alerts for failures
4. **Health Checks**: Regular endpoint monitoring
5. **Performance Tracking**: Monitor latency and throughput

---

## Advanced Deployment

### Kubernetes

```bash
# Create deployment
kubectl apply -f k8s/deployment.yaml

# Expose service
kubectl apply -f k8s/service.yaml

# Scale replicas
kubectl scale deployment ml-classifier --replicas=3
```

### Cloud Platforms

#### AWS
```bash
# Push to ECR
aws ecr get-login-password | docker login --username AWS --password-stdin <ACCOUNT>.dkr.ecr.us-east-1.amazonaws.com
docker tag multi-signal-classifier:latest <ACCOUNT>.dkr.ecr.us-east-1.amazonaws.com/ml-classifier:latest
docker push <ACCOUNT>.dkr.ecr.us-east-1.amazonaws.com/ml-classifier:latest
```

#### GCP
```bash
# Push to GCR
docker tag multi-signal-classifier gcr.io/PROJECT_ID/ml-classifier
docker push gcr.io/PROJECT_ID/ml-classifier
```

#### Azure
```bash
# Push to ACR
az acr login --name myregistry
docker tag multi-signal-classifier myregistry.azurecr.io/ml-classifier
docker push myregistry.azurecr.io/ml-classifier
```

---

## Production Checklist

- [ ] Model trained and validated
- [ ] All tests passing (>80% coverage)
- [ ] Docker image built and tested
- [ ] Environment variables configured
- [ ] Volume mounts set up
- [ ] Health checks working
- [ ] Logging configured
- [ ] Monitoring set up
- [ ] Backup strategy in place
- [ ] Documentation updated
- [ ] Security review completed
- [ ] Load testing done

---

## Security Considerations

1. **API Security**:
   - Use API keys/tokens
   - Enable HTTPS/SSL
   - Rate limiting
   - Input validation

2. **Container Security**:
   - Use specific Python version
   - Minimal base image
   - Scan for vulnerabilities
   - Run as non-root user

3. **Data Security**:
   - Encrypt model files
   - Secure model storage
   - Access control
   - Audit logging

---

## Performance Optimization

1. **Use GPU** (if available):
   ```bash
   docker run --gpus all ...
   ```

2. **Increase workers**:
   ```bash
   uvicorn src.api.predict_api:app --workers 4
   ```

3. **Enable caching**:
   ```bash
   # Use Redis for caching predictions
   ```

4. **Optimize model**:
   - Use ONNX runtime
   - Quantize model
   - Reduce feature count

---

## Support & Maintenance

For issues or questions:
1. Check the [Troubleshooting Guide](TROUBLESHOOTING.md)
2. Review logs: `docker logs ml-classifier`
3. Run tests: `pytest tests/ -v`
4. Check health: `curl http://localhost:8000/health`

---

**Last Updated**: January 2025
**Version**: 1.0.0

