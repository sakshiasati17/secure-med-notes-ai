import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime, timezone

from design_system import (
    st_section_header,
    st_card,
    st_gradient_button,
    st_animated_loader,
)


def _headers():
    if st.session_state.access_token:
        return {"Authorization": f"Bearer {st.session_state.access_token}"}
    return {}


def _fetch_notes():
    try:
        resp = requests.get(
            f"{st.session_state.API_BASE_URL}/notes/",
            headers=_headers(),
            timeout=8,
        )
        if resp.status_code == 200:
            return resp.json()
    except Exception:
        pass
    return []


def _fetch_ai_status():
    try:
        resp = requests.get(
            f"{st.session_state.API_BASE_URL}/ai/ai-status",
            headers=_headers(),
            timeout=8,
        )
        if resp.status_code == 200:
            return resp.json()
    except Exception:
        pass
    return {"status": "error"}


def _fetch_high_risk():
    try:
        resp = requests.get(
            f"{st.session_state.API_BASE_URL}/ai/high-risk-patients",
            headers=_headers(),
            timeout=8,
        )
        if resp.status_code == 200:
            return resp.json().get("high_risk_patients", [])
    except Exception:
        pass
    return []


def show_ai_dashboard():
    st_section_header(
        "AI Insights Lab",
        "Operational overview of summarization, risk scoring, and intelligent recommendations.",
    )

    ai_status = _fetch_ai_status()
    status_message = ai_status.get("status", "error").title()
    tone = "✅" if ai_status.get("status") == "operational" else "⚠️"
    st.info(f"{tone} AI Service Status • {status_message}")

    notes = _fetch_notes()

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        [
            "📊 Patient Analytics",
            "🔍 AI Insights",
            "⚠️ Risk Monitoring",
            "📈 Trends & Patterns",
            "🎯 Recommendations",
        ]
    )

    with tab1:
        stats_cols = st.columns(4)
        stats = [
            ("Total Notes", str(len(notes)), None, "🗒️"),
            ("Doctor Notes", str(len([n for n in notes if n.get("note_type") == "doctor_note"])), None, "👨‍⚕️"),
            ("Nurse Notes", str(len([n for n in notes if n.get("note_type") == "nurse_note"])), None, "👩‍⚕️"),
            ("AI Processed", str(len([n for n in notes if n.get("summary")])), None, "🤖"),
        ]
        for col, (title, value, trend, icon) in zip(stats_cols, stats):
            with col:
                st_card(title, value, trend=trend, icon=icon)

        if notes:
            df = pd.DataFrame(notes)
            df["created_at"] = pd.to_datetime(df["created_at"])
            df["date"] = df["created_at"].dt.date
            daily_activity = df.groupby(["date", "note_type"]).size().reset_index(name="count")
            fig = px.bar(
                daily_activity,
                x="date",
                y="count",
                color="note_type",
                title="Daily Note Activity",
            )
            fig.update_layout(paper_bgcolor="white", plot_bgcolor="white")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st_animated_loader("Awaiting documentation to build analytics...")

    with tab2:
        st.markdown("#### AI Summaries & Recommendations")
        left, right = st.columns([2, 1])
        with right:
            if st_gradient_button("Run Full AI Analysis", icon="🚀", key="run-ai"):
                unprocessed = [n for n in notes if not n.get("summary")]
                with st.spinner("Processing notes with AI..."):
                    for note in unprocessed:
                        requests.post(
                            f"{st.session_state.API_BASE_URL}/ai/summarize/{note['id']}",
                            headers=_headers(),
                        )
                st.success(f"Queued {len(unprocessed)} notes for AI summarization.")
                st.experimental_rerun()

        processed_notes = [n for n in notes if n.get("summary")]
        if processed_notes:
            for note in processed_notes[:5]:
                st.markdown(
                    f"""
                    <div class="smn-panel" style="padding:1rem; margin-bottom:0.85rem;">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <strong>{note.get('title','Untitled')}</strong>
                            <span class="smn-pill">Risk: {note.get('risk_level','—')}</span>
                        </div>
                        <p style="color:var(--muted); margin-top:0.3rem;">{note.get('summary','No summary available')}</p>
                        <small style="color:var(--muted);">Created {note.get('created_at','')[:16].replace('T',' ')}</small>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        else:
            st.info("No AI summaries yet. Trigger analysis to generate content.")

    with tab3:
        high_risk = _fetch_high_risk()
        if high_risk:
            level_counts = pd.Series([p.get("risk_level", "HIGH") for p in high_risk]).value_counts()
            fig = px.pie(
                values=level_counts.values,
                names=level_counts.index,
                title="Risk Distribution",
                color_discrete_sequence=px.colors.sequential.RdPu,
            )
            fig.update_layout(paper_bgcolor="white", plot_bgcolor="white")
            st.plotly_chart(fig, use_container_width=True)

            st.markdown("#### Patients Requiring Attention")
            for patient in high_risk:
                st.markdown(
                    f"""
                    <div class="smn-panel" style="margin-bottom:0.8rem;">
                        <strong>{patient.get('patient_name','')}</strong>
                        <div class="smn-pill" style="margin:0.4rem 0;">Risk {patient.get('risk_level','HIGH')}</div>
                        <p style="color:var(--muted); margin:0;">{patient.get('recommendations','Review plan')}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        else:
            st.success("No active high-risk patients flagged by the AI.")

    with tab4:
        if notes:
            df = pd.DataFrame(notes)
            df["created_at"] = pd.to_datetime(df["created_at"])
            df["hour"] = df["created_at"].dt.hour
            df["weekday"] = df["created_at"].dt.day_name()

            col1, col2 = st.columns(2)
            with col1:
                fig = px.bar(
                    df.groupby("hour").size(),
                    title="Notes by Hour",
                    labels={"value": "Notes", "index": "Hour"},
                )
                fig.update_layout(paper_bgcolor="white", plot_bgcolor="white")
                st.plotly_chart(fig, use_container_width=True)
            with col2:
                fig = px.bar(
                    df.groupby("weekday").size(),
                    title="Notes by Weekday",
                    labels={"value": "Notes", "index": "Day"},
                )
                fig.update_layout(paper_bgcolor="white", plot_bgcolor="white")
                st.plotly_chart(fig, use_container_width=True)
        else:
            st_animated_loader("Collecting timeline data...")

    with tab5:
        st.markdown("#### Recommendation Feed")
        if not notes:
            st.info("Once notes are processed, AI-driven recommendations appear here.")
            return

        now = datetime.now(timezone.utc).strftime("%b %d • %I:%M %p")
        recs = [
            ("Monitor escalating hypertension cases", "High-risk patients", now),
            ("Follow-up on pending discharge summaries", "Documentation", now),
            ("Review AI summaries for diabetic cohort", "AI Insights", now),
        ]
        for title, category, timestamp in recs:
            st.markdown(
                f"""
                <div class="smn-panel" style="padding:1rem; margin-bottom:0.75rem;">
                    <strong>{title}</strong>
                    <div style="display:flex; gap:0.5rem; margin:0.35rem 0;">
                        <span class="smn-pill">{category}</span>
                        <span class="smn-pill">Updated {timestamp}</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
