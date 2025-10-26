# ./api/app.py
import os
from fastapi import FastAPI
from pydantic import BaseModel
import mlflow
import mlflow.pyfunc 
import pandas as pd
# from pathlib import Path

MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://mlflow:5000")
MODEL_NAME = os.getenv("MODEL_NAME", "diabetes_regressor")  # anpassen
MODEL_STAGE = os.getenv("MODEL_STAGE", "None")   # <- hier "None"

app = FastAPI(title="Predict API")
_model = None

class PredictRequest(BaseModel):
    data: list[dict]

def load_model_dynamic():
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    return mlflow.pyfunc.load_model(f"models:/{MODEL_NAME}/{MODEL_STAGE}")

@app.on_event("startup")
def warm():
    global _model
    try:
        _model = load_model_dynamic()
        print(f"[startup] loaded models:/{MODEL_NAME}/{MODEL_STAGE}")
    except Exception as e:
        _model = None
        print(f"[startup] no model yet: {e}")

@app.post("/predict")
def predict(req: PredictRequest):
    global _model
    if _model is None:
        return {"error": "No model loaded yet. Try again after trainer finished."}
    df = pd.DataFrame(req.data)
    preds = _model.predict(df)
    return {"predictions": preds.tolist()}
