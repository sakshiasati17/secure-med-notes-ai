import streamlit as st
import requests
from datetime import datetime

from note_templates import show_template_selector
from design_system import (
    st_section_header,
    st_gradient_button,
    st_animated_loader,
    st_card,
)


def _headers():
    if st.session_state.access_token:
        return {"Authorization": f"Bearer {st.session_state.access_token}"}
    return {}


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


def _fetch_notes():
    try:
        resp = requests.get(
            f"{st.session_state.API_BASE_URL}/notes/",
            headers=_headers(),
            timeout=8,
        )
        if resp.status_code == 200:
            return resp.json()
    except Exception as e:
        st.error(f"Error fetching notes: {e}")
    return []


def show():
    st_section_header(
        "Clinical Documentation Studio",
        "Create structured notes, review prior encounters, and search your documentation.",
    )

    patients = _fetch_patients()
    patient_options = {
        f"{p['first_name']} {p['last_name']} (#{p['id']})": p["id"] for p in patients
    }

    create_tab, view_tab, search_tab = st.tabs(
        ["📝 Compose Note", "📋 Notes Library", "🔍 Search"]
    )

    with create_tab:
        st.markdown("###### Select Template")
        show_template_selector()

        with st.form("note_form"):
            top_cols = st.columns([2, 1])
            with top_cols[0]:
                if patient_options:
                    selected_label = st.selectbox("Patient", options=list(patient_options.keys()))
                    patient_id = patient_options[selected_label]
                else:
                    patient_id = st.number_input("Patient ID", min_value=1, value=1)
                note_type = st.selectbox(
                    "Note Type",
                    ["Progress Note", "SOAP Note", "Consultation", "Discharge Summary", "Procedure Note"],
                )
            with top_cols[1]:
                visit_date = st.date_input("Visit Date", value=datetime.now())
                chief_complaint = st.text_input("Chief Complaint")

            st.markdown("###### Structured Fields")
            subjective = st.text_area("Subjective", height=100, placeholder="Patient-reported symptoms...")
            objective = st.text_area("Objective", height=100, placeholder="Clinical findings, vitals...")
            assessment = st.text_area("Assessment", height=100, placeholder="Differential, diagnosis...")
            plan = st.text_area("Plan", height=100, placeholder="Treatment plan, follow-ups...")

            submitted = st.form_submit_button("💾 Save Clinical Note")
            if submitted:
                note_payload = {
                    "patient_id": patient_id,
                    "title": f"{note_type} - {chief_complaint or visit_date.isoformat()}",
                    "content": f"""**Subjective**: {subjective}

**Objective**: {objective}

**Assessment**: {assessment}

**Plan**: {plan}""",
                    # API enum only allows doctor_note / nurse_note
                    "note_type": "doctor_note",
                }
                try:
                    resp = requests.post(
                        f"{st.session_state.API_BASE_URL}/notes/",
                        json=note_payload,
                        headers=_headers(),
                        timeout=10,
                    )
                    if resp.status_code == 200:
                        st.success("✅ Note saved successfully.")
                        st.rerun()
                    else:
                        st.error(f"Failed to save note: {resp.text}")
                except Exception as ex:
                    st.error(f"Error saving note: {ex}")

    with view_tab:
        st.markdown("###### Latest Documentation")
        notes = sorted(
            _fetch_notes(),
            key=lambda n: n.get("created_at", ""),
            reverse=True,
        )
        if not notes:
            st_animated_loader("Fetching notes from the API...")
        for note in notes:
            with st.expander(f"📄 {note.get('title','Untitled')} — {note.get('created_at','')[:10]}"):
                st.write(f"**Patient ID:** {note.get('patient_id')}")
                st.write(f"**Type:** {note.get('note_type', 'N/A')}")
                st.write(f"**Created:** {note.get('created_at')}")
                st.divider()
                st.markdown(note.get("content", ""))

    with search_tab:
        st.markdown("###### Filter & Search")
        search_cols = st.columns([3, 1])
        keyword = search_cols[0].text_input("Keywords")
        filter_type = search_cols[1].selectbox(
            "Note Type",
            ["All", "Progress Note", "SOAP Note", "Consultation", "Discharge Summary", "Procedure Note"],
        )
        if st.button("Run Search"):
            results = [
                note
                for note in _fetch_notes()
                if (keyword.lower() in note.get("content", "").lower() or keyword.lower() in note.get("title", "").lower())
                and (filter_type == "All" or filter_type.lower().replace(" ", "_") == note.get("note_type"))
            ]
            st.info(f"Found {len(results)} matching notes.")
            for note in results[:5]:
                st.markdown(
                    f"""
                    <div class="smn-panel" style="padding:1rem; margin-bottom:0.8rem;">
                        <strong>{note.get('title','Untitled')}</strong>
                        <div class="smn-pill" style="margin:0.4rem 0;">Patient #{note.get('patient_id')}</div>
                        <p style="color:var(--muted); margin:0;">{note.get('content','')[:180]}...</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
