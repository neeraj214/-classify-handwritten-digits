# Frontend Integration Guide - MNIST Digit Classifier

## Quick Start

### 1. Start the Backend API

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

API will be available at: `http://localhost:8000`

### 2. Frontend Requirements

Your frontend application needs to:
- Send 784 normalized pixel values (0.0-1.0) as a JSON payload
- Handle the prediction response with confidence score and digit prediction
- Display results to the user

## API Endpoints

### Base URL
```
http://localhost:8000
```

### Health Check
```
GET /health

Response:
{
  "status": "ok",
  "model_loaded": true
}
```

### Get Model Info
```
GET /

Response:
{
  "message": "MNIST Classifier API is running",
  "model": "Final Model (Phase 4)"
}
```

### Make Prediction
```
POST /predict
Content-Type: application/json

Request Body:
{
  "pixels": [array of 784 floats between 0.0 and 1.0]
}

Response:
{
  "predicted_digit": 7,
  "confidence": 0.9823,
  "all_probabilities": [0.001, 0.002, ..., 0.9823],
  "model_used": "Final Model (Phase 4)"
}
```

## Integration Examples

### JavaScript/React Example

```javascript
async function predictDigit(pixelArray) {
  const response = await fetch('http://localhost:8000/predict', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      pixels: pixelArray  // Array of 784 values (0.0-1.0)
    })
  });
  
  const prediction = await response.json();
  console.log(`Predicted digit: ${prediction.predicted_digit}`);
  console.log(`Confidence: ${(prediction.confidence * 100).toFixed(2)}%`);
  
  return prediction;
}

// Usage with canvas
function captureDrawing(canvas) {
  const ctx = canvas.getContext('2d');
  const imageData = ctx.getImageData(0, 0, 28, 28);
  const pixels = [];
  
  // Convert to grayscale and normalize
  for (let i = 0; i < imageData.data.length; i += 4) {
    const gray = (imageData.data[i] + imageData.data[i+1] + imageData.data[i+2]) / 3;
    pixels.push(gray / 255); // Normalize to 0.0-1.0
  }
  
  return predictDigit(pixels);
}
```

### Python Example

```python
import requests
import numpy as np

def predict_digit(pixels):
    """
    Make prediction via API
    
    Args:
        pixels: List of 784 floats (0.0-1.0)
    
    Returns:
        dict: Prediction response
    """
    response = requests.post(
        'http://localhost:8000/predict',
        json={'pixels': pixels}
    )
    return response.json()

# Example usage
sample_pixels = np.random.rand(784).tolist()
result = predict_digit(sample_pixels)

print(f"Predicted: {result['predicted_digit']}")
print(f"Confidence: {result['confidence']:.2%}")
```

## Canvas to Prediction Pipeline

### 1. Canvas Setup (28×28 pixels)
```javascript
const canvas = document.createElement('canvas');
canvas.width = 28;
canvas.height = 28;
const ctx = canvas.getContext('2d');
// User draws on canvas...
```

### 2. Extract Pixel Data
```javascript
function getPixelsFromCanvas(canvas) {
  const imageData = canvas.getContext('2d').getImageData(0, 0, 28, 28);
  const pixels = [];
  
  for (let i = 0; i < imageData.data.length; i += 4) {
    // Average RGB channels for grayscale
    const r = imageData.data[i];
    const g = imageData.data[i + 1];
    const b = imageData.data[i + 2];
    const gray = (r + g + b) / 3;
    
    // Normalize to 0.0-1.0
    pixels.push(gray / 255);
  }
  
  return pixels;
}
```

### 3. Send to API
```javascript
const pixels = getPixelsFromCanvas(canvas);
const prediction = await predictDigit(pixels);
displayResult(prediction);
```

## CORS Configuration

The API is configured with CORS enabled for all origins. If you need to restrict it:

Edit `backend/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)
```

## Testing the API

### Using curl
```bash
# Health check
curl http://localhost:8000/health

# Model info
curl http://localhost:8000/

# Make prediction with random pixels
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"pixels": [0.1, 0.2, 0.3, ..., 0.9]}'
```

### Using the test script
```bash
cd backend
python test_api.py
```

## Error Handling

### Common Errors and Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| 400 - "Expected 784 pixels" | Wrong number of values | Ensure exactly 784 pixel values |
| 422 - "Invalid request body" | Wrong JSON format | Check JSON structure: `{"pixels": [...]}` |
| 500 - "Model not found" | Model file missing | Run Phase 4 notebook or check models/ directory |
| Connection refused | API not running | Start API with `uvicorn main:app --reload` |

## Performance Metrics

- **Average Inference Time**: ~5-10ms per prediction
- **Memory Usage**: ~500MB (model in memory)
- **Throughput**: ~100-200 predictions/second on standard hardware
- **Model Size**: 33MB (loaded once at startup)

## Deployment Considerations

### Local Development
```bash
python -m uvicorn main:app --reload
```

### Production (Gunicorn + Uvicorn)
```bash
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Docker (Optional)
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Next Steps

1. ✅ Verify API is running
2. ✅ Test with sample requests
3. ✅ Build canvas drawing interface
4. ✅ Implement prediction display
5. ✅ Deploy to production environment
