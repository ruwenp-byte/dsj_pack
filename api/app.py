# ./api/app.py
import os
from fastapi import FastAPI
from pydantic import BaseModel
import mlflow
import mlflow.pyfunc 
import pandas as pd
from pathlib import Path

MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://mlflow:5000")
MODEL_NAME = os.getenv("MODEL_NAME", "diabetes_regressor")  # anpassen
MODEL_STAGE = os.getenv("MODEL_STAGE", "None")   # <- hier "None"

app = FastAPI(title="Predict API")
_model = None

class ReportRequest(BaseModel):
    csv_path: str = "/home/jovyan/work/run_task.csv"
    out_path: str = "/home/jovyan/work/reports/task_summary.md"

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

@app.post("/run-task")
def run_task(req: ReportRequest):
    csv = Path(req.csv_path)
    out = Path(req.out_path)
    df = pd.read_csv(csv)
    n = len(df)
    rev_mean = float(df["revenue"].mean())
    spend_mean = float(df["marketing_spend"].mean())
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        f"# API Summary\n\nRows: {n}\n\nMean revenue: {rev_mean:.2f}\n\nMean marketing_spend: {spend_mean:.2f}\n"
    )
    return {"status": "ok", "written": str(out)}