from fastapi import FastAPI
from pydantic import BaseModel
from fastai.text.all import *
import os
import requests

# Auto-download model from Google Drive if not present
MODEL_URL = "https://drive.google.com/uc?export=download&id=1wyTRTGIQFSIDoeADJZMwxpD0kV8cmcgJ"
MODEL_PATH = "news_category_classifier.pkl"

if not os.path.exists(MODEL_PATH):
    print("Downloading model from Google Drive...")
    response = requests.get(MODEL_URL)
    with open(MODEL_PATH, "wb") as f:
        f.write(response.content)

# Load model
learn = load_learner(MODEL_PATH)

# FastAPI setup
class NewsRequest(BaseModel):
    text: str

app = FastAPI(title="News Category Classifier")

@app.post("/predict")
def predict_category(req: NewsRequest):
    pred_class, pred_idx, probs = learn.predict(req.text)
    return {
        "prediction": str(pred_class),
        "confidence": round(probs[pred_idx].item(), 4)
    }
