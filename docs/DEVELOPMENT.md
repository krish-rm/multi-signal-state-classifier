# Development Guide

Guide for developers working on the Multi-Signal State Classifier project.

## Table of Contents

1. [Development Setup](#development-setup)
2. [Code Structure](#code-structure)
3. [Testing](#testing)
4. [Code Quality](#code-quality)
5. [Contributing](#contributing)
6. [Best Practices](#best-practices)

---

## Development Setup

### Prerequisites

- Python 3.10+
- Git
- Virtual environment (venv or conda)
- Code editor (VS Code, PyCharm, etc.)

### Initial Setup

```bash
# Clone repository
git clone <your-repo-url>
cd multi-signal-state-classifier

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies (if any)
pip install -r requirements-dev.txt  # If exists

# Run tests to verify setup
pytest tests/ -v
```

---

## Code Structure

### Project Layout

```
multi-signal-state-classifier/
├── src/                    # Source code
│   ├── data/              # Data generation & feature engineering
│   ├── models/            # Model training & prediction
│   └── api/               # FastAPI application
├── tests/                 # Test suite
├── notebooks/             # EDA notebooks
├── docs/                  # Documentation
├── configs/               # Configuration files
├── data/                  # Data storage
├── models/                # Trained models
└── logs/                  # Log files
```

### Key Modules

**`src/data/`**:
- `__init__.py`: Data generation and loading
- `feature_engineering.py`: Feature extraction pipelines

**`src/models/`**:
- `__init__.py`: Model training and ensemble
- `predict.py`: Inference module

**`src/api/`**:
- `predict_api.py`: FastAPI application
- `__init__.py`: Lighting control mapping

---

## Testing

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_models.py -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run specific test
pytest tests/test_api.py::TestAPIPrediction::test_predict_endpoint_structure -v
```

### Test Coverage

**Target**: >80% code coverage

**Current Coverage**:
- Data loading and generation: ✓
- Feature engineering: ✓
- Model training and evaluation: ✓
- API endpoints: ✓
- Integration tests: ✓

### Writing Tests

Follow these guidelines:

1. **Test Structure**:
   ```python
   def test_feature_name(self):
       """Test description."""
       # Arrange
       # Act
       # Assert
   ```

2. **Use Fixtures**: Share common setup in `conftest.py`

3. **Test Isolation**: Each test should be independent

4. **Naming**: Use descriptive test names

### Test Files

- `tests/test_data.py`: Data generation and feature engineering tests
- `tests/test_models.py`: Model training and evaluation tests
- `tests/test_api.py`: API endpoint tests
- `tests/conftest.py`: Shared fixtures and configuration

---

## Code Quality

### Type Hints

All functions should have type hints:

```python
def process_signals(
    trading_data: pd.DataFrame,
    plant_data: pd.DataFrame
) -> pd.DataFrame:
    """Process and combine signals."""
    ...
```

### Docstrings

Use Google-style docstrings:

```python
def train_model(X: np.ndarray, y: np.ndarray) -> Model:
    """
    Train ensemble model.
    
    Args:
        X: Training features
        y: Training labels
    
    Returns:
        Trained model
    """
    ...
```

### Code Formatting

```bash
# Format code with black
black src/ --line-length 88

# Lint code with flake8
flake8 src/ --max-line-length 88

# Type checking with mypy (if configured)
mypy src/
```

### Code Standards

- **PEP 8**: Follow Python style guide
- **Type Hints**: Use type hints on all functions
- **Docstrings**: Document all public functions/classes
- **Error Handling**: Use try/except appropriately
- **Logging**: Use logging instead of print statements

---

## Contributing

### Workflow

1. **Fork Repository**: Create your fork
2. **Create Branch**: `git checkout -b feature/amazing-feature`
3. **Make Changes**: Write code and tests
4. **Run Tests**: `pytest tests/ -v`
5. **Commit**: `git commit -m 'Add amazing feature'`
6. **Push**: `git push origin feature/amazing-feature`
7. **Pull Request**: Open PR with description

### Commit Messages

Use clear, descriptive commit messages:

```
feat: Add batch prediction endpoint
fix: Resolve feature pipeline loading issue
docs: Update API documentation
test: Add tests for new feature
refactor: Improve code structure
```

### Pull Request Guidelines

- Include description of changes
- Reference related issues
- Ensure all tests pass
- Update documentation if needed
- Follow code style guidelines

---

## Best Practices

### Error Handling

```python
try:
    result = process_data(data)
except ValueError as e:
    logger.error(f"Data processing failed: {e}")
    raise HTTPException(status_code=400, detail=str(e))
```

### Logging

```python
import logging

logger = logging.getLogger(__name__)

logger.info("Processing started")
logger.warning("Low confidence prediction")
logger.error("Model loading failed")
```

### Configuration

- Use environment variables for configuration
- Store configs in `configs/` directory
- Document configuration options

### Performance

- Profile code to identify bottlenecks
- Use appropriate data structures
- Optimize feature engineering
- Cache expensive computations

### Security

- Validate all inputs
- Sanitize user data
- Use secure defaults
- Keep dependencies updated

---

## Development Tools

### Recommended Tools

- **IDE**: VS Code or PyCharm
- **Linter**: flake8 or pylint
- **Formatter**: black
- **Type Checker**: mypy
- **Testing**: pytest
- **Version Control**: Git

### VS Code Extensions

- Python
- Pylance
- Black Formatter
- Python Test Explorer
- GitLens

---

## Debugging

### Debug Mode

```bash
# Run API in debug mode
uvicorn src.api.predict_api:app --reload --log-level debug

# Run tests with verbose output
pytest tests/ -v -s

# Use Python debugger
python -m pdb train.py
```

### Common Debugging Steps

1. **Check Logs**: Review error messages
2. **Add Print Statements**: Temporary debugging
3. **Use Debugger**: Set breakpoints in IDE
4. **Test Isolated**: Test functions individually
5. **Verify Data**: Check data shapes and types

---

## Performance Optimization

### Profiling

```python
import cProfile

profiler = cProfile.Profile()
profiler.enable()
# Your code here
profiler.disable()
profiler.print_stats()
```

### Optimization Tips

1. **Vectorization**: Use NumPy/Pandas vectorized operations
2. **Caching**: Cache expensive computations
3. **Lazy Loading**: Load data only when needed
4. **Batch Processing**: Process data in batches
5. **Parallel Processing**: Use multiprocessing for independent tasks

---

## Related Documentation

- [API Documentation](API.md) - API endpoints and usage
- [Data Documentation](DATA.md) - Data structure and generation
- [Deployment Guide](DEPLOYMENT.md) - Deployment instructions
- [Troubleshooting Guide](TROUBLESHOOTING.md) - Common issues and solutions

---

**Last Updated**: January 2025

