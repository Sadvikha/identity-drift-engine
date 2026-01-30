import json
from datetime import datetime

AUDIT_FILE = "audit_log.json"

def log_event(event):
    event["timestamp"] = datetime.utcnow().isoformat()

    try:
        with open(AUDIT_FILE, "r") as f:
            logs = json.load(f)
    except:
        logs = []

    logs.append(event)

    with open(AUDIT_FILE, "w") as f:
        json.dump(logs, f, indent=4)
