import requests
import numpy as np

# Generate a random normalized image for testing
sample_pixels = np.random.rand(784).tolist()

response = requests.post(
    "http://localhost:8000/predict",
    json={"pixels": sample_pixels}
)

print("Status:", response.status_code)
print("Response:", response.json())
