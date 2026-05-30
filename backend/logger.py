"""
Logging configuration for MNIST Classifier API.
Provides structured logging for debugging and monitoring.
"""

import logging
import logging.handlers
from config import config
from typing import Optional

def setup_logger(name: str, log_file: Optional[str] = None) -> logging.Logger:
    """
    Setup and configure logger with both file and console handlers.
    
    Args:
        name: Logger name (typically __name__)
        log_file: Optional file path for logging
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, config.LOG_LEVEL))
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, config.LOG_LEVEL))
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (if specified)
    if log_file or config.LOG_FILE:
        file_path = log_file or config.LOG_FILE
        try:
            file_handler = logging.handlers.RotatingFileHandler(
                file_path,
                maxBytes=10485760,  # 10MB
                backupCount=5
            )
            file_handler.setLevel(getattr(logging, config.LOG_LEVEL))
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        except Exception as e:
            logger.warning(f"Could not setup file logging: {e}")
    
    return logger


# Create module-level logger
logger = setup_logger(__name__)


def log_request(method: str, path: str, status_code: int, duration: float):
    """Log HTTP request details."""
    logger.info(f"{method} {path} - {status_code} - {duration:.3f}s")


def log_prediction(digit: int, confidence: float, model: str):
    """Log prediction details."""
    logger.info(f"Prediction: digit={digit}, confidence={confidence:.4f}, model={model}")


def log_error(error_type: str, message: str, details: Optional[str] = None):
    """Log error with context."""
    if details:
        logger.error(f"{error_type}: {message} - {details}")
    else:
        logger.error(f"{error_type}: {message}")
