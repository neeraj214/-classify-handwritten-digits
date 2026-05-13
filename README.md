# MNIST Handwritten Digit Classifier 🎯

A complete machine learning project for classifying handwritten digits using the MNIST dataset. Includes trained models, a production-ready FastAPI backend, and comprehensive documentation for frontend integration.

## 📋 Project Status

| Component | Status | Details |
|-----------|--------|---------|
| **Backend API** | ✅ Complete | FastAPI with model serving |
| **Trained Models** | ✅ Complete | 3 models available (final, best, baseline) |
| **Model Training** | ✅ Complete | 4 Jupyter notebooks with full pipeline |
| **Documentation** | ✅ Complete | Model performance & frontend integration guides |
| **Testing** | ✅ Ready | API test script included |

## 🚀 Quick Start

### Start the API Server
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --reload
```

API available at: `http://localhost:8000`

### Test the API
```bash
python backend/test_api.py
```

### Health Check
```bash
curl http://localhost:8000/health
```

## 📁 Project Structure

```
.
├── backend/                              # FastAPI server
│   ├── main.py                          # API endpoints
│   ├── model_loader.py                  # Model loading logic
│   ├── test_api.py                      # API testing script
│   └── requirements.txt                 # Python dependencies
│
├── mnist-digit-classifier/              # Main training pipeline
│   ├── notebooks/
│   │   ├── 01_data_exploration.ipynb   # Data analysis & visualization
│   │   ├── 02_baseline_model.ipynb     # Decision tree baseline
│   │   └── 03_model_comparison.ipynb   # Model comparison & selection
│   ├── models/                          # Trained model files
│   │   ├── final_model.pkl             # Production model (33MB)
│   │   ├── best_model.pkl              # Alternative variant (33MB)
│   │   ├── decision_tree_baseline.pkl  # Baseline model (1.1MB)
│   │   └── model_info.txt              # Model metadata
│   ├── data/                            # Training visualizations
│   │   ├── sample_digits.png
│   │   ├── confusion_matrix_dt.png
│   │   ├── model_comparison_chart.png
│   │   ├── class_distribution.png
│   │   └── all_confusion_matrices.png
│   └── requirements.txt
│
├── mnist-handwritten-digits/            # Secondary analysis
│   ├── notebooks/
│   │   ├── mnist_exploration.ipynb
│   │   └── hyperparameter_tuning.ipynb
│   ├── src/
│   │   ├── data.py
│   │   ├── model.py
│   │   └── utils.py
│   └── requirements.txt
│
├── MODEL_PERFORMANCE.md                 # Model metrics & specs
├── FRONTEND_INTEGRATION.md              # Integration guide
└── README.md                            # This file
```

## 🤖 Available Models

### Final Model (Production) ⭐
- **File**: `mnist-digit-classifier/models/final_model.pkl`
- **Status**: Active (default in API)
- **Size**: 33MB
- **Use Case**: Production predictions

### Best Model
- **File**: `mnist-digit-classifier/models/best_model.pkl`
- **Size**: 33MB
- **Use Case**: Comparison testing

### Decision Tree Baseline
- **File**: `mnist-digit-classifier/models/decision_tree_baseline.pkl`
- **Size**: 1.1MB
- **Use Case**: Fast inference, baseline comparison

## 🔌 API Endpoints

### GET `/`
Returns API info and loaded model name.

### GET `/health`
Health check endpoint.
```json
{"status": "ok", "model_loaded": true}
```

### POST `/predict`
Make predictions on handwritten digits.

**Request:**
```json
{
  "pixels": [0.1, 0.2, ..., 0.9]  // 784 normalized pixel values (0.0-1.0)
}
```

**Response:**
```json
{
  "predicted_digit": 7,
  "confidence": 0.9823,
  "all_probabilities": [0.001, 0.002, ..., 0.9823],
  "model_used": "Final Model (Phase 4)"
}
```

## 📊 Input Specifications

- **Format**: 28×28 pixel grayscale image
- **Total Features**: 784 (28 × 28)
- **Value Range**: 0.0 - 1.0 (normalized pixel intensities)
- **Data Type**: Array of floats

## 📈 Training Pipeline

### Phase 1: Data Exploration
- Load MNIST dataset
- Visualize sample digits
- Analyze class distribution
- Data preprocessing & normalization

### Phase 2: Baseline Model
- Implement Decision Tree classifier
- Train and evaluate
- Generate confusion matrix
- Establish baseline metrics

### Phase 3: Model Comparison
- Train multiple models (SVM, Random Forest, Neural Networks)
- Compare performance metrics
- Select best model
- Generate comparison charts

### Phase 4: Final Model
- Fine-tune best performing model
- Optimize hyperparameters
- Final evaluation
- Save production model

## 🧪 Testing

### Run API Tests
```bash
cd backend
python test_api.py
```

### Manual Testing with curl
```bash
# Health check
curl http://localhost:8000/health

# Get model info
curl http://localhost:8000/

# Make prediction (with Python)
python backend/test_api.py
```

## 📚 Documentation

- **[MODEL_PERFORMANCE.md](MODEL_PERFORMANCE.md)** - Model specifications, metrics, and performance details
- **[FRONTEND_INTEGRATION.md](FRONTEND_INTEGRATION.md)** - Complete guide for integrating with frontend applications (React, Vue, vanilla JS, etc.)

## 🛠️ Tech Stack

- **Backend**: FastAPI, Uvicorn
- **ML Framework**: scikit-learn
- **Data Processing**: NumPy, Pandas
- **Visualization**: Matplotlib, Seaborn
- **Model Serialization**: Joblib
- **Testing**: requests library

## 📦 Installation

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
```

### Training Setup (Optional)
```bash
cd mnist-digit-classifier
pip install -r requirements.txt
# Run notebooks in order: 01 → 02 → 03
```

## 🚀 Deployment

### Local Development
```bash
cd backend
python -m uvicorn main:app --reload
```

### Production with Gunicorn
```bash
pip install gunicorn
cd backend
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Docker (Coming Soon)
A Dockerfile will be added for containerized deployment.

## 📝 CORS Configuration

The API allows requests from all origins. To restrict to specific domains, edit `backend/main.py`:

```python
allow_origins=["http://localhost:3000", "https://yourdomain.com"]
```

## 🔍 Troubleshooting

| Issue | Solution |
|-------|----------|
| "Model not found" error | Ensure `final_model.pkl` exists in `mnist-digit-classifier/models/` |
| Port 8000 already in use | Use different port: `--port 8001` |
| Module not found errors | Install dependencies: `pip install -r requirements.txt` |
| JSON decode errors | Check pixel array has exactly 784 values between 0.0-1.0 |

## 📖 Learn More

- [MNIST Dataset](http://yann.lecun.com/exdb/mnist/) - Original dataset source
- [scikit-learn Documentation](https://scikit-learn.org/) - ML library
- [FastAPI Documentation](https://fastapi.tiangolo.com/) - API framework

## 👤 Author

Created as a portfolio machine learning project demonstrating:
- Data exploration and visualization
- Model training and evaluation
- Performance comparison and selection
- Production API implementation
- Complete documentation

## 📄 License

This project is open source and available for educational purposes.

---

**Status**: ✅ Ready for production use or frontend integration