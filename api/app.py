from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
from pathlib import Path

app = FastAPI(title="Course API")

class ReportRequest(BaseModel):
    csv_path: str = "work/sample_data.csv"
    out_path: str = "work/reports/api_summary.md"

@app.get("/")
def root():
    return {"ok": True}

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
