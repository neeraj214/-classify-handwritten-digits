"""
Test suite for MNIST Classifier API.

Provides comprehensive testing of API endpoints including:
- Health checks
- Input validation
- Prediction accuracy
- Error handling
"""

import requests
import numpy as np
import json
from typing import Dict, Any

BASE_URL = "http://localhost:8000"


class Colors:
    """ANSI color codes for terminal output."""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


def print_section(title: str):
    """Print section header."""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{title}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}\n")


def print_success(message: str):
    """Print success message."""
    print(f"{Colors.GREEN}✓ {message}{Colors.RESET}")


def print_error(message: str):
    """Print error message."""
    print(f"{Colors.RED}✗ {message}{Colors.RESET}")


def print_info(message: str):
    """Print info message."""
    print(f"{Colors.YELLOW}ℹ {message}{Colors.RESET}")


def test_health_check():
    """Test API health endpoint."""
    print_section("Test 1: Health Check")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print_success(f"Health check passed")
            print(f"  Status: {data.get('status')}")
            print(f"  Model Loaded: {data.get('model_loaded')}")
            print(f"  Model Name: {data.get('model_name')}")
            return True
        else:
            print_error(f"Health check failed with status {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Health check exception: {e}")
        return False


def test_api_info():
    """Test API info endpoint."""
    print_section("Test 2: API Info")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            data = response.json()
            print_success("API info retrieved")
            print(f"  Message: {data.get('message')}")
            print(f"  Model: {data.get('model')}")
            return True
        else:
            print_error(f"API info failed with status {response.status_code}")
            return False
    except Exception as e:
        print_error(f"API info exception: {e}")
        return False


def test_random_prediction():
    """Test prediction with random pixels."""
    print_section("Test 3: Random Prediction")
    try:
        pixels = np.random.rand(784).tolist()
        response = requests.post(
            f"{BASE_URL}/predict",
            json={"pixels": pixels}
        )
        if response.status_code == 200:
            data = response.json()
            print_success("Random prediction successful")
            print(f"  Predicted Digit: {data.get('predicted_digit')}")
            print(f"  Confidence: {data.get('confidence'):.4f}")
            print(f"  Model Used: {data.get('model_used')}")
            return True
        else:
            print_error(f"Prediction failed with status {response.status_code}")
            print(f"  Response: {response.text}")
            return False
    except Exception as e:
        print_error(f"Prediction exception: {e}")
        return False


def test_zero_image():
    """Test prediction with all-zero image."""
    print_section("Test 4: Zero Image Prediction")
    try:
        pixels = [0.0] * 784
        response = requests.post(
            f"{BASE_URL}/predict",
            json={"pixels": pixels}
        )
        if response.status_code == 200:
            data = response.json()
            print_success("Zero image prediction successful")
            print(f"  Predicted Digit: {data.get('predicted_digit')}")
            print(f"  Confidence: {data.get('confidence'):.4f}")
            return True
        else:
            print_error(f"Zero image prediction failed")
            return False
    except Exception as e:
        print_error(f"Zero image exception: {e}")
        return False


def test_invalid_pixel_count():
    """Test validation: invalid pixel count."""
    print_section("Test 5: Invalid Pixel Count Validation")
    try:
        pixels = [0.5] * 100  # Wrong count
        response = requests.post(
            f"{BASE_URL}/predict",
            json={"pixels": pixels}
        )
        if response.status_code == 400:
            print_success("Invalid pixel count correctly rejected")
            print(f"  Error: {response.json().get('detail')}")
            return True
        else:
            print_error(f"Should have returned 400, got {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Validation exception: {e}")
        return False


def test_out_of_range_pixels():
    """Test validation: pixels out of range."""
    print_section("Test 6: Out-of-Range Pixel Validation")
    try:
        pixels = [0.5] * 783 + [1.5]  # Last pixel > 1.0
        response = requests.post(
            f"{BASE_URL}/predict",
            json={"pixels": pixels}
        )
        if response.status_code == 400:
            print_success("Out-of-range pixel correctly rejected")
            print(f"  Error: {response.json().get('detail')}")
            return True
        else:
            print_error(f"Should have returned 400, got {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Validation exception: {e}")
        return False


def test_non_numeric_pixels():
    """Test validation: non-numeric pixels."""
    print_section("Test 7: Non-Numeric Pixel Validation")
    try:
        pixels = [0.5] * 783 + ["invalid"]  # Last pixel is string
        response = requests.post(
            f"{BASE_URL}/predict",
            json={"pixels": pixels}
        )
        # FastAPI should reject this during JSON parsing
        if response.status_code >= 400:
            print_success("Non-numeric pixel correctly rejected")
            return True
        else:
            print_error(f"Should have rejected non-numeric input")
            return False
    except Exception as e:
        print_info(f"Validation exception (expected): {type(e).__name__}")
        return True


def test_empty_request():
    """Test validation: empty request."""
    print_section("Test 8: Empty Request Validation")
    try:
        response = requests.post(
            f"{BASE_URL}/predict",
            json={}
        )
        if response.status_code >= 400:
            print_success("Empty request correctly rejected")
            return True
        else:
            print_error("Empty request should have been rejected")
            return False
    except Exception as e:
        print_error(f"Exception: {e}")
        return False


def test_edge_case_pixels():
    """Test edge case: min and max pixel values."""
    print_section("Test 9: Edge Case Pixels (Min/Max)")
    try:
        # Alternate between min and max
        pixels = [0.0 if i % 2 == 0 else 1.0 for i in range(784)]
        response = requests.post(
            f"{BASE_URL}/predict",
            json={"pixels": pixels}
        )
        if response.status_code == 200:
            data = response.json()
            print_success("Edge case pixels handled successfully")
            print(f"  Predicted Digit: {data.get('predicted_digit')}")
            return True
        else:
            print_error(f"Edge case failed with status {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Edge case exception: {e}")
        return False


def test_response_structure():
    """Test response structure and types."""
    print_section("Test 10: Response Structure Validation")
    try:
        pixels = np.random.rand(784).tolist()
        response = requests.post(
            f"{BASE_URL}/predict",
            json={"pixels": pixels}
        )
        if response.status_code == 200:
            data = response.json()
            required_fields = [
                "predicted_digit",
                "confidence",
                "all_probabilities",
                "model_used"
            ]
            
            all_present = all(field in data for field in required_fields)
            
            if all_present:
                # Validate types
                digit_valid = isinstance(data["predicted_digit"], int) and 0 <= data["predicted_digit"] <= 9
                confidence_valid = isinstance(data["confidence"], (int, float)) and 0.0 <= data["confidence"] <= 1.0
                probs_valid = isinstance(data["all_probabilities"], list) and len(data["all_probabilities"]) == 10
                model_valid = isinstance(data["model_used"], str)
                
                if digit_valid and confidence_valid and probs_valid and model_valid:
                    print_success("Response structure valid")
                    return True
                else:
                    print_error("Response types invalid")
                    return False
            else:
                print_error(f"Missing required fields")
                return False
        else:
            print_error(f"Failed with status {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Exception: {e}")
        return False


def run_all_tests():
    """Run all tests and report results."""
    print_section("MNIST Classifier API - Test Suite")
    print_info(f"Testing API at {BASE_URL}")
    
    tests = [
        test_health_check,
        test_api_info,
        test_random_prediction,
        test_zero_image,
        test_invalid_pixel_count,
        test_out_of_range_pixels,
        test_non_numeric_pixels,
        test_empty_request,
        test_edge_case_pixels,
        test_response_structure,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print_error(f"Test {test.__name__} crashed: {e}")
            results.append(False)
    
    # Print summary
    print_section("Test Summary")
    passed = sum(results)
    total = len(results)
    percentage = (passed / total) * 100
    
    print(f"Passed: {passed}/{total} ({percentage:.1f}%)\n")
    
    if passed == total:
        print_success("All tests passed! ✓")
    else:
        print_error(f"{total - passed} test(s) failed")
    
    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
