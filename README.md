# Secure Medical Notes Summarizer (with Nurse Assist)

A secure, AI-powered clinical documentation platform for healthcare teams. Doctors and nurses can upload and summarize notes, receive risk assessments, and get evidence-based recommendations—all with tamper-proof audit trails and compliance by design.

---

## What This Project Solves
- **Reduces cognitive load for nurses and doctors** by summarizing real-time and historical notes.
- **Flags at-risk patients** and suggests evidence-based interventions, supporting faster, safer clinical decisions.
- **Ensures compliance** with encryption, audit trails, and role-based access.
- **Provides a professional, interview-ready example** of a modern, secure, healthcare AI service.

---

## Architecture Diagram
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

## Final Tech Stack
1. **API/Backend**
   - FastAPI: REST API endpoints
   - Celery + Redis: Background jobs (summarization, encryption, risk scan)
   - PostgreSQL: Store patients, notes, summaries, audit logs
   - SQLAlchemy + Alembic: ORM + migrations
   - python-dotenv: Manage secrets
2. **AI/LLM Layer**
   - LangChain: Orchestrates summarizer + nurse-assist agent
   - OpenAI GPT-4o / GPT-4-mini: Summarization + recommendations
   - Embeddings: text-embedding-3-small (OpenAI) or Hugging Face
   - Vector DB: FAISS or Postgres pgvector extension for historical notes
3. **UI/Dashboard**
   - Streamlit: Interactive web UI (no frontend coding)
   - Tabs: Doctor Notes | Nurse Notes | Summaries | Risk Reports | Audit Trail
   - Plotly/Altair (optional): Graphs for risk levels or timeline view
4. **Infrastructure / Deployment**
   - Docker + Docker Compose: Run Postgres, Redis, API, and UI containers
   - Nginx: Optional reverse proxy if deployed
   - GitHub Actions: CI for linting & tests
   - GCP/AWS (optional): Deploy if time/credits allow
5. **Security**
   - AES (cryptography): Encrypt stored notes
   - JWT/OAuth2: User auth + RBAC (Doctor, Nurse, Admin)
   - Audit logging: Postgres table (hash chain optional)
6. **Notebooks (Exploration)**
   - eval_llm_prompts.ipynb: Test summarization prompts
   - risk_agent_prototyping.ipynb: Retrieval + risk scoring
   - nurse_demo_flow.ipynb: Simulate full nurse-assist flow

---

## Project Flow
1. **Doctors upload notes** via the UI. Notes are encrypted and stored in Postgres.
2. **Nurses enter real-time notes**; the system summarizes and links them to patient history.
3. **Background jobs** (Celery) handle summarization, encryption, and risk scanning.
4. **LLM/Agents** (LangChain + OpenAI) generate summaries, risk reports, and recommendations.
5. **Audit logs** are created for every access and modification, ensuring compliance.
6. **Dashboard** (Streamlit) displays notes, summaries, risk flags, and audit trails for doctors and nurses.

---

## Features
- **Doctor & Nurse Notes:** Upload, summarize, and encrypt clinical notes.
- **Nurse Assist Module:** Real-time documentation, risk flagging, and intervention suggestions using LLMs and RAG over historical data.
- **Audit Trail:** Immutable, hash-chained logs for compliance.
- **Role-based Summaries:** Patient-friendly and clinical summaries for different users.
- **Evidence Integration:** Recommendations grounded in clinical guidelines and past data.

---

## Project Structure
secure-med-notes-ai/
├─ README.md
├─ requirements.txt
├─ .gitignore
├─ .env.example
├─ docker-compose.yml
│
├─ infra/
│  ├─ Dockerfile.api
│  ├─ Dockerfile.worker
│  ├─ Dockerfile.ui
│  └─ nginx.conf
│
├─ api/
│  ├─ main.py
│  ├─ deps.py
│  ├─ routes/
│  ├─ services/
│  ├─ agents/
│  ├─ models/
│  ├─ db/
│  ├─ tasks/
│  └─ tests/
│
├─ ui/
│  ├─ app.py
│  ├─ components/
│  └─ assets/
│
├─ data/
│  ├─ sample_doctor_notes/
│  ├─ sample_nurse_notes/
│  └─ policies/hipaa.md
│
├─ documentation/
│  └─ planner.md
│
└─ notebooks/
   ├─ eval_llm_prompts.ipynb
   ├─ risk_agent_prototyping.ipynb
   └─ nurse_demo_flow.ipynb

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