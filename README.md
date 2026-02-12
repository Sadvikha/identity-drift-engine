# Identity Drift Engine

A lightweight, API-driven identity drift detection system that integrates with SailPoint Identity Security Cloud workflows to identify high-risk access changes and trigger governance-aligned notifications.

---

## 🚩 Problem Statement

Identity environments continuously evolve.  
Entitlements are added and removed, privileged access accumulates, and manual reviews struggle to keep up.

While certifications provide periodic review, they do not provide:

- Continuous drift awareness  
- Immediate risk surfacing  
- Event-driven response  

This project addresses that gap by implementing a lightweight, extensible drift detection pipeline that:

- Captures baseline access state  
- Detects changes over time  
- Classifies risk  
- Integrates with SailPoint workflows  
- Triggers human review notifications  

---

## 🏗️ Architecture Overview

The solution is intentionally split into two domains:

### 1️⃣ External Drift Engine (Developer-Controlled)
Built using FastAPI and Python.

Responsible for:
- Data collection
- Snapshot generation
- Drift comparison
- Risk classification
- API exposure

### 2️⃣ SailPoint Identity Security Cloud (System of Record)
Responsible for:
- Event triggering
- Workflow orchestration
- Decision branching
- Email notification

---

## 🔄 High-Level Flow

# Identity Drift Engine

A lightweight, API-driven identity drift detection system that integrates with SailPoint Identity Security Cloud workflows to identify high-risk access changes and trigger governance-aligned notifications.

---

## 🚩 Problem Statement

Identity environments continuously evolve.  
Entitlements are added and removed, privileged access accumulates, and manual reviews struggle to keep up.

While certifications provide periodic review, they do not provide:

- Continuous drift awareness  
- Immediate risk surfacing  
- Event-driven response  

This project addresses that gap by implementing a lightweight, extensible drift detection pipeline that:

- Captures baseline access state  
- Detects changes over time  
- Classifies risk  
- Integrates with SailPoint workflows  
- Triggers human review notifications  

---

## 🏗️ Architecture Overview

The solution is intentionally split into two domains:

### 1️⃣ External Drift Engine (Developer-Controlled)
Built using FastAPI and Python.

Responsible for:
- Data collection
- Snapshot generation
- Drift comparison
- Risk classification
- API exposure

### 2️⃣ SailPoint Identity Security Cloud (System of Record)
Responsible for:
- Event triggering
- Workflow orchestration
- Decision branching
- Email notification

---

## 🔄 High-Level Flow

Account Aggregation Completed
↓
SailPoint Workflow Trigger
↓
HTTP Call → FastAPI Drift Engine
↓
Drift Detection + Risk Classification
↓
Return Structured Drift JSON
↓
Workflow Loop
↓
Send Email for HIGH Risk



---

## 📂 Project Structure

```json
identity-drift-engine/
│
├── api_server.py # FastAPI service
├── baseline_snapshot.py # Creates baseline snapshot
├── current_snapshot.py # Captures current access state
├── drift_detector.py # Compares baseline vs current
├── orchestrator.py # Executes full pipeline
├── drift.json # Drift results output
├── baseline.json # Stored baseline
├── current.json # Latest snapshot
└── requirements.txt
```


---

## ⚙️ Technical Design

### 1️⃣ Data Collection

The system collects identity data using SailPoint REST APIs via OAuth client credentials.

Collected objects:
- Identities
- Accounts
- Entitlements

Data is normalized into structured JSON format.

---

### 2️⃣ Baseline Snapshot

A baseline snapshot represents a known access state.

Stored in: baseline.json


This becomes the comparison reference.

---

### 3️⃣ Current Snapshot

A new snapshot is generated using the same collection logic.

Stored in: current.json



---

### 4️⃣ Drift Detection

The engine compares:

- Added entitlements
- Removed entitlements

Output stored in: drift.json


Example output:

```json
{
  "drifts": [
    {
      "accountId": "user123",
      "entitlement": "Domain Admin",
      "eventType": "ADDED",
      "riskLevel": "HIGH",
      "recommendedAction": "Review and remove if unauthorized"
    }
  ]
}
```

---

### 5️⃣ Risk Classification

Simple policy-based classification rules:

Example:

- Entitlements containing "Admin"

- Privileged group assignments

- Sensitive access keywords

Each drift event is enriched with:

- Risk Level (LOW / MEDIUM / HIGH)

- Event Type

- Recommended Action

The logic is fully extensible.

---


### 6️⃣ FastAPI Service

The drift engine is exposed via REST endpoints:

Endpoint	Method	Description
/health	        GET	Health check
/baseline	POST	Create baseline snapshot
/run	        POST	Execute full pipeline
/drift	        POST	Run drift detection only
/drift/report	GET	Retrieve drift results


---
## 🚀 Running Locally

### 1️⃣ Install Dependencies
pip install -r requirements.txt

### 2️⃣ Start FastAPI Server
uvicorn api_server:app --reload


``json 
    Access Swagger UI:

    http://127.0.0.1:8000/docs
```

### 3️⃣ Create Baseline
POST /baseline

### 4️⃣ Run Full Pipeline
POST /run

### 5️⃣ View Drift Report
GET /drift/report

---
## 🔗 SailPoint Workflow Integration

A SailPoint Identity Security Cloud workflow is configured to:

- Trigger after account aggregation completion

- Call the FastAPI endpoint using HTTP action

- Iterate over returned drift results

- Filter HIGH-risk items

- Send email notifications

---
## 🛡️ Governance Philosophy

This system intentionally follows a human-in-the-loop automation model.

Automation is used for:

- Detection

- Classification

- Alerting

- Human decision-making is used for:

- Remediation

- Approval

- Access removal

This avoids over-automation risks while improving response time.

---

### 📊 Extensibility

Future enhancements may include:

- Approval workflow integration

- Auto-remediation policies

- Access request creation

- Certification trigger automation

- AI-based risk scoring

- Dashboard visualization layer

- Persistent database storage

- Event streaming architecture

---

## 🧠 Key Design Principles

Externalize complex logic

Keep identity platform clean

Use APIs for extensibility

Separate detection from remediation

Prefer safe automation over aggressive automation

Design for auditability

---

## 📌 Limitations

- No persistent database (JSON storage)

- No real-time streaming architecture

- Rule-based risk scoring only

- No automated remediation

- Single-tenant test setup

---
## 🎯 Intended Use Case

- This project is ideal for:

- Developers extending identity platforms

- Architects designing adaptive identity workflows

- Security teams seeking lightweight drift monitoring

- Identity governance proof-of-concepts

---
## 🏁 Conclusion

- The Identity Drift Engine demonstrates how to:

- Extend identity workflows through APIs

- Detect access drift in near-real time

- Integrate external services with SailPoint

- Implement governance-aligned automation

- Build adaptive identity systems safely

It is a practical, developer-driven implementation of platform extensibility in identity security.
