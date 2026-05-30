/**
 * API utilities for MNIST Digit Classifier frontend
 * Handles communication with the backend API
 */

// API Configuration
const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";
const REQUEST_TIMEOUT = 30000; // 30 seconds

/**
 * Custom error class for API errors
 */
export class APIError extends Error {
  constructor(message, statusCode, details) {
    super(message);
    this.name = "APIError";
    this.statusCode = statusCode;
    this.details = details;
  }
}

/**
 * Make a fetch request with timeout
 */
async function fetchWithTimeout(url, options = {}) {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), REQUEST_TIMEOUT);

  try {
    const response = await fetch(url, {
      ...options,
      signal: controller.signal,
    });
    clearTimeout(timeoutId);
    return response;
  } catch (error) {
    clearTimeout(timeoutId);
    if (error.name === "AbortError") {
      throw new APIError(
        "Request timeout",
        408,
        `Request exceeded ${REQUEST_TIMEOUT}ms timeout`
      );
    }
    throw error;
  }
}

/**
 * Check if the backend API is running
 * @returns {Promise<boolean>} True if API is healthy
 */
export async function checkHealth() {
  try {
    const response = await fetchWithTimeout(`${BASE_URL}/health`);
    if (!response.ok) {
      return false;
    }
    const data = await response.json();
    return data.status === "healthy" || data.status === "ok";
  } catch (error) {
    console.error("Health check failed:", error);
    return false;
  }
}

/**
 * Get API information and model details
 * @returns {Promise<Object>} API info and model details
 */
export async function getAPIInfo() {
  try {
    const response = await fetchWithTimeout(`${BASE_URL}/`);
    if (!response.ok) {
      throw new APIError(
        "Failed to get API info",
        response.status,
        response.statusText
      );
    }
    return await response.json();
  } catch (error) {
    if (error instanceof APIError) {
      throw error;
    }
    throw new APIError(
      "Failed to get API info",
      0,
      error.message
    );
  }
}

/**
 * Validate pixel array format
 * @param {number[]} pixels - Array of pixel values
 * @returns {Object} Validation result {valid, error}
 */
export function validatePixelArray(pixels) {
  if (!Array.isArray(pixels)) {
    return {
      valid: false,
      error: "Pixels must be an array",
    };
  }

  if (pixels.length !== 784) {
    return {
      valid: false,
      error: `Expected 784 pixels, got ${pixels.length}`,
    };
  }

  for (let i = 0; i < pixels.length; i++) {
    const pixel = pixels[i];
    if (typeof pixel !== "number") {
      return {
        valid: false,
        error: `Pixel at index ${i} is not a number`,
      };
    }
    if (pixel < 0 || pixel > 1) {
      return {
        valid: false,
        error: `Pixel at index ${i} is out of range [0, 1]: ${pixel}`,
      };
    }
  }

  return { valid: true, error: null };
}

/**
 * Predict handwritten digit from pixel array
 * @param {number[]} pixels - Array of 784 normalized pixel values (0-1)
 * @returns {Promise<Object>} Prediction result with digit and confidence
 * @throws {APIError} If prediction fails
 */
export async function predictDigit(pixels) {
  // Validate input
  const validation = validatePixelArray(pixels);
  if (!validation.valid) {
    throw new APIError(
      "Invalid pixel array",
      400,
      validation.error
    );
  }

  try {
    const response = await fetchWithTimeout(`${BASE_URL}/predict`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ pixels }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new APIError(
        data.detail || "Prediction failed",
        response.status,
        data.detail
      );
    }

    return data;
  } catch (error) {
    if (error instanceof APIError) {
      throw error;
    }
    if (error.name === "TypeError" && error.message.includes("Failed to fetch")) {
      throw new APIError(
        "Cannot connect to backend",
        0,
        "Is the backend API running at " + BASE_URL + "?"
      );
    }
    throw new APIError(
      "Prediction failed",
      0,
      error.message
    );
  }
}

/**
 * Format confidence as percentage string
 * @param {number} confidence - Confidence value (0-1)
 * @returns {string} Formatted percentage
 */
export function formatConfidence(confidence) {
  return `${(confidence * 100).toFixed(2)}%`;
}

/**
 * Get API base URL
 * @returns {string} Base URL for API
 */
export function getAPIBaseURL() {
  return BASE_URL;
}

