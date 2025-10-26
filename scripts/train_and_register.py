import os
import mlflow
import mlflow.sklearn
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split
from sklearn.linear_model import ElasticNet
from sklearn.metrics import root_mean_squared_error  # <-- neuer Import

TRACKING = os.getenv("MLFLOW_TRACKING_URI", "http://mlflow:5000")
MODEL_NAME = os.getenv("MODEL_NAME", "diabetes_regressor")

print(f"[trainer] Tracking URI: {TRACKING}")
print(f"[trainer] Model name:   {MODEL_NAME}")

mlflow.set_tracking_uri(TRACKING)
mlflow.set_experiment("demo-diabetes")

X, y = load_diabetes(return_X_y=True, as_frame=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

model = ElasticNet(alpha=0.4, l1_ratio=0.5, random_state=42)
model.fit(X_train, y_train)

# ✅ Verwende neue Funktion (ab sklearn 1.4)
rmse = root_mean_squared_error(y_test, model.predict(X_test))
print(f"[trainer] RMSE: {rmse:.4f}")

with mlflow.start_run(run_name="baseline"):
    mlflow.log_param("alpha", 0.4)
    mlflow.log_param("l1_ratio", 0.5)
    mlflow.log_metric("rmse", rmse)

    mlflow.sklearn.log_model(
        model,
        artifact_path="model",
        registered_model_name=MODEL_NAME,  # legt Registered Model + Version an
    )

print("[trainer] Training + Registrierung abgeschlossen.")
