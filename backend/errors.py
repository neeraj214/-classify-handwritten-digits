"""
Error handling utilities for MNIST Classifier API.
Provides custom error classes and error response formatting.
"""

from typing import Dict, Any, Optional
from logger import logger


class APIError(Exception):
    """Base exception for API errors."""
    
    def __init__(self, message: str, status_code: int = 500, details: Optional[str] = None):
        """
        Initialize API error.
        
        Args:
            message: Error message
            status_code: HTTP status code
            details: Additional error details
        """
        self.message = message
        self.status_code = status_code
        self.details = details
        super().__init__(self.message)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert error to dictionary response."""
        response = {
            "error": self.message,
            "status_code": self.status_code,
        }
        if self.details:
            response["details"] = self.details
        return response


class ValidationError(APIError):
    """Raised when input validation fails."""
    
    def __init__(self, message: str, details: Optional[str] = None):
        super().__init__(message, status_code=400, details=details)
        logger.warning(f"Validation error: {message}")


class ModelError(APIError):
    """Raised when model operations fail."""
    
    def __init__(self, message: str, details: Optional[str] = None):
        super().__init__(message, status_code=500, details=details)
        logger.error(f"Model error: {message}")


class NotFoundError(APIError):
    """Raised when resource is not found."""
    
    def __init__(self, message: str, details: Optional[str] = None):
        super().__init__(message, status_code=404, details=details)
        logger.warning(f"Not found: {message}")


class ServerError(APIError):
    """Raised for internal server errors."""
    
    def __init__(self, message: str, details: Optional[str] = None):
        super().__init__(message, status_code=500, details=details)
        logger.error(f"Server error: {message} - {details}")


def create_error_response(error: Exception, include_details: bool = False) -> Dict[str, Any]:
    """
    Create standardized error response from exception.
    
    Args:
        error: Exception instance
        include_details: Whether to include detailed error info
        
    Returns:
        Error response dictionary
    """
    if isinstance(error, APIError):
        response = error.to_dict()
    else:
        response = {
            "error": "An unexpected error occurred",
            "status_code": 500,
        }
        if include_details:
            response["details"] = str(error)
    
    return response


def format_success_response(data: Any, message: str = "Success") -> Dict[str, Any]:
    """
    Format successful response.
    
    Args:
        data: Response data
        message: Success message
        
    Returns:
        Formatted response dictionary
    """
    return {
        "status": "success",
        "message": message,
        "data": data,
    }
