"""
MNIST Digit Classifier API - Main FastAPI Application

This module provides REST API endpoints for classifying handwritten digits
using trained machine learning models. It includes:
- Model inference endpoints
- Health checks
- CORS support for frontend integration
- Comprehensive error handling and logging
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
from model_loader import load_model, load_model_name
from config import config
from logger import setup_logger, log_prediction, log_error
from validators import validate_and_normalize_pixels
from errors import ValidationError, ModelError, create_error_response

# Initialize logger
logger = setup_logger(__name__)

# Create FastAPI app
app = FastAPI(
    title="MNIST Digit Classifier API",
    description="API for classifying handwritten digits using MNIST-trained models",
    version="1.0.0"
)

# Configure CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ORIGINS,
    allow_credentials=config.CORS_CREDENTIALS,
    allow_methods=config.CORS_METHODS,
    allow_headers=config.CORS_HEADERS,
)

# Load model once at startup
logger.info("Loading ML model...")
model = load_model()
model_name = load_model_name()
logger.info(f"Model loaded successfully: {model_name}")


class PredictRequest(BaseModel):
    """Request model for digit prediction endpoint.
    
    Attributes:
        pixels: List of 784 normalized pixel values (0.0-1.0)
    """
    pixels: list[float]


class PredictResponse(BaseModel):
    """Response model for digit prediction endpoint.
    
    Attributes:
        predicted_digit: Classified digit (0-9)
        confidence: Confidence score for prediction (0.0-1.0)
        all_probabilities: Probability distribution for all digits
        model_used: Name of the model used for prediction
    """
    predicted_digit: int
    confidence: float
    all_probabilities: list[float]
    model_used: str


class HealthResponse(BaseModel):
    """Response model for health check endpoint."""
    status: str
    model_loaded: bool
    model_name: str


@app.get("/", tags=["Info"])
def root() -> dict:
    """Get API information and model details.
    
    Returns:
        Dictionary containing API status and loaded model information.
    """
    logger.info("API info endpoint accessed")
    return {
        "message": "MNIST Classifier API is running",
        "model": model_name,
        "version": "1.0.0"
    }


@app.get("/health", tags=["Health"], response_model=HealthResponse)
def health() -> dict:
    """Health check endpoint.
    
    Returns:
        Dictionary with API and model health status.
    """
    is_healthy = model is not None
    status = "healthy" if is_healthy else "unhealthy"
    logger.info(f"Health check: {status}")
    
    return {
        "status": status,
        "model_loaded": is_healthy,
        "model_name": model_name
    }


@app.post("/predict", response_model=PredictResponse, tags=["Prediction"])
def predict(request: PredictRequest) -> PredictResponse:
    """Classify a handwritten digit.
    
    Args:
        request: PredictRequest containing 784 normalized pixel values
        
    Returns:
        PredictResponse with digit prediction and confidence
        
    Raises:
        HTTPException: If validation fails or model inference fails
    """
    try:
        # Validate and normalize input
        pixels, error_msg = validate_and_normalize_pixels(request.pixels)
        if error_msg:
            logger.warning(f"Validation failed: {error_msg}")
            raise HTTPException(status_code=400, detail=error_msg)
        
        # Convert to numpy array and reshape for model
        img_array = np.array(pixels, dtype=np.float32).reshape(1, -1)
        
        # Make prediction
        predicted_digit = int(model.predict(img_array)[0])
        
        # Get confidence and probabilities
        if hasattr(model, "predict_proba"):
            proba = model.predict_proba(img_array)[0]
            confidence = float(proba[predicted_digit])
            all_probs = [round(float(p), 4) for p in proba]
        else:
            confidence = 1.0
            all_probs = [0.0] * 10
            all_probs[predicted_digit] = 1.0
        
        # Log prediction
        log_prediction(predicted_digit, confidence, model_name)
        
        return PredictResponse(
            predicted_digit=predicted_digit,
            confidence=round(confidence, 4),
            all_probabilities=all_probs,
            model_used=model_name
        )
    
    except HTTPException:
        raise
    except Exception as e:
        error_msg = f"Prediction failed: {str(e)}"
        log_error("PREDICTION_ERROR", error_msg, str(e))
        raise HTTPException(status_code=500, detail=error_msg)
