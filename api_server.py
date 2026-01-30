from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import subprocess
import json
import os

app = FastAPI(title="Identity Drift Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------
# Health Check
# -----------------------

@app.get("/health")
def health():
    return {"status": "running"}

# -----------------------
# Create Baseline
# -----------------------

@app.post("/baseline")
def create_baseline():
    subprocess.run(["python", "baseline_snapshot.py"])
    return {"message": "Baseline created"}

# -----------------------
# Run Full Pipeline
# -----------------------

@app.post("/run")
def run_pipeline():
    subprocess.run(["python", "orchestrator.py"])
    return {"message": "Pipeline executed"}

# -----------------------
# Run Drift Detection Only
# -----------------------

@app.post("/drift")
def run_drift():
    subprocess.run(["python", "drift_detector.py"])
    return {"message": "Drift detection executed"}

# -----------------------
# Get Drift Report
# -----------------------

@app.get("/drift/report")
def get_drift_report():
    if not os.path.exists("drift.json"):
        return {"message": "No drift report found"}

    with open("drift.json") as f:
        data = json.load(f)

    return data

#Optional
@app.get("/")
def root():
    return {"message": "Identity Drift Engine API Running"}

#audit logs
@app.get("/audit")
def get_audit_logs():
    with open("audit_log.json") as f:
        return json.load(f)
