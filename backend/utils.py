"""
Utility functions for MNIST Classifier API.

Provides helper functions for data processing, normalization,
and common operations used throughout the application.
"""

from typing import List, Tuple
import numpy as np


def normalize_pixel_values(pixels: List[float]) -> List[float]:
    """
    Ensure pixel values are in valid range [0.0, 1.0].
    
    Args:
        pixels: List of pixel values
        
    Returns:
        Normalized pixel values
    """
    return [max(0.0, min(1.0, p)) for p in pixels]


def pixel_array_to_image(pixels: List[float], size: Tuple[int, int] = (28, 28)) -> np.ndarray:
    """
    Convert flat pixel array to 2D image array.
    
    Args:
        pixels: List of 784 pixel values
        size: Target image size (default 28x28 for MNIST)
        
    Returns:
        2D numpy array representing the image
    """
    return np.array(pixels).reshape(size)


def image_to_pixel_array(image: np.ndarray) -> List[float]:
    """
    Convert 2D image array to flat pixel list.
    
    Args:
        image: 2D numpy array
        
    Returns:
        Flattened list of pixel values
    """
    return image.flatten().tolist()


def calculate_statistics(pixels: List[float]) -> dict:
    """
    Calculate statistics for a pixel array.
    
    Useful for understanding input characteristics.
    
    Args:
        pixels: List of pixel values
        
    Returns:
        Dictionary with pixel statistics
    """
    arr = np.array(pixels)
    return {
        "mean": float(np.mean(arr)),
        "std": float(np.std(arr)),
        "min": float(np.min(arr)),
        "max": float(np.max(arr)),
        "median": float(np.median(arr)),
    }


def format_confidence_percent(confidence: float) -> str:
    """
    Format confidence score as percentage string.
    
    Args:
        confidence: Confidence value (0.0-1.0)
        
    Returns:
        Formatted percentage string
    """
    return f"{confidence * 100:.2f}%"


def get_top_n_predictions(probabilities: List[float], n: int = 3) -> List[Tuple[int, float]]:
    """
    Get top N predicted digits with highest probability.
    
    Args:
        probabilities: List of 10 probability values
        n: Number of top predictions to return
        
    Returns:
        List of (digit, probability) tuples sorted by probability
    """
    predictions = [(i, p) for i, p in enumerate(probabilities)]
    return sorted(predictions, key=lambda x: x[1], reverse=True)[:n]


def create_prediction_summary(
    digit: int,
    confidence: float,
    probabilities: List[float]
) -> dict:
    """
    Create a summary of prediction results.
    
    Args:
        digit: Predicted digit
        confidence: Confidence score
        probabilities: All probability values
        
    Returns:
        Dictionary with prediction summary
    """
    top_3 = get_top_n_predictions(probabilities, 3)
    
    return {
        "predicted_digit": digit,
        "confidence": confidence,
        "confidence_percent": format_confidence_percent(confidence),
        "top_3_predictions": [
            {"digit": d, "probability": p} for d, p in top_3
        ]
    }
