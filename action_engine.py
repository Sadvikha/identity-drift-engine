import json
from audit_logger import log_event


def load(file):
    with open(file) as f:
        return json.load(f)


drifts = load("drift.json")

if not drifts:
    print("No actions required.")
    exit()


for d in drifts:

    if d["recommendedAction"] == "REMOVE_ACCESS":
        print("🚨 AUTO REMEDIATION")
        print(f'Removing entitlement {d["entitlement"]} from account {d["accountId"]}')

        log_event({
            "identityId": d.get("identityId", "unknown"),
            "accountId": d["accountId"],
            "entitlement": d["entitlement"],
            "eventType": d["eventType"],
            "riskLevel": d["riskLevel"],
            "policy": "High Risk Keyword Match",
            "actionTaken": "REMOVE_ACCESS",
            "status": "SUCCESS"
        })

    elif d["recommendedAction"] == "REVIEW":
        print("🔍 REVIEW REQUIRED")
        print(f'Review entitlement {d["entitlement"]}')


print("Action processing complete.")
