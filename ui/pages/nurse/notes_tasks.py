import streamlit as st
import requests
from datetime import datetime
from uuid import uuid4

from design_system import (
    st_section_header,
    st_gradient_button,
)


def _headers():
    if st.session_state.access_token:
        return {"Authorization": f"Bearer {st.session_state.access_token}"}
    return {}


def _fetch_notes():
    try:
        resp = requests.get(
            f"{st.session_state.API_BASE_URL}/notes",
            headers=_headers(),
            timeout=8,
        )
        if resp.status_code == 200:
            return resp.json()
    except Exception:
        pass
    return []

def _fetch_patients():
    try:
        resp = requests.get(
            f"{st.session_state.API_BASE_URL}/patients/",
            headers=_headers(),
            timeout=8,
        )
        if resp.status_code == 200:
            return resp.json()
    except Exception:
        pass
    return []


def _ensure_task_state():
    if "nurse_tasks" in st.session_state:
        return
    st.session_state.nurse_tasks = [
        {
            "id": str(uuid4()),
            "title": "Administer medication - Room 305",
            "due": "10:30 AM",
            "priority": "High",
            "status": "upcoming",
            "created_at": datetime.now().isoformat(),
            "completed_at": None,
        },
        {
            "id": str(uuid4()),
            "title": "Wound dressing change - Room 307",
            "due": "11:00 AM",
            "priority": "Medium",
            "status": "upcoming",
            "created_at": datetime.now().isoformat(),
            "completed_at": None,
        },
        {
            "id": str(uuid4()),
            "title": "Patient education - Room 310",
            "due": "02:00 PM",
            "priority": "Low",
            "status": "upcoming",
            "created_at": datetime.now().isoformat(),
            "completed_at": None,
        },
    ]


def _ensure_vitals_state():
    if "nurse_vitals" not in st.session_state:
        st.session_state.nurse_vitals = []


def _mark_task_complete(task_id: str):
    for task in st.session_state.nurse_tasks:
        if task["id"] == task_id and task["status"] != "completed":
            task["status"] = "completed"
            task["completed_at"] = datetime.now().isoformat()
            st.success("Task completed.")
            st.rerun()
            return


def _add_task(title: str, due: str, priority: str):
    st.session_state.nurse_tasks.append(
        {
            "id": str(uuid4()),
            "title": title,
            "due": due,
            "priority": priority,
            "status": "upcoming",
            "created_at": datetime.now().isoformat(),
            "completed_at": None,
        }
    )
    st.success("Task added to board.")
    st.rerun()


def _render_notes_library():
    notes = _fetch_notes()
    if not notes:
        st.info("No nurse notes available yet.")
        return
    notes_sorted = sorted(
        notes,
        key=lambda note: note.get("created_at") or note.get("updated_at") or "",
        reverse=True,
    )
    for note in notes_sorted[:10]:
        created = note.get("created_at", "")[:16].replace("T", " ")
        st.markdown(
            f"""
            <div class="smn-panel" style="padding:1rem; margin-bottom:0.7rem;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <strong>{note.get('title','Note')}</strong>
                    <span class="smn-pill">Patient #{note.get('patient_id','')}</span>
                </div>
                <small style="color:var(--muted);">{created or '—'}</small>
                <p style="color:var(--muted); margin:0.6rem 0;">{note.get('content','')[:220]}...</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


def show():
    """Nurse Notes & Tasks Page"""
    st_section_header(
        "Notes, Tasks & Vitals",
        "Document nursing notes, manage tasks, and capture vital signs.",
    )

    _ensure_task_state()
    _ensure_vitals_state()

    notes_tab, tasks_tab, vitals_tab = st.tabs(
        ["📝 Nurse Notes", "✅ Task Management", "🩺 Vitals Records"]
    )

    with notes_tab:
        create_tab, library_tab = st.tabs(["Create Note", "Notes Library"])

        with create_tab:
            st.markdown("#### Create Nurse Note")
            with st.form("nurse_note_form"):
                col1, col2 = st.columns(2)
                with col1:
                    patient_id = st.number_input("Patient ID", min_value=1, value=1)
                    note_type = st.selectbox(
                        "Note Type",
                        ["Assessment Note", "Progress Note", "Shift Report", "Incident Report"],
                    )
                with col2:
                    visit_date = st.date_input("Date", value=datetime.now())
                    visit_time = st.time_input("Time")

                vitals = st.text_area("Vital Signs", placeholder="BP, HR, Temp, RR, SpO₂ ...")
                observations = st.text_area("Observations", height=100)
                interventions = st.text_area("Interventions / Care Provided", height=100)
                patient_response = st.text_area("Patient Response", height=80)

                if st.form_submit_button("💾 Save Note"):
                    note_data = {
                        "patient_id": patient_id,
                        "title": f"{note_type} - {visit_date}",
                        "content": f"""**Vitals**: {vitals}

**Observations**: {observations}

**Interventions**: {interventions}

**Patient Response**: {patient_response}""",
                        "note_type": "nurse_note",
                    }
                    resp = requests.post(
                        f"{st.session_state.API_BASE_URL}/notes",
                        json=note_data,
                        headers=_headers(),
                    )
                    if resp.status_code == 200:
                        st.success("Note saved successfully.")
                    else:
                        st.error("Unable to save note.")

        with library_tab:
            st.markdown("#### Notes Library")
            _render_notes_library()

    with tasks_tab:
        upcoming_tab, completed_tab, add_tab = st.tabs(
            ["Upcoming Tasks", "Completed Tasks", "➕ Add Task"]
        )

        with upcoming_tab:
            upcoming = [t for t in st.session_state.nurse_tasks if t["status"] == "upcoming"]
            if not upcoming:
                st.info("All tasks completed. Great job! 🎉")
            for task in upcoming:
                st.markdown(
                    f"""
                    <div class="smn-panel" style="margin-bottom:0.6rem;">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <div>
                                <strong>{task['title']}</strong>
                                <div class="smn-pill" style="margin-top:0.3rem;">Due {task['due']}</div>
                            </div>
                            <div class="smn-pill">{task['priority']} Priority</div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                if st.button("✅ Mark Complete", key=f"complete-{task['id']}"):
                    _mark_task_complete(task["id"])

        with completed_tab:
            completed = [t for t in st.session_state.nurse_tasks if t["status"] == "completed"]
            if not completed:
                st.info("No completed tasks yet.")
            for task in completed:
                completed_at = task["completed_at"]
                st.markdown(
                    f"""
                    <div class="smn-panel" style="margin-bottom:0.6rem; opacity:0.85;">
                        <strong>{task['title']}</strong>
                        <div class="smn-pill" style="margin-top:0.3rem;">Finished at {completed_at[11:16] if completed_at else '—'}</div>
                        <small style="color:var(--muted); display:block; margin-top:0.3rem;">Priority {task['priority']}</small>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        with add_tab:
            st.markdown("#### Add Task")
            with st.form("add_task_form"):
                task_desc = st.text_input("Task description")
                due_time = st.time_input("Due Time")
                priority = st.selectbox("Priority", ["High", "Medium", "Low"])
                if st.form_submit_button("Add Task"):
                    if not task_desc.strip():
                        st.error("Please provide a description.")
                    else:
                        _add_task(task_desc.strip(), due_time.strftime("%I:%M %p"), priority)

    with vitals_tab:
        record_tab, history_tab = st.tabs(["Record Vitals", "Vitals History"])
        patients = _fetch_patients()
        options = {
            f"{p.get('first_name','')} {p.get('last_name','')} • MRN {p.get('medical_record_number','')}": p.get("id")
            for p in patients
        }

        with record_tab:
            st.markdown("#### Record Vital Signs")
            with st.form("vitals_form"):
                col1, col2 = st.columns(2)
                with col1:
                    patient_label = st.selectbox(
                        "Patient",
                        options.keys() or ["Patient #1"],
                    )
                    patient_id = options.get(patient_label, 1)
                    systolic = st.number_input("BP Systolic", min_value=50, max_value=250, value=120)
                    diastolic = st.number_input("BP Diastolic", min_value=30, max_value=150, value=80)
                    heart_rate = st.number_input("Heart Rate (bpm)", min_value=30, max_value=200, value=72)
                with col2:
                    temperature = st.number_input("Temperature (°F)", min_value=95.0, max_value=106.0, value=98.6, step=0.1)
                    respiratory_rate = st.number_input("Respiratory Rate", min_value=8, max_value=40, value=16)
                    spo2 = st.number_input("SpO₂ (%)", min_value=70, max_value=100, value=98)
                    pain_scale = st.slider("Pain Scale", 0, 10, 0)

                notes = st.text_area("Additional Notes")
                if st.form_submit_button("💾 Save Vitals"):
                    st.session_state.nurse_vitals.append(
                        {
                            "id": str(uuid4()),
                            "patient_id": patient_id,
                            "patient_name": patient_label,
                            "timestamp": datetime.now(),
                            "bp": f"{systolic}/{diastolic}",
                            "heart_rate": heart_rate,
                            "temperature": temperature,
                            "respiratory_rate": respiratory_rate,
                            "spo2": spo2,
                            "pain_scale": pain_scale,
                            "notes": notes,
                        }
                    )
                    st.success("Vital signs recorded securely.")

        with history_tab:
            if not st.session_state.nurse_vitals:
                st.info("No vitals recorded yet.")
            else:
                unique_patients = ["All Patients"] + sorted(
                    {entry["patient_name"] for entry in st.session_state.nurse_vitals}
                )
                selection = st.selectbox("Filter by patient", unique_patients)
                display_entries = st.session_state.nurse_vitals
                if selection != "All Patients":
                    display_entries = [e for e in display_entries if e["patient_name"] == selection]
                for entry in sorted(display_entries, key=lambda e: e["timestamp"], reverse=True):
                    st.markdown(
                        f"""
                        <div class="smn-panel" style="margin-bottom:0.8rem;">
                            <strong>{entry['patient_name']}</strong>
                            <div class="smn-pill" style="margin:0.4rem 0;">
                                {entry['timestamp'].strftime('%b %d, %I:%M %p')}
                            </div>
                            <p style="margin:0.2rem 0;">BP: {entry['bp']} • HR: {entry['heart_rate']} bpm • Temp: {entry['temperature']}°F</p>
                            <p style="margin:0.2rem 0;">RR: {entry['respiratory_rate']} • SpO₂: {entry['spo2']}% • Pain: {entry['pain_scale']}/10</p>
                            <small style="color:var(--muted);">{entry['notes'] or 'No additional notes.'}</small>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
