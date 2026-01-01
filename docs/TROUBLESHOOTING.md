# Troubleshooting Guide

Common issues and solutions for the Multi-Signal State Classifier.

## Table of Contents

1. [Installation Issues](#installation-issues)
2. [Model Training Issues](#model-training-issues)
3. [API Issues](#api-issues)
4. [Docker Issues](#docker-issues)
5. [Performance Issues](#performance-issues)
6. [Data Issues](#data-issues)

---

## Installation Issues

### Issue: Import errors

```
ModuleNotFoundError: No module named '...'
```

**Solution:**
```bash
# Reinstall dependencies
pip install -r requirements.txt --upgrade

# Ensure virtual environment is activated
source venv/bin/activate  # Windows: venv\Scripts\activate

# Check Python version (requires 3.10+)
python --version
```

### Issue: Package conflicts

```
ERROR: pip's dependency resolver does not currently take into account all the packages that are installed.
```

**Solution:**
```bash
# Create fresh virtual environment
python -m venv venv_new
source venv_new/bin/activate
pip install -r requirements.txt
```

---

## Model Training Issues

### Issue: Model not found

```
ERROR: Model not found at models/ensemble_model.pkl
```

**Solution:**
```bash
# Train model first
python train.py

# Verify model exists
ls -la models/ensemble_model.pkl
ls -la models/feature_pipeline.pkl
```

### Issue: Training fails with memory error

```
ERROR: Cannot allocate memory
```

**Solution:**
```bash
# Reduce sample size in train.py
# Change n_samples=2500 to n_samples=1000

# Or increase system memory
# Close other applications
```

### Issue: Poor model performance

**Solution:**
- Check data quality: `pytest tests/test_data.py -v`
- Verify feature engineering: Review notebooks
- Try different hyperparameters
- Check for data leakage in time-series split

---

## API Issues

### Issue: Port already in use

```
ERROR: Address already in use
```

**Solution:**
```bash
# Find process using port (Linux/Mac)
lsof -i :8000

# Find process using port (Windows)
netstat -ano | findstr :8000

# Kill process
kill -9 <PID>  # Linux/Mac
taskkill /PID <PID> /F  # Windows

# Or use different port
uvicorn src.api.predict_api:app --port 9000
```

### Issue: Model not loaded error

```
503: Model not loaded. Service unavailable.
```

**Solution:**
```bash
# Ensure model files exist
ls -la models/

# Train model if missing
python train.py

# Restart API server
uvicorn src.api.predict_api:app --reload
```

### Issue: Prediction returns wrong state format

```
Response shows "1" instead of "calm"
```

**Solution:**
- This was fixed in recent updates
- Ensure you're using the latest code
- Restart API server after code updates

### Issue: Feature mismatch error

```
X has 7 features, but RandomForestClassifier is expecting 256 features
```

**Solution:**
- This was fixed - feature pipeline is now loaded and used
- Ensure `models/feature_pipeline.pkl` exists
- Restart API server

---

## Docker Issues

### Issue: Docker build fails

```
ERROR: failed to solve: process "/bin/sh -c pip install..." did not complete successfully
```

**Solution:**
```bash
# Check Dockerfile syntax
docker build --no-cache -t multi-signal-classifier .

# Check internet connection
# Verify requirements.txt is valid
```

### Issue: Container exits immediately

```
Container status: Exited (1)
```

**Solution:**
```bash
# Check logs
docker logs <container-id>

# Run interactively to see errors
docker run -it multi-signal-classifier /bin/bash

# Check if model files are mounted correctly
docker run -v $(pwd)/models:/app/models multi-signal-classifier
```

### Issue: Volume mount not working

```
Model not found in container
```

**Solution:**
```bash
# Use absolute paths for volumes (Windows)
docker run -v C:/path/to/models:/app/models ...

# Check volume mount
docker exec <container-id> ls -la /app/models

# Verify host files exist
ls -la models/
```

### Issue: Out of memory

```
ERROR: Cannot allocate memory
```

**Solution:**
```bash
# Check available memory
free -h  # Linux
docker stats  # Docker stats

# Limit container memory
docker run -m 2g ...  # 2GB limit

# Or increase system memory
```

---

## Performance Issues

### Issue: Slow predictions

```
Latency > 100ms
```

**Solution:**
```bash
# Check logs for errors
docker logs ml-classifier

# Monitor resource usage
docker stats

# Check feature engineering performance
# Reduce feature count if needed

# Increase resources
docker run -m 4g --cpus="2" ...
```

### Issue: High memory usage

**Solution:**
- Reduce batch size
- Optimize feature engineering
- Use model quantization
- Increase container memory limits

### Issue: API timeout

**Solution:**
- Check network connectivity
- Verify API is running: `curl http://localhost:8000/health`
- Check server resources
- Review logs for errors

---

## Data Issues

### Issue: Data generation fails

```
ERROR: Data generation error
```

**Solution:**
```bash
# Check Python version (3.10+)
python --version

# Verify numpy/pandas versions
pip list | grep -E "numpy|pandas"

# Try regenerating with different seed
# Edit train.py to change seed
```

### Issue: Feature engineering produces NaN values

**Solution:**
- This should be handled automatically (NaN filled with 0)
- Check data quality: `pytest tests/test_data.py::TestFeaturePipeline::test_no_nan_values`
- Review feature engineering code

### Issue: Data file not found

```
FileNotFoundError: data/processed/unified_signals.parquet
```

**Solution:**
```bash
# Generate data
python train.py

# Or load existing data
# Check data/processed/ directory
```

---

## Debug Commands

### General Debugging

```bash
# Check Python version
python --version

# Check installed packages
pip list

# Run tests
pytest tests/ -v

# Check API health
curl http://localhost:8000/health

# View API logs
# Check console output or logs/ml_classifier.log
```

### Docker Debugging

```bash
# Enter running container
docker exec -it ml-classifier bash

# Check environment
docker exec ml-classifier env

# Run command in container
docker exec ml-classifier python -c "import sys; print(sys.version)"

# View container resources
docker stats

# Inspect container
docker inspect ml-classifier

# View container logs
docker logs -f ml-classifier
```

### API Debugging

```bash
# Test health endpoint
curl http://localhost:8000/health

# Test prediction endpoint
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"signals": {"trading": {...}, "plant_health": {...}}}'

# Check metrics
curl http://localhost:8000/metrics

# View interactive docs
# Open http://localhost:8000/docs in browser
```

---

## Common Error Messages

### "Model not loaded. Service unavailable."
- **Cause**: Model file missing or not loaded
- **Fix**: Train model with `python train.py` and restart API

### "X has 7 features, but model expects 256 features"
- **Cause**: Feature pipeline not being used
- **Fix**: Ensure `models/feature_pipeline.pkl` exists and API is using it (fixed in recent update)

### "Address already in use"
- **Cause**: Port 8000 already in use
- **Fix**: Kill process using port or use different port

### "Cannot allocate memory"
- **Cause**: Insufficient memory
- **Fix**: Close other applications or increase memory limits

### "ModuleNotFoundError"
- **Cause**: Missing dependencies
- **Fix**: `pip install -r requirements.txt`

---

## Getting Help

If you encounter issues not covered here:

1. **Check Logs**: Review error messages in logs
2. **Run Tests**: `pytest tests/ -v` to verify setup
3. **Review Documentation**: 
   - [API Documentation](API.md)
   - [Deployment Guide](DEPLOYMENT.md)
   - [Development Guide](DEVELOPMENT.md)
4. **Check GitHub Issues**: Search for similar problems
5. **Create Issue**: Include:
   - Error message
   - Operating system
   - Python version
   - Steps to reproduce

---

**Last Updated**: January 2025

