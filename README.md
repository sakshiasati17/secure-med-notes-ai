# Secure Medical Notes Summarizer (with Nurse Assist)

A secure, AI-powered clinical documentation platform for healthcare teams. Doctors and nurses can upload and summarize notes, receive risk assessments, and get evidence-based recommendations—all with tamper-proof audit trails and compliance by design.

---

## What This Project Solves
- **Reduces cognitive load for nurses and doctors** by summarizing real-time and historical notes.
- **Flags at-risk patients** and suggests evidence-based interventions, supporting faster, safer clinical decisions.
- **Ensures compliance** with encryption, audit trails, and role-based access.
- **Provides a professional, interview-ready example** of a modern, secure, healthcare AI service.

---

## Tech Stack
- **API:** FastAPI (Python)
- **UI:** Streamlit (Python)
- **Database:** PostgreSQL (structured data: patients, users, notes, audit logs)
- **Message Queue:** Celery + Redis (background summarization, encryption)
- **Key-Value Store:** Redis
- **LLM/AI:** OpenAI GPT (via LangChain) or BioBERT/ClinicalBERT
- **Encryption:** AES-256 (at rest), TLS (in transit), key management (Vault/KMS)
- **Containers:** Docker (local/cloud deployment)
- **(Optional) Storage:** S3/MinIO for file storage

---

## Features
- **Doctor & Nurse Notes:** Upload, summarize, and encrypt clinical notes.
- **Nurse Assist Module:** Real-time documentation, risk flagging, and intervention suggestions using LLMs and RAG over historical data.
- **Audit Trail:** Immutable, hash-chained logs for compliance.
- **Role-based Summaries:** Patient-friendly and clinical summaries for different users.
- **Evidence Integration:** Recommendations grounded in clinical guidelines and past data.

---

## Architecture
```
[Doctor/Nurse UI]
     │
     ▼
[API Gateway (FastAPI)]
     │
 ┌───┼─────────────┬─────────────┐
 │   │             │             │
 ▼   ▼             ▼             ▼
DB  MessageQ   VectorDB      Object Storage
(Postgres) (Celery/Redis) (pgvector/FAISS) (S3/MinIO)
     │
     ▼
[LLM/Agents (LangChain)]
     │
     ▼
[Audit Log, Risk Engine, Compliance]
```

---

## Setup Instructions
1. **Clone the repo:**
   ```sh
   git clone https://github.com/sakshiasati17/secure-med-notes-ai.git
   cd secure-med-notes-ai
   ```
2. **Copy and edit environment variables:**
   ```sh
   cp .env.example .env
   # Edit .env as needed
   ```
3. **Start infrastructure:**
   ```sh
   docker compose up -d
   ```
4. **Create and activate Python virtual environment:**
   ```sh
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
5. **Run API locally:**
   ```sh
   uvicorn api.main:app --reload
   # Visit http://127.0.0.1:8000
   ```
6. **Run UI locally:**
   ```sh
   streamlit run ui/app.py
   # Visit http://localhost:8501
   ```

---

## Sample API Calls

### Healthcheck
```http
GET / HTTP/1.1
Host: localhost:8000
```
Response:
```json
{"status": "ok"}
```

### (Planned) Upload Nurse Note
```http
POST /nurse_notes/upload HTTP/1.1
Content-Type: multipart/form-data
Authorization: Bearer <token>

file=@note.txt&patient_id=<uuid>
```
Response:
```json
{"note_id": "..."}
```

### (Planned) Get Patient Risk Report
```http
GET /patient/{id}/risk_report HTTP/1.1
Authorization: Bearer <token>
```
Response:
```json
{
  "risk_level": "High",
  "summary": "...",
  "risks": ["Possible infection"],
  "recommendations": ["Monitor vitals every 30 min"],
  "escalation": "Consider infectious disease consult"
}
```

---

## Quick Start

1) Copy `.env.example` to `.env` and fill values.
2) Start infra: `docker compose up -d` (Postgres + Redis).
3) (When ready) run API locally: `uvicorn api.main:app --reload`
4) (When ready) run UI: `streamlit run ui/app.py`

## Install Checklist (no coding)
- VS Code (+ extensions: Python, Pylance, Docker, GitHub PRs & Issues, REST/Thunder Client, Python Test Adapter)
- Python 3.11+
- Git + GitHub CLI (`gh`)
- Docker Desktop
- OpenAI account + API key
- Optional: DBeaver/pgAdmin, Postman/Insomnia, WSL2 (Windows), Node.js (only if React later)

## Next Steps
- Fill `api/main.py` with FastAPI routes.
- Fill `ui/app.py` with Streamlit tabs.
- Add Celery worker + tasks when ready.