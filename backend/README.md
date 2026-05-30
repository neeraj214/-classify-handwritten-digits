# Backend Setup & Configuration Guide

## Overview

The MNIST Digit Classifier backend is built with **FastAPI** and provides REST API endpoints for digit classification. This guide covers setup, configuration, and operation.

## Quick Start

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment

Create a `.env` file in the backend directory (optional, uses defaults if not provided):

```bash
cp .env.example .env
```

Edit `.env` to customize settings:

```ini
API_PORT=8000
DEBUG=True
LOG_LEVEL=INFO
MODEL_TYPE=final
ENABLE_CACHE=True
```

### 3. Start the API Server

```bash
# Development mode with auto-reload
python -m uvicorn main:app --reload

# Production mode
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`

## API Endpoints

### Health Check

```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "model_name": "Final Model (Phase 4)"
}
```

### Get API Info

```bash
curl http://localhost:8000/
```

### Make Prediction

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "pixels": [0.0, 0.1, ..., 0.9]  # 784 values, 0.0-1.0
  }'
```

Response:
```json
{
  "predicted_digit": 7,
  "confidence": 0.9823,
  "all_probabilities": [0.001, 0.002, ...],
  "model_used": "Final Model (Phase 4)"
}
```

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `API_HOST` | 0.0.0.0 | API host address |
| `API_PORT` | 8000 | API port number |
| `API_RELOAD` | True | Auto-reload on code changes |
| `DEBUG` | True | Debug mode |
| `MODEL_TYPE` | final | Model to use (final, best, baseline) |
| `MODEL_PATH` | ./models/final_model.pkl | Path to model file |
| `CORS_ORIGINS` | * | CORS allowed origins |
| `LOG_LEVEL` | INFO | Logging level (DEBUG, INFO, WARNING, ERROR) |
| `LOG_FILE` | api.log | Log file path |
| `RATE_LIMIT_ENABLED` | True | Enable rate limiting |
| `ENABLE_CACHE` | True | Enable result caching |

### Module Structure

```
backend/
├── main.py              # FastAPI application
├── config.py            # Configuration management
├── logger.py            # Logging configuration
├── validators.py        # Input validation
├── errors.py            # Error handling
├── model_loader.py      # Model loading
├── utils.py             # Utility functions
├── test_api.py          # API testing script
├── requirements.txt     # Python dependencies
└── .env.example         # Environment template
```

## Testing

### Run API Tests

```bash
python test_api.py
```

### Manual Testing with cURL

```bash
# Create a test image (784 zeros with center pixel = 1.0)
pixels=$(python -c "print([0.0]*384 + [1.0] + [0.0]*399)")
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d "{\"pixels\": $pixels}"
```

## Development

### Adding New Endpoints

1. Import required modules in `main.py`
2. Define request/response Pydantic models
3. Create endpoint function with docstring
4. Add tags for API documentation
5. Use logging for debugging

Example:

```python
@app.post("/debug/validate", tags=["Debug"])
def validate_input(request: PredictRequest):
    """Validate input without making prediction."""
    is_valid, error_msg = validate_pixel_array(request.pixels)
    return {"valid": is_valid, "error": error_msg}
```

### Adding Validation Rules

Edit `validators.py` to add custom validation:

```python
def validate_custom_rule(pixels):
    # Your validation logic
    return is_valid, error_message
```

Then use in endpoints:

```python
is_valid, msg = validate_custom_rule(pixels)
if not is_valid:
    raise HTTPException(status_code=400, detail=msg)
```

## Logging

Logs are written to:
- **Console**: Real-time output during development
- **File**: Configured in `.env` (default: `api.log`)

Log levels:
- `DEBUG`: Detailed diagnostic information
- `INFO`: Confirmation that things are working
- `WARNING`: Unexpected events
- `ERROR`: Serious problems

## Troubleshooting

### Model Not Found

```
FileNotFoundError: Model not found at ...
```

**Solution**: Ensure `mnist-digit-classifier/models/final_model.pkl` exists

### CORS Errors

**Solution**: Check CORS configuration in `.env`:
```ini
CORS_ORIGINS=*
CORS_CREDENTIALS=True
```

### Port Already in Use

```bash
# Use different port
python -m uvicorn main:app --port 8001
```

## Performance Tips

1. **Enable Caching**: Set `ENABLE_CACHE=True` in `.env`
2. **Batch Predictions**: Send multiple predictions in succession
3. **Use Production Mode**: Remove `--reload` flag in production
4. **Monitor Logs**: Check `api.log` for performance issues

## Security

For production deployment:

1. Set `DEBUG=False`
2. Configure specific CORS origins instead of `*`
3. Enable rate limiting
4. Use HTTPS
5. Monitor logs for suspicious activity
6. Keep dependencies updated

## Next Steps

- [Frontend Integration Guide](../FRONTEND_INTEGRATION.md)
- [Model Performance Report](../MODEL_PERFORMANCE.md)
