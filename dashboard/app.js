const API = "http://127.0.0.1:8000";

async function loadDrift() {
    const res = await fetch(`${API}/drift/report`);
    const data = await res.json();

    const table = document.getElementById("driftTable");

    data.forEach(d => {
        const row = table.insertRow();
        row.insertCell(0).innerText = d.accountId;
        row.insertCell(1).innerText = d.entitlement;
        row.insertCell(2).innerText = d.riskLevel;
        row.insertCell(3).innerText = d.recommendedAction;
    });
}

async function loadAudit() {
    const res = await fetch(`${API}/audit`);
    const data = await res.json();

    const table = document.getElementById("auditTable");

    data.forEach(a => {
        const row = table.insertRow();
        row.insertCell(0).innerText = a.accountId;
        row.insertCell(1).innerText = a.entitlement;
        row.insertCell(2).innerText = a.actionTaken;
        row.insertCell(3).innerText = a.status;
    });
}

loadDrift();
loadAudit();
