# Jupyter + MLflow + FastAPI (Linting inklusive) – Starterpaket

Dieses Paket startet:
- **JupyterLab** (Image: `jupyter/scipy-notebook`) mit NumPy, Pandas, Matplotlib, Seaborn, scikit-learn
- **MLflow UI** (Experiment-Tracking)
- **FastAPI** als **eigenes Image** (stabil; keine Runtime-Installation)
- Linting/Testing-Tools werden beim Start im Jupyter-Container installiert: `ruff`, `black`, `mypy`, `pytest`, `nbdime`, `jupyterlab-lsp`

## Start
```bash
docker compose build --no-cache   # baut das API-Image
docker compose up
```
Dienste:
- JupyterLab: http://localhost:8888
- MLflow:    http://localhost:5000
- FastAPI:   http://localhost:8000

> Jupyter startet **ohne Token** (nur lokal/Dev). Für produktive Nutzung bitte `JUPYTER_TOKEN` setzen oder die `--NotebookApp.*`-Flags anpassen.

## Arbeitsordner
- `./work` wird nach `/home/jovyan/work` gemountet.
- Beispielinhalte:
  - `work/notebooks/01_exploration.ipynb`
  - `work/sample_data.csv`
  - `work/reports/` (Outputs)

## FastAPI testen
```bash
curl -sSf http://localhost:8000/docs | head -n 5   # Healthcheck der API
curl -X POST http://localhost:8000/run-task   -H "Content-Type: application/json"   -d '{"csv_path": "work/sample_data.csv", "out_path": "work/reports/api_summary.md"}'
```
→ Report: `work/reports/api_summary.md`

## MLflow verwenden
1. UI öffnen: http://localhost:5000  
2. In Jupyter (Terminal/Notebook):
```bash
python - <<'PY'
import os, mlflow
os.environ['MLFLOW_TRACKING_URI'] = 'http://mlflow:5000'
mlflow.set_experiment('demo')
with mlflow.start_run(run_name='quick'):
    mlflow.log_param('alpha', 0.1)
    mlflow.log_metric('mse', 123.45)
print("Run geloggt -> MLflow UI prüfen.")
PY
```

## Linting & Tests (im Jupyter-Terminal)
```bash
ruff --version && black --version && mypy --version && pytest -q
```

## Troubleshooting
- **API-Port 8000 refused** → Stelle sicher, dass `docker compose build` vorher lief. Logs prüfen: `docker compose logs -f api`.
- **Berechtigungen in `work/` (Linux)** → setze optional `user: "${UID:-1000}:${GID:-1000}"` unter `jupyter:`.
