import requests
import json
from datetime import datetime
import os

from dotenv import load_dotenv

load_dotenv()  # Loads from .env file

TENANT = os.getenv("SAILPOINT_TENANT", "partner5799")  # Optional fallback for tenant
CLIENT_ID = os.getenv("SAILPOINT_CLIENT_ID")
CLIENT_SECRET = os.getenv("SAILPOINT_CLIENT_SECRET")
IDENTITY_ID = os.getenv("SAILPOINT_IDENTITY_ID")

# Safety check (add this)
if not CLIENT_ID or not CLIENT_SECRET:
    raise ValueError("Missing required SailPoint credentials in environment variables")

def get_token():
    url = f"https://partner5799.api.identitynow-demo.com/oauth/token"

    payload = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }

    response = requests.post(url, data=payload)
    response.raise_for_status()

    return response.json()["access_token"]

def get_accounts(token):
    url = f"https://partner5799.api.identitynow-demo.com/v3/accounts"
    params = {
        "filters": f'identityId eq "{IDENTITY_ID}"'
    }

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()

    return response.json()

def get_entitlements(token, account_id):
    url = f"https://partner5799.api.identitynow-demo.com/v3/accounts/{account_id}/entitlements"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    return response.json()

def build_snapshot():
    token = get_token()
    accounts = get_accounts(token)

    snapshot = {
        "identityId": IDENTITY_ID,
        "capturedAt": datetime.utcnow().isoformat(),
        "accounts": []
    }

    for acc in accounts:
        if acc.get("hasEntitlements"):
            entitlements = get_entitlements(token, acc["id"])

            ent_names = [e["name"] for e in entitlements]

            snapshot["accounts"].append({
                "accountId": acc["id"],
                "source": acc["sourceName"],
                "entitlements": ent_names
            })

    return snapshot

def save_snapshot(snapshot):
    with open("baseline.json", "w") as f:
        json.dump(snapshot, f, indent=4)


if __name__ == "__main__":
    snapshot = build_snapshot()
    save_snapshot(snapshot)
    print("Baseline snapshot created: baseline.json")
