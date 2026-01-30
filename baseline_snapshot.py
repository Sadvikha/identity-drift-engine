import requests
import json
from datetime import datetime

TENANT = "partner5799"

CLIENT_ID = "002e5667-ea34-49d7-8062-316a1f393bd7"
CLIENT_SECRET = "df902a30abe46742afaa001b560f07f3bef50831434c0b676650a191eb6874c5"

IDENTITY_ID = "2e247ea01c864797818b2b554f69c81c"

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
