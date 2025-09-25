# Secure Medical Notes Summarizer (with Nurse Assist) — Starter

Minimal skeleton for FastAPI backend + Streamlit UI.

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