/**
 * Frontend Constants
 * Centralized constants for the MNIST Digit Classifier UI
 */

// Canvas Configuration
export const CANVAS_CONFIG = {
  WIDTH: 280,
  HEIGHT: 280,
  LINE_WIDTH: 10,
  LINE_COLOR: "#FFFFFF",
  BACKGROUND_COLOR: "#000000",
  MODEL_SIZE: 28, // MNIST is 28x28
};

// Digit Information
export const DIGIT_NAMES = {
  0: "Zero",
  1: "One",
  2: "Two",
  3: "Three",
  4: "Four",
  5: "Five",
  6: "Six",
  7: "Seven",
  8: "Eight",
  9: "Nine",
};

// UI Messages
export const MESSAGES = {
  DRAW_DIGIT: "Draw a digit (0-9)",
  DRAWING_HINT: "Use your mouse to draw",
  LOADING: "Analyzing your drawing...",
  ERROR_BACKEND: "Cannot connect to backend. Make sure the API is running.",
  ERROR_INVALID_INPUT: "Invalid input for prediction",
  ERROR_GENERIC: "An error occurred. Please try again.",
  SUCCESS: "Prediction successful!",
  CLEAR_DRAWING: "Drawing cleared",
  API_ERROR_TIMEOUT: "Request timeout. Backend is not responding.",
  API_ERROR_NETWORK: "Network error. Please check your connection.",
};

// Confidence Thresholds
export const CONFIDENCE_LEVELS = {
  HIGH: 0.85,      // >= 85%
  MEDIUM: 0.70,    // >= 70%
  LOW: 0.50,       // >= 50%
  VERY_LOW: 0.0,   // < 50%
};

// Colors for UI
export const UI_COLORS = {
  SUCCESS: "#10b981",  // Green
  WARNING: "#f59e0b",  // Amber
  ERROR: "#ef4444",    // Red
  INFO: "#3b82f6",     // Blue
  NEUTRAL: "#6b7280",  // Gray
};

// Confidence Color Mapping
export function getConfidenceColor(confidence) {
  if (confidence >= CONFIDENCE_LEVELS.HIGH) {
    return UI_COLORS.SUCCESS;
  } else if (confidence >= CONFIDENCE_LEVELS.MEDIUM) {
    return UI_COLORS.WARNING;
  } else if (confidence >= CONFIDENCE_LEVELS.LOW) {
    return UI_COLORS.INFO;
  } else {
    return UI_COLORS.NEUTRAL;
  }
}

// API Timeouts and Retries
export const API_CONFIG = {
  TIMEOUT: 30000,     // 30 seconds
  RETRY_ATTEMPTS: 3,
  RETRY_DELAY: 1000,  // 1 second
  HEALTH_CHECK_INTERVAL: 5000, // 5 seconds
};

// Animation Durations
export const ANIMATIONS = {
  FADE_IN: 300,
  FADE_OUT: 200,
  SLIDE_IN: 400,
  BUTTON_HOVER: 150,
};

// Accessibility
export const A11Y = {
  BUTTON_FOCUS_OUTLINE: "2px solid #3b82f6",
  BUTTON_FOCUS_OFFSET: "2px",
  MIN_TOUCH_TARGET: 44, // Minimum touch target size in pixels
};

// Development
export const DEV_CONFIG = {
  LOG_API_CALLS: true,
  LOG_CANVAS_OPERATIONS: false,
  SHOW_DEBUG_INFO: false,
};
