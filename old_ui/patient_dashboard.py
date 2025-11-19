import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime

from design_system import (
    st_section_header,
    st_card,
    st_patient_card,
    st_gradient_button,
    st_gradient_badge,
    st_tabbed_navbar,
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


def _calculate_age(dob: str) -> int:
    try:
        birth = datetime.strptime(dob, "%Y-%m-%d")
        return (datetime.now() - birth).days // 365
    except Exception:
        return 0


def _select_patient(patients, query):
    if not query:
        return None
    if query.isdigit():
        for patient in patients:
            if str(patient.get("id")) == query:
                return patient
    lowered = query.lower()
    for patient in patients:
        full_name = f"{patient.get('first_name','')} {patient.get('last_name','')}".lower()
        if lowered in full_name:
            return patient
    return None


def show_patient_dashboard():
    st_section_header(
        "Patient Intelligence Workspace",
        "Search, triage, and analyze every patient from one secure dashboard.",
    )

    patients = _fetch_patients()
    if not patients:
        st.info("No patients found. Use the API to seed sample data.")
        return

    # No longer track selected patient; detail panel shows all patients.

    search_col, btn_col = st.columns([3, 1])
    query = search_col.text_input("Search by ID or Name", placeholder="e.g. 4 or Jane")
    selected_patient = None
    if btn_col.button("🔎 Search"):
        selected_patient = _select_patient(patients, query)
        if selected_patient:
            st.success(f"✅ Located {selected_patient.get('first_name','')} {selected_patient.get('last_name','')}")
        else:
            st.warning("No patient matched that query.")

    nav_items = ["📊 Overview", "🏥 Patient Detail", "📈 Analytics"]
    current_tab = st.session_state.get("patient_dashboard_nav", nav_items[0])
    selected_tab = st_tabbed_navbar(
        nav_items, current_tab=current_tab, key="patient-dashboard-nav"
    )
    st.session_state.patient_dashboard_nav = selected_tab

    if selected_tab == "📊 Overview":
        stats = [
            ("Active Patients", str(len(patients)), "+3 this week", "👥"),
            ("Chronic Care", "18", "engaged", "🩺"),
            ("High Risk", "4", "requires review", "⚠️"),
            ("Upcoming Visits", "12", "next 7 days", "📅"),
        ]
        cols = st.columns(4)
        for col, (title, value, trend, icon) in zip(cols, stats):
            with col:
                st_card(title, value, trend=trend, icon=icon)

        st.write("")
        grid_cols = st.columns(3)
        for idx, patient in enumerate(patients[:6]):
            with grid_cols[idx % 3]:
                name = f"{patient.get('first_name','')} {patient.get('last_name','')}"
                mrn = patient.get("medical_record_number", "MRN-0000")
                risk = ["LOW", "MEDIUM", "HIGH"][idx % 3]
                st_patient_card(
                    name,
                    mrn,
                    risk=risk,
                    meta=f"{patient.get('medical_history', 'General Care')[:60]}...",
                )

    if selected_tab == "🏥 Patient Detail":
        st_section_header("Comprehensive Patient Details", "All patient records in one view.")

        notes_lookup = {}
        try:
            notes_resp = requests.get(
                f"{st.session_state.API_BASE_URL}/notes/",
                headers=_headers(),
                timeout=8,
            )
            if notes_resp.status_code == 200:
                for note in notes_resp.json():
                    notes_lookup.setdefault(note.get("patient_id"), []).append(note)
        except Exception:
            pass

        for idx, patient in enumerate(patients):
            name = f"{patient.get('first_name','')} {patient.get('last_name','')}"
            st.markdown(
                f"""
                <div class="smn-panel" style="margin-bottom:1.25rem; border-left:4px solid rgba(102,126,234,0.35);">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <div>
                            <div class="smn-pill">MRN {patient.get('medical_record_number','N/A')}</div>
                            <h3 style="margin:0.2rem 0;">{name}</h3>
                        </div>
                        <div class="smn-pill">Age {_calculate_age(patient.get('date_of_birth','1980-01-01'))}</div>
                    </div>
                """,
                unsafe_allow_html=True,
            )

            info_cols = st.columns(4)
            details = [
                ("Allergies", patient.get("allergies", "None")),
                ("Patient ID", str(patient.get("id", "N/A"))),
                ("DOB", patient.get("date_of_birth", "N/A")),
                ("History", patient.get("medical_history", "No history recorded")),
            ]
            for col, (title, value) in zip(info_cols, details):
                with col:
                    st_card(title, value, icon="ℹ️")

            patient_notes = notes_lookup.get(patient.get("id"), [])
            if patient_notes:
                st.markdown("**Recent Notes**")
                for note in patient_notes[:2]:
                    st.markdown(
                        f"""
                        <div class="smn-panel" style="padding:0.9rem; margin-bottom:0.5rem;">
                            <strong>{note.get('title','Untitled')}</strong>
                            <div style="display:flex; gap:0.6rem; margin:0.3rem 0;">
                                {st_gradient_badge(note.get('note_type','note').title())}
                                <span class="smn-pill">{note.get('created_at','')[:10]}</span>
                            </div>
                            <p style="color:var(--muted); margin:0;">{note.get('content','')[:160]}...</p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown(
                "<div style='height:1px; background:rgba(102,126,234,0.35); margin:0.8rem 0;'></div>",
                unsafe_allow_html=True,
            )

    if selected_tab == "📈 Analytics":
        analytics_df = pd.DataFrame(
            [
                {
                    "name": f"{p.get('first_name','')} {p.get('last_name','')}",
                    "age": _calculate_age(p.get("date_of_birth", "1980-01-01")),
                    "risk": ["Low", "Medium", "High"][idx % 3],
                    "medical_history": p.get("medical_history", "General Care"),
                }
                for idx, p in enumerate(patients)
            ]
        )

        st.markdown("#### Population Insights")
        metric_cols = st.columns(3)
        with metric_cols[0]:
            st_card("Median Age", f"{int(analytics_df['age'].median())}", icon="🎂")
        with metric_cols[1]:
            st_card("High-Risk Cohort", f"{(analytics_df['risk'] == 'High').sum()}", icon="⚠️")
        with metric_cols[2]:
            chronic_share = int(
                (analytics_df['medical_history'].str.contains("diabetes|hypertension|copd|asthma", case=False).mean())
                * 100
            )
            st_card("Chronic Condition %", f"{chronic_share}%", icon="🧬")

        chart_col1, chart_col2 = st.columns(2)
        with chart_col1:
            st.markdown("##### Risk Distribution")
            fig = px.pie(
                analytics_df,
                names="risk",
                color="risk",
                color_discrete_map={"Low": "#4cc9f0", "Medium": "#f9c74f", "High": "#f94144"},
            )
            fig.update_traces(
                textposition="inside",
                textinfo="percent+label",
                textfont=dict(color="#0f172a", size=12),
            )
            fig.update_layout(paper_bgcolor="white", plot_bgcolor="white", font_color="#0f172a")
            st.plotly_chart(fig, use_container_width=True)

        with chart_col2:
            st.markdown("##### Age Spectrum")
            fig = px.histogram(
                analytics_df,
                x="age",
                nbins=10,
                color_discrete_sequence=["#7b2cbf"],
            )
            fig.update_layout(
                paper_bgcolor="white",
                plot_bgcolor="white",
                font_color="#0f172a",
                bargap=0.1,
                xaxis=dict(color="#475569"),
                yaxis=dict(color="#475569"),
            )
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("##### Condition Frequency")
        condition_counts = {}
        for history in analytics_df["medical_history"]:
            for condition in [c.strip() for c in history.split(",") if c.strip()]:
                condition_counts[condition] = condition_counts.get(condition, 0) + 1
        if condition_counts:
            condition_df = (
                pd.DataFrame(condition_counts.items(), columns=["Condition", "Count"])
                .sort_values("Count", ascending=False)
                .head(7)
            )
            fig = px.bar(
                condition_df,
                x="Condition",
                y="Count",
                color="Count",
                color_continuous_scale="PuBu",
            )
            fig.update_coloraxes(colorbar=dict(title="Count", tickfont=dict(color="#0f172a")))
            fig.update_layout(
                paper_bgcolor="white",
                plot_bgcolor="white",
                font_color="#0f172a",
                xaxis=dict(color="#475569"),
                yaxis=dict(color="#475569"),
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No condition data available.")

        st.markdown("##### Risk vs Age Correlation")
        risk_map = {"Low": 1, "Medium": 2, "High": 3}
        scatter_df = analytics_df.assign(risk_score=analytics_df["risk"].map(risk_map))
        fig = px.scatter(
            scatter_df,
            x="age",
            y="risk_score",
            color="risk",
            color_discrete_map={"Low": "#4cc9f0", "Medium": "#f9c74f", "High": "#f94144"},
            hover_data=["name"],
        )
        fig.update_layout(
            yaxis=dict(
                tickmode="array",
                tickvals=[1, 2, 3],
                ticktext=["Low", "Medium", "High"],
                color="#475569",
            ),
            paper_bgcolor="white",
            plot_bgcolor="white",
            font_color="#0f172a",
            xaxis=dict(color="#475569"),
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("##### Follow-up Outlook")
        followup_data = {
            "Patient": analytics_df["name"].head(5),
            "Next Follow-up": pd.date_range(datetime.now(), periods=5, freq="7D").strftime("%Y-%m-%d"),
            "Priority": ["Routine", "High", "Routine", "Medium", "Routine"],
        }
        followup_df = pd.DataFrame(followup_data)
        st.dataframe(followup_df, use_container_width=True, hide_index=True)
