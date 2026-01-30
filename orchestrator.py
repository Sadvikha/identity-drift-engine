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
