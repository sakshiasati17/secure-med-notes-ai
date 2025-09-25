# Secure Medical Notes AI — 8-Week Project Timeline (Team of 2)

This planner breaks down the project into weekly milestones, with clear, balanced work for both team members. Each person will work on both backend and frontend tasks, ensuring equal opportunities and collaboration.

---

## Week 1: Project Setup & Research
- **Both:**
  - Finalize requirements, repo, and architecture together
  - Set up Docker, FastAPI, Streamlit skeletons
  - Research compliance (HIPAA, audit logging)
  - Draft initial data models (patients, users, notes)

## Week 2: Database & Auth Foundations
- **Person A:**
  - Implement Postgres schema (patients, users, doctor_notes, nurse_notes)
  - Add SQLAlchemy models & Alembic migrations
- **Person B:**
  - Build basic user signup/login (JWT) in FastAPI
  - Add healthcheck/test endpoints
- **Both:**
  - Review each other’s code and test DB + auth integration

## Week 3: Doctor Notes Module
- **Person A:**
  - REST endpoints for doctor note upload & retrieval (API)
  - Add file upload (text, PDF placeholder)
- **Person B:**
  - Streamlit UI: Doctor Notes tab (upload, view)
  - Display uploaded notes in UI
- **Both:**
  - Test end-to-end doctor note upload and display

## Week 4: Summarization Agent (Doctor)
- **Person A:**
  - Integrate LLM summarizer (LangChain/OpenAI) in backend
  - Add backend route for summarization
- **Person B:**
  - UI: Display summaries, add patient-friendly summary output
  - Unit tests for summarizer (work together)
- **Both:**
  - Demo doctor note summarization in UI

## Week 5: Nurse Notes & Real-Time Docs
- **Person A:**
  - REST endpoints for nurse note upload (real-time)
  - Link nurse notes to patients
- **Person B:**
  - Streamlit UI: Nurse Notes tab (real-time entry)
  - Display nurse notes in UI
- **Both:**
  - Test nurse note upload and display

## Week 6: Nurse Assist Agent & RAG
- **Person A:**
  - Integrate vector DB (pgvector/FAISS) for historical notes
  - Build Nurse Assist Agent (retrieves, summarizes, flags risks)
- **Person B:**
  - REST endpoint: /patient/{id}/risk_report
  - Streamlit UI: Risk Flags tab (risk report display)
- **Both:**
  - Test risk flagging and recommendations in UI

## Week 7: Audit Trail & Compliance
- **Person A:**
  - Implement hash-chained audit log (backend + DB)
  - Add audit log viewing endpoints
- **Person B:**
  - Streamlit UI: Audit Trail tab
  - RBAC (role-based access control) in UI
- **Both:**
  - Test audit log and RBAC

## Week 8: Polish, Test, Docs, Stretch
- **Both:**
  - End-to-end tests (API, UI, agents)
  - Polish UI (badges, timeline, recommendations)
  - Write documentation (README, API docs, compliance notes)
  - Stretch: Evidence integration, admin dashboard, deployment scripts

---

**Tip:** Pair on tricky features, review each other’s PRs, and meet weekly to demo progress and adjust the plan!
