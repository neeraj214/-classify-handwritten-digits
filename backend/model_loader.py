import joblib
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), 
                          "../mnist-digit-classifier/models/final_model.pkl")
INFO_PATH = os.path.join(os.path.dirname(__file__), 
                         "../mnist-digit-classifier/models/model_info.txt")

def load_model():
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            f"Model not found at {MODEL_PATH}. "
            "Run Phase 4 notebook first."
        )
    model = joblib.load(MODEL_PATH)
    return model

def load_model_name():
    if os.path.exists(INFO_PATH):
        with open(INFO_PATH, "r") as f:
            return f.read().strip()
    return "Unknown Model"
