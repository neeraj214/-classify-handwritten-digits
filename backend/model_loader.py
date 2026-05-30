"""
Model loader module for MNIST Digit Classifier.

Provides functions to load the trained ML model and retrieve model metadata.
Handles model file discovery, validation, and error reporting.
"""

import joblib
import os
from typing import Optional, Tuple
from logger import setup_logger

# Initialize logger
logger = setup_logger(__name__)

# Model paths
MODEL_PATH = os.path.join(os.path.dirname(__file__), 
                          "../mnist-digit-classifier/models/final_model.pkl")
INFO_PATH = os.path.join(os.path.dirname(__file__), 
                         "../mnist-digit-classifier/models/model_info.txt")

# Cache for loaded model
_loaded_model = None
_loaded_model_name = None


def load_model():
    """
    Load the trained MNIST classifier model from disk.
    
    Loads the model from the configured model path using joblib.
    Caches the model in memory for subsequent calls.
    
    Returns:
        Loaded scikit-learn model object
        
    Raises:
        FileNotFoundError: If model file not found
        Exception: If model loading fails
    """
    global _loaded_model
    
    # Return cached model if available
    if _loaded_model is not None:
        logger.debug("Returning cached model instance")
        return _loaded_model
    
    logger.info(f"Loading model from {MODEL_PATH}")
    
    # Check if model exists
    if not os.path.exists(MODEL_PATH):
        error_msg = (
            f"Model not found at {MODEL_PATH}. "
            "Ensure model_info.txt exists in mnist-digit-classifier/models/"
        )
        logger.error(error_msg)
        raise FileNotFoundError(error_msg)
    
    try:
        # Load model
        model = joblib.load(MODEL_PATH)
        _loaded_model = model
        logger.info("Model loaded successfully")
        return model
    
    except Exception as e:
        error_msg = f"Failed to load model: {str(e)}"
        logger.error(error_msg)
        raise Exception(error_msg)


def load_model_name() -> str:
    """
    Load model name/description from metadata file.
    
    Reads model information from model_info.txt if available,
    otherwise returns a default name.
    
    Returns:
        Model name/description string
    """
    global _loaded_model_name
    
    # Return cached name if available
    if _loaded_model_name is not None:
        return _loaded_model_name
    
    logger.info(f"Loading model info from {INFO_PATH}")
    
    if os.path.exists(INFO_PATH):
        try:
            with open(INFO_PATH, "r") as f:
                model_name = f.read().strip()
                _loaded_model_name = model_name
                logger.info(f"Model name: {model_name}")
                return model_name
        except Exception as e:
            logger.warning(f"Could not read model info file: {e}")
    
    default_name = "Final Model (Phase 4)"
    _loaded_model_name = default_name
    return default_name


def get_model_info() -> dict:
    """
    Get comprehensive model information.
    
    Returns:
        Dictionary with model metadata
    """
    return {
        "model_name": load_model_name(),
        "model_path": MODEL_PATH,
        "model_exists": os.path.exists(MODEL_PATH),
        "model_size_mb": round(os.path.getsize(MODEL_PATH) / 1024 / 1024, 2) if os.path.exists(MODEL_PATH) else 0
    }


def reload_model():
    """Force reload the model from disk (clear cache)."""
    global _loaded_model, _loaded_model_name
    _loaded_model = None
    _loaded_model_name = None
    logger.info("Model cache cleared, will reload on next use")
    return load_model()
