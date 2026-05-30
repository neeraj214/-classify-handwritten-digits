"""
Input validation utilities for MNIST Classifier API.
Provides functions to validate and sanitize user inputs.
"""

from typing import List, Tuple
from config import config
from logger import logger, log_error


class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass


def validate_pixel_array(pixels: List[float]) -> Tuple[bool, str]:
    """
    Validate pixel array for MNIST input.
    
    Args:
        pixels: List of pixel values
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Check if pixels is a list
    if not isinstance(pixels, list):
        return False, "Pixels must be a list"
    
    # Check length
    if len(pixels) != config.EXPECTED_PIXEL_COUNT:
        return False, f"Expected {config.EXPECTED_PIXEL_COUNT} pixels, got {len(pixels)}"
    
    # Check each pixel value
    for i, pixel in enumerate(pixels):
        if not isinstance(pixel, (int, float)):
            return False, f"Pixel at index {i} is not a number: {pixel}"
        
        if pixel < config.MIN_PIXEL_VALUE or pixel > config.MAX_PIXEL_VALUE:
            return False, f"Pixel at index {i} is out of range [0.0, 1.0]: {pixel}"
    
    return True, "Valid"


def validate_and_normalize_pixels(pixels: List[float]) -> Tuple[List[float], str]:
    """
    Validate and normalize pixel array.
    
    Args:
        pixels: Raw pixel values
        
    Returns:
        Tuple of (normalized_pixels, error_message or empty string)
    """
    is_valid, error_msg = validate_pixel_array(pixels)
    
    if not is_valid:
        log_error("VALIDATION_ERROR", error_msg)
        return [], error_msg
    
    # Ensure all values are floats
    normalized = [float(p) for p in pixels]
    
    return normalized, ""


def validate_model_type(model_type: str) -> bool:
    """
    Validate that requested model type is supported.
    
    Args:
        model_type: Model identifier
        
    Returns:
        True if model type is valid
    """
    valid_models = ["final", "best", "baseline"]
    return model_type.lower() in valid_models


def sanitize_string(value: str, max_length: int = 255) -> str:
    """
    Sanitize string input.
    
    Args:
        value: String to sanitize
        max_length: Maximum allowed length
        
    Returns:
        Sanitized string
    """
    if not isinstance(value, str):
        return ""
    
    # Strip whitespace and truncate
    return value.strip()[:max_length]
