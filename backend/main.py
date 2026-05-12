from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
from model_loader import load_model, load_model_name

app = FastAPI(title="MNIST Digit Classifier API")

# CORS — allow React frontend on any port
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model once at startup
model = load_model()
model_name = load_model_name()

class PredictRequest(BaseModel):
    pixels: list[float]  # 784 floats, normalized 0-1

class PredictResponse(BaseModel):
    predicted_digit: int
    confidence: float
    all_probabilities: list[float]
    model_used: str

@app.get("/")
def root():
    return {
        "message": "MNIST Classifier API is running",
        "model": model_name
    }

@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": model is not None}

@app.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest):
    pixels = request.pixels

    # Validate input length
    if len(pixels) != 784:
        raise HTTPException(
            status_code=400,
            detail=f"Expected 784 pixels, got {len(pixels)}"
        )

    # Convert to numpy array and reshape
    img_array = np.array(pixels, dtype=np.float32).reshape(1, -1)

    # Predict
    predicted_digit = int(model.predict(img_array)[0])

    # Get probabilities if model supports it
    if hasattr(model, "predict_proba"):
        proba = model.predict_proba(img_array)[0]
        confidence = float(proba[predicted_digit])
        all_probs = [round(float(p), 4) for p in proba]
    else:
        confidence = 1.0
        all_probs = [0.0] * 10
        all_probs[predicted_digit] = 1.0

    return PredictResponse(
        predicted_digit=predicted_digit,
        confidence=round(confidence, 4),
        all_probabilities=all_probs,
        model_used=model_name
    )
