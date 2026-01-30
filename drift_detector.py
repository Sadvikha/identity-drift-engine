import json

# -------------------------
# Risk Classification Rules
# -------------------------

HIGH_RISK_KEYWORDS = [
    "admin",
    "root",
    "finance",
    "payroll",
    "privileged",
    "security",
    "superuser"
]

def calculate_risk(entitlement_name):
    name = entitlement_name.lower()
    for word in HIGH_RISK_KEYWORDS:
        if word in name:
            return "HIGH"
    return "LOW"


# -------------------------
# Utility
# -------------------------

def load(file):
    with open(file) as f:
        return json.load(f)


# -------------------------
# Load Snapshots
# -------------------------

baseline = load("baseline.json")
current = load("current.json")


# -------------------------
# Build Maps
# -------------------------

baseline_map = {}
for acc in baseline["accounts"]:
    baseline_map[acc["accountId"]] = set(acc["entitlements"])

current_map = {}
for acc in current["accounts"]:
    current_map[acc["accountId"]] = set(acc["entitlements"])


# -------------------------
# Drift Detection
# -------------------------

drift_report = []

for account_id in current_map:

    base_ents = baseline_map.get(account_id, set())
    curr_ents = current_map.get(account_id, set())

    added = curr_ents - base_ents
    removed = base_ents - curr_ents

    # Handle added entitlements
    for ent in added:
        risk = calculate_risk(ent)

        drift_report.append({
            "eventType": "ENTITLEMENT_ADDED",
            "accountId": account_id,
            "entitlement": ent,
            "riskLevel": risk,
            "policyViolation": True if risk == "HIGH" else False,
            "recommendedAction": "REMOVE_ACCESS" if risk == "HIGH" else "REVIEW"
        })

    # Handle removed entitlements
    for ent in removed:
        drift_report.append({
            "eventType": "ENTITLEMENT_REMOVED",
            "accountId": account_id,
            "entitlement": ent,
            "riskLevel": "INFO",
            "policyViolation": False,
            "recommendedAction": "NONE"
        })


# -------------------------
# Output
# -------------------------

if not drift_report:
    print("✅ No drift detected")
else:
    print("🚨 Drift detected:")
    for d in drift_report:
        print(json.dumps(d, indent=2))


# -------------------------
# Save Drift File
# -------------------------

with open("drift.json", "w") as f:
    json.dump(drift_report, f, indent=4)
