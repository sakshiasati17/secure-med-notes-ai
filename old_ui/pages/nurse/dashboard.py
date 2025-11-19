import streamlit as st
from design_system import (
    st_section_header,
    st_card,
    st_gradient_button,
    st_patient_card,
)


def _navigate_to(tab: str):
    st.session_state["next_nurse_nav"] = tab
    st.rerun()


def show():
    """Nurse Dashboard Page"""
    st_section_header(
        "Nurse Command Center",
        "Monitor assignments, tasks, vitals, and medication schedules at a glance.",
    )

    stats = [
        ("Assigned Patients", "12", "+3 today", "🧑‍🤝‍🧑"),
        ("Tasks Pending", "8", "updated 5m ago", "📋"),
        ("Vitals Due", "5", "due this hour", "🩺"),
        ("Medications Due", "15", "next 2 hours", "💊"),
    ]
    cols = st.columns(4)
    for col, (title, value, trend, icon) in zip(cols, stats):
        with col:
            st_card(title, value, trend=trend, icon=icon)

    st.write("")
    left, right = st.columns([1.8, 1])

    with left:
        st.markdown("#### Today's Timeline")
        tasks = [
            ("10:00 AM", "Vitals check — Room 305", "danger"),
            ("10:30 AM", "Medication administration — Room 307", "danger"),
            ("11:00 AM", "Patient education — Room 310", "warning"),
            ("02:00 PM", "Wound dressing — Room 312", "warning"),
            ("03:30 PM", "Discharge prep — Room 305", "success"),
        ]
        for time, task, tone in tasks:
            color = {
                "danger": "#dc3545",
                "warning": "#ffc107",
                "success": "#198754",
            }[tone]
            st.markdown(
                f"""
                <div class="smn-panel" style="padding:0.8rem 1rem; margin-bottom:0.6rem; border-left:4px solid {color};">
                    <strong style="color:{color};">{time}</strong><br/>
                    <span style="color:var(--muted);">{task}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

    with right:
        st.markdown("#### Completion Snapshot")
        st.metric("Tasks Completed", "14", "+4 today")
        st.metric("Overdue Tasks", "3", "needs attention")
        st.metric("Completion Rate", "86%", "")

        st.markdown("#### Assigned Patients")
        sample_patients = [
            ("John Smith", "MRN-2021", "HIGH", "Post-op, frequent vitals"),
            ("Mary Johnson", "MRN-2022", "MEDIUM", "Medication adjustments"),
        ]
        for name, mrn, risk, meta in sample_patients:
            st_patient_card(name, mrn, risk=risk, meta=meta)

    st.write("")
    st.markdown("#### Quick Actions")
    actions = [
        ("Add Note", "📝", "📋 Notes & Tasks"),
        ("Record Vitals", "🩺", "📋 Notes & Tasks"),
        ("Medication Log", "💊", "📊 Patient Care"),
        ("View Tasks", "📋", "📋 Notes & Tasks"),
    ]
    quick_cols = st.columns(4)
    for col, (label, icon, target_tab) in zip(quick_cols, actions):
        with col:
            if st_gradient_button(label, icon=icon, key=f"nurse-{label}"):
                _navigate_to(target_tab)
