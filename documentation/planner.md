# Secure Medical Notes AI — 8-Week Project Timeline

This planner breaks down the project into weekly milestones, combining the Secure Summarizer and Nurse Assist modules. Adjust as needed for your team or class schedule.

---

## Week 1: Project Setup & Research
- Finalize requirements and architecture
- Set up repo, Docker, FastAPI, Streamlit skeletons
- Research compliance (HIPAA, audit logging)
- Draft initial data models (patients, users, notes)

## Week 2: Database & Auth Foundations
- Implement Postgres schema (patients, users, doctor_notes, nurse_notes)
- Add SQLAlchemy models & Alembic migrations
- Build basic user signup/login (JWT)
- Add healthcheck/test endpoints

## Week 3: Doctor Notes Module
- REST endpoints for doctor note upload & retrieval
- Add file upload (text, PDF placeholder)
- Store notes encrypted in DB
- Basic Streamlit UI: Doctor Notes tab

## Week 4: Summarization Agent (Doctor)
- Integrate LLM summarizer (LangChain/OpenAI)
- Summarize doctor notes (backend route + UI display)
- Add patient-friendly summary output
- Unit tests for summarizer

## Week 5: Nurse Notes & Real-Time Docs
- REST endpoints for nurse note upload (real-time)
- Link nurse notes to patients
- Streamlit UI: Nurse Notes tab (real-time entry)
- Store nurse notes encrypted

## Week 6: Nurse Assist Agent & RAG
- Integrate vector DB (pgvector/FAISS) for historical notes
- Build Nurse Assist Agent (retrieves, summarizes, flags risks)
- REST endpoint: /patient/{id}/risk_report
- Streamlit UI: Risk Flags tab

## Week 7: Audit Trail & Compliance
- Implement hash-chained audit log (backend + DB)
- Add audit log viewing endpoints
- Streamlit UI: Audit Trail tab
- RBAC (role-based access control)

## Week 8: Polish, Test, Docs, Stretch
- End-to-end tests (API, UI, agents)
- Polish UI (badges, timeline, recommendations)
- Write documentation (README, API docs, compliance notes)
- Stretch: Evidence integration, admin dashboard, deployment scripts

---

**Tip:** Adjust the order or depth of each week based on your team’s strengths and deadlines. Use this planner as a living document!
