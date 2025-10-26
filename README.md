# 🚀 MLflow + FastAPI + JupyterLab + n8n – Automatisiertes MLOps-Starterpaket

Dieses Setup bringt dir eine vollautomatische lokale MLOps-Umgebung:

- **MLflow** – Experiment-Tracking & Model-Registry  
- **Trainer-Service** – führt beim Start automatisch ein Training & Registrierung aus  
- **FastAPI** – bietet einen `/predict`-Endpoint und lädt das registrierte Modell automatisch  
- **JupyterLab** – für Notebooks, Experimente und Analysen  
- **n8n** – zur Orchestrierung von Workflows (z. B. Retraining-/Prediction-Automationen)

---

## 🧭 Architekturüberblick

```mermaid
flowchart TD
    subgraph Docker_Network["Docker-Netzwerk (mlnet)"]
    Jupyter[JupyterLab<br>Port 8888] -->|loggt Runs & Artefakte| MLflow
    Trainer[Trainer-Service<br>(train_and_register.py)] -->|registriert Modell| MLflow[MLflow Server<br>Port 5000]
    MLflow -->|Model Registry (Stage: None)| API[FastAPI<br>Port 8000]
    API -->|Predictions| n8n[n8n Workflows<br>Port 5678]
    n8n -->|HTTP Requests| API
    end
    User[(Lokaler Browser)] -->|öffnet| Jupyter & MLflow & n8n
```

---

## ⚙️ Komponentenüberblick

| Service   | Port | Beschreibung |
|------------|------|--------------|
| **JupyterLab** | 8888 | Notebook-Umgebung für Analysen & MLflow-Experimente |
| **MLflow UI**  | 5000 | Experimente, Metriken & Model Registry |
| **FastAPI** | 8000 | REST-API für Predictions, lädt registriertes Modell |
| **Trainer** | — | führt automatisch Training & Registrierung aus |
| **n8n** | 5678 | Workflow-Orchestrierung |

---

## 🚀 Starten

```bash
docker compose build --no-cache
docker compose up -d
```

**Ablauf beim Start:**
1. MLflow-DB wird automatisch migriert (Upgrade bei Versionswechsel).  
2. MLflow startet (Tracking & Registry).  
3. Trainer wartet auf MLflow, trainiert das Modell (`ElasticNet`) und registriert es als `diabetes_regressor`.  
4. FastAPI startet erst, wenn das Training erfolgreich abgeschlossen ist, und lädt `models:/diabetes_regressor/None`.  
5. JupyterLab & n8n starten im Hintergrund.

---

## 🌐 Dienste

| Service | URL |
|----------|-----|
| **JupyterLab** | [http://localhost:8888](http://localhost:8888) |
| **MLflow UI** | [http://localhost:5000](http://localhost:5000) |
| **FastAPI Docs** | [http://localhost:8000/docs](http://localhost:8000/docs) |
| **n8n** | [http://localhost:5678](http://localhost:5678) |

---

## 🧠 Datenfluss

1. **Trainer** führt `scripts/train_and_register.py` aus  
   → trainiert `ElasticNet`  
   → loggt Metriken & registriert Modell in MLflow  

2. **MLflow** speichert:
   - Runs & Artefakte unter `./mlruns/`
   - Registry (SQLite) im Volume `mlflow_db`

3. **FastAPI** lädt automatisch `models:/diabetes_regressor/None`  
   → `/predict` gibt Vorhersagen zurück.

4. **n8n** kann die API per HTTP-Node aufrufen:
   ```bash
   POST http://api:8000/predict
   {
     "data": [{"feature1": 0.1, "feature2": 0.2}]
   }
   ```

---

## 🧪 Beispiel: Manuelles Retraining

```bash
docker compose run --rm trainer
```

– führt erneut `train_and_register.py` aus und erstellt eine neue Modellversion.

---

## 🧰 Troubleshooting

| Problem | Ursache | Lösung |
|----------|----------|--------|
| **Schema mismatch** (`Detected out-of-date database schema`) | MLflow-Upgrade | Compose führt automatisch `mlflow db upgrade` aus |
| **API lädt kein Modell** | Trainer noch nicht fertig | `docker compose logs -f trainer` prüfen |
| **Verbindungsfehler MLflow** | falscher Hostname | In Docker: `http://mlflow:5000`, nicht `127.0.0.1` |
| **n8n kann API nicht erreichen** | getrennte Netzwerke | sicherstellen: `networks: [mlnet]` in beiden Services |

---

## 📂 Projektstruktur

```
.
├── api/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── scripts/
│   └── train_and_register.py
├── mlruns/
├── work/
├── docker-compose.yml
└── README.md
```

---

## 🧭 Weiterentwicklung

- Wechsel von **SQLite → Postgres** (für Mehrbenutzerbetrieb)  
- Nutzung von **MinIO/S3** als Artifact-Store  
- Erweiterung des Trainers für eigene Datensätze  
- Automatisierte Promotion per n8n → `/promote` Endpoint

---

**Stand:** Oktober 2025  
**Autor:** Ruwen Poljak
**Name:** Dein automatisiertes MLOps-Docker-Setup  
*(MLflow + FastAPI + Jupyter + n8n + Trainer-Service)*
