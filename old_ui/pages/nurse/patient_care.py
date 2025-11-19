import streamlit as st
import requests
from datetime import datetime, timedelta

from design_system import (
    st_section_header,
    st_patient_card,
    st_card,
    st_gradient_button,
)


st.markdown(
    """
    <style>
    /* Patient Cards */
    .patient-card, [class*="stCard"], [data-testid="stVerticalBlock"] > div {
        background: rgba(40, 42, 46, 0.9) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255,255,255,0.05) !important;
        box-shadow: 0 2px 12px rgba(0,0,0,0.3) !important;
        color: #f5f5f5 !important;
        transition: 0.25s ease;
        position: relative;
        overflow: hidden;
        margin-bottom: 1.2rem;
    }

    .patient-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 18px rgba(0,0,0,0.45) !important;
    }

    .patient-card::after {
        content: "";
        position: absolute;
        bottom: -8px;
        left: 10%;
        right: 10%;
        height: 2px;
        background: linear-gradient(90deg, rgba(102,126,234,0), rgba(102,126,234,0.8), rgba(102,126,234,0));
        opacity: 0.5;
    }

    /* Risk Colors */
    .low-risk { color: #51cf66 !important; font-weight: 600; }
    .medium-risk { color: #ffc048 !important; font-weight: 600; }
    .high-risk { color: #ff6b6b !important; font-weight: 600; }

    /* Text Adjustments */
    p, span, label {
      color: #e0e0e0 !important;
    }
    h2, h3 {
      color: #ffffff !important;
    }

    /* Metrics Section */
    .metrics-container, [class*="metrics"], [class*="summary"] {
      background: transparent !important;
      box-shadow: none !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
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


def _build_shift_report(patients_snapshot):
    if not patients_snapshot:
        return "No patient data available for this shift."

    timestamp = datetime.now().strftime("%b %d, %Y • %I:%M %p")
    lines = [
        f"# Nurse Shift Report",
        f"**Generated:** {timestamp}",
        f"**Total Assigned Patients:** {len(patients_snapshot)}",
        "",
        "| Patient | MRN | Room | Risk | Next Check | Notes |",
        "| --- | --- | --- | --- | --- | --- |",
    ]

    for p in patients_snapshot:
        lines.append(
            f"| {p['name']} | {p['mrn']} | {p['room']} | {p['risk']} | {p['next_check']} | {p['notes']} |"
        )

    lines.extend(
        [
            "",
            "### Summary",
            f"- Vitals logged: {32}",
            f"- Medications administered: {18}",
            f"- Outstanding escalations: {2}",
            "",
            "_Auto-generated from Patient Care Hub._",
        ]
    )
    return "\n".join(lines)


def show():
    """Nurse Patient Care Page"""
    st_section_header(
        "Patient Care Hub",
        "Track assignments, vitals, medications, and care plans in one workspace.",
    )

    patients = _fetch_patients()[:5]
    if not patients:
        st.info("No patient data available.")
        return

    st.markdown("#### Care Metrics")
    metric_data = [
        ("Vitals Logged", "32", "🩺"),
        ("Meds Administered", "18", "💊"),
        ("Tasks Completed", "21", "✅"),
        ("Rounds Completed", "14", "🚶‍♀️"),
        ("Open Escalations", "2", "🚨"),
        ("Care Plans Updated", "9", "📘"),
    ]
    for i in range(0, len(metric_data), 3):
        row = st.columns(3)
        for col, (label, value, icon) in zip(row, metric_data[i : i + 3]):
            with col:
                st_card(label, value, icon=icon)

    st.markdown("#### Assigned Patients")
    risk_labels = ["LOW", "MEDIUM", "HIGH"]
    risk_classes = {"LOW": "low-risk", "MEDIUM": "medium-risk", "HIGH": "high-risk"}
    cols_per_row = 3
    cols = st.columns(cols_per_row)
    patient_snapshots = []
    for idx, patient in enumerate(patients):
        column = cols[idx % cols_per_row]
        with column:
            name = f"{patient.get('first_name','')} {patient.get('last_name','')}".strip() or "Patient"
            mrn = patient.get("medical_record_number", "MRN")
            meta = patient.get("medical_history", "General care plan")
            risk = risk_labels[idx % 3]
            next_check = (datetime.now() + timedelta(hours=2 + idx)).strftime("%I:%M %p")
            room = 200 + idx
            patient_snapshots.append(
                {
                    "name": name,
                    "mrn": mrn,
                    "risk": risk,
                    "next_check": next_check,
                    "room": room,
                    "notes": meta[:80] + ("..." if len(meta) > 80 else ""),
                }
            )
            st.markdown(
                f"""
                <div class="nurse-patient-box patient-card">
                    <h4>{name}</h4>
                    <p class="nurse-patient-meta" style="color:#b0b0b0;">MRN {mrn}</p>
                    <div class="smn-pill {risk_classes[risk].replace('-', ' ')}" style="margin-bottom:0.6rem; background:rgba(255,255,255,0.08);">
                        <span class="{risk_classes[risk]}">{risk.title()} risk</span>
                    </div>
                    <p style="color:#b0b0b0; margin-bottom:0.6rem;">{meta[:120]}{'...' if len(meta) > 120 else ''}</p>
                    <div style="display:flex; gap:0.4rem; flex-wrap:wrap;">
                        <span class="smn-pill" style="background:rgba(255,255,255,0.05); color:#f5f5f5;">
                            Next check: {next_check}
                        </span>
                        <span class="smn-pill" style="background:rgba(255,255,255,0.05); color:#f5f5f5;">
                            Room {room}
                        </span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("#### Care Timeline")
    timeline_items = [
        ("08:00", "Initial assessment", "Room 204"),
        ("10:30", "Medication pass", "Room 207"),
        ("12:00", "Vitals + I/O", "Room 205"),
        ("14:30", "Wound care", "Room 208"),
    ]
    for time, title, location in timeline_items:
        st.markdown(
            f"""
            <div class="smn-panel" style="padding:0.9rem 1rem; margin-bottom:0.6rem;">
                <strong>{time}</strong> — {title}
                <div class="smn-pill" style="margin-top:0.4rem;">{location}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("#### Care Actions")
    action_cols = st.columns(3)
    buttons = [
        ("Document Shift Report", "📝"),
        ("Update MAR", "💊"),
        ("Record Intake/Output", "💧"),
    ]
    for col, (label, icon) in zip(action_cols, buttons):
        with col:
            if st_gradient_button(label, icon=icon, key=f"care-{label}"):
                if label == "Document Shift Report":
                    report = _build_shift_report(patient_snapshots)
                    st.success("Shift report generated below.")
                    st.markdown(report)
                    st.download_button(
                        "Download Shift Report",
                        data=report,
                        file_name=f"shift-report-{datetime.now().strftime('%Y%m%d-%H%M')}.md",
                        mime="text/markdown",
                        key="download-shift-report",
                    )
                else:
                    st.info(f"{label} shortcut coming soon.")
