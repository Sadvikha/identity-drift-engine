import os
import subprocess

if not os.path.exists("baseline.json"):
    print("Baseline not found. Creating baseline...")
    subprocess.run(["python", "baseline_snapshot.py"])
else:
    print("Baseline exists.")
    print("Creating current snapshot...")
    subprocess.run(["python", "current_snapshot.py"])

    print("Running drift detection...")
    subprocess.run(["python", "drift_detector.py"])


import json

drifts = [
    {
        "riskLevel": "HIGH",
        "accountId": "demo-user",
        "entitlement": "Domain Admin",
        "recommendedAction": "Remove Access"
    }
]

with open("drift.json", "w") as f:
    json.dump(drifts, f)

print("Injected demo drift")
