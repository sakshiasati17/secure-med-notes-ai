import streamlit as st
import requests
from datetime import datetime

from design_system import (
    st_card,
    st_section_header,
    st_gradient_button,
    st_patient_card,
    st_animated_loader,
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


def show():
    """Doctor Dashboard Page"""
    st_section_header("Clinical Command Center", "Real-time intelligence for your patient panel.")

    stats = [
        ("Total Patients", "5", "+2 this week", "👥"),
        ("Active Notes", "73", "+15 today", "📝"),
        ("High Risk", "2", "Requires review", "⚠️"),
        ("Pending Reviews", "8", "Due today", "📋"),
    ]
    cols = st.columns(4)
    for col, (title, value, trend, icon) in zip(cols, stats):
        with col:
            st_card(title, value, trend=trend, icon=icon)

    st.write("")
    left, right = st.columns([1.3, 1])

    with left:
        st.markdown("<div class='smn-section-header'>Recent Notes</div>", unsafe_allow_html=True)
        notes = _fetch_notes()[:5]
        if not notes:
            st_animated_loader("Waiting for new documentation...")
        for note in notes:
            created = note.get("created_at", "")[:16].replace("T", " ")
            st.markdown(
                f"""
                <div class="smn-panel" style="padding:1rem; margin-bottom:0.8rem;">
                    <strong>{note.get('title','Untitled')}</strong>
                    <div class="smn-pill" style="margin:0.4rem 0;">Patient #{note.get('patient_id','–')}</div>
                    <small style="color:var(--muted);">{created}</small>
                    <p style="margin-top:0.5rem; color:var(--muted);">{note.get('summary') or note.get('content','')[:140]}...</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    with right:
        st.markdown("<div class='smn-section-header'>High-Risk Patients</div>", unsafe_allow_html=True)
        critical_patients = [
            {"name": "John Doe", "mrn": "MRN-1134", "risk": "HIGH", "meta": "Post-surgical monitoring"},
            {"name": "Jane Smith", "mrn": "MRN-1188", "risk": "MEDIUM", "meta": "Diabetes complications"},
            {"name": "Marcus Lee", "mrn": "MRN-1320", "risk": "HIGH", "meta": "CHF readmission risk"},
        ]
        for patient in critical_patients:
            st_patient_card(
                patient["name"],
                patient["mrn"],
                risk=patient["risk"],
                meta=patient["meta"],
            )

    st.write("")
    st.markdown("<div class='smn-section-header'>Quick Actions</div>", unsafe_allow_html=True)
    action_cols = st.columns(4)
    actions = [
        ("New Clinical Note", "📝", "Navigate to Clinical Notes tab"),
        ("View Patient List", "👥", "Navigate to Patients tab"),
        ("Run AI Analysis", "🤖", "Open AI & Analytics tab"),
        ("Generate Report", "📊", "Coming soon"),
    ]
    for col, (label, icon, message) in zip(action_cols, actions):
        with col:
            if st_gradient_button(label, icon=icon, key=f"qa-{label}"):
                st.info(message)
