"""
Google Calendar-inspired scheduling system for the Secure Medical Notes UI.
"""
from __future__ import annotations

import calendar
from collections import defaultdict
from datetime import date, datetime, timedelta
from textwrap import dedent
from typing import Dict, List, Optional, Tuple

import requests
import streamlit as st

from design_system import st_card, st_gradient_badge, st_section_header

EVENT_COLORS = {
    "Consultation": "#6366f1",
    "Follow-up": "#0ea5e9",
    "Procedure": "#ec4899",
    "Telehealth": "#10b981",
    "Rounding": "#f59e0b",
}

STATUS_COLORS = {
    "confirmed": "#22c55e",
    "pending": "#f97316",
    "hold": "#eab308",
    "cancelled": "#ef4444",
}

DURATION_OPTIONS = [30, 45, 60, 90, 120]
API_TIMEOUT = 10


def show_calendar_system() -> None:
    """Render the calendar page."""
    if "calendar_date" not in st.session_state:
        st.session_state.calendar_date = datetime.now().replace(
            day=1, hour=0, minute=0, second=0, microsecond=0
        )

    current_month = st.session_state.calendar_date

    st.markdown(_calendar_css(), unsafe_allow_html=True)
    st_section_header(
        "Care Team Calendar",
        "A Google Calendar-style hub for consults, procedures, and follow-ups.",
        icon="📅",
    )

    events, fetch_message, fetch_level = _fetch_appointments(current_month)
    if fetch_message:
        if fetch_level == "info":
            st.info(fetch_message)
        elif fetch_level == "warning":
            st.warning(fetch_message)
        else:
            st.error(fetch_message)
        if fetch_level == "error" and not events:
            events = _generate_mock_events(current_month)

    events_by_day = _group_events_by_day(events)

    _render_calendar_header(current_month)
    _render_metric_row(events, current_month)

    grid_col, agenda_col = st.columns([1.9, 1])

    with grid_col:
        st.markdown(
            "<div class='smn-section-header'>Month at a glance</div>",
            unsafe_allow_html=True,
        )
        _render_month_grid(current_month, events_by_day)
        st.write("")
        _render_followups()

    with agenda_col:
        st.markdown(
            "<div class='smn-section-header'>Today's agenda</div>",
            unsafe_allow_html=True,
        )
        _render_agenda_panel(events)
        st.write("")
        _render_quick_create(current_month)


def _render_calendar_header(current_month: datetime) -> None:
    controls = st.columns([0.4, 0.4, 2.7, 1])
    with controls[0]:
        if st.button("◀", key="calendar-prev"):
            st.session_state.calendar_date = _shift_month(current_month, -1)
            st.rerun()

    with controls[1]:
        if st.button("▶", key="calendar-next"):
            st.session_state.calendar_date = _shift_month(current_month, 1)
            st.rerun()

    with controls[2]:
        st.markdown(
            f"""
            <div class="calendar-month-title">{current_month.strftime('%B %Y')}</div>
            <p class="calendar-month-subtitle">Synced across the whole care team</p>
            """,
            unsafe_allow_html=True,
        )

    with controls[3]:
        if st.button("Today", key="calendar-today"):
            st.session_state.calendar_date = datetime.now().replace(
                day=1, hour=0, minute=0, second=0, microsecond=0
            )
            st.rerun()


def _render_metric_row(events: List[Dict], current_month: datetime) -> None:
    month_events = [
        event
        for event in events
        if event["date"].year == current_month.year and event["date"].month == current_month.month
    ]
    stats = [
        ("Total Appointments", str(len(month_events)), "+5 vs last week", "📋"),
        (
            "Follow-ups",
            str(sum(1 for event in month_events if event["type"] == "Follow-up")),
            "Auto reminders enabled",
            "🔄",
        ),
        (
            "Procedures",
            str(sum(1 for event in month_events if event["type"] == "Procedure")),
            "OR blocks confirmed",
            "🩺",
        ),
        (
            "Telehealth",
            str(sum(1 for event in month_events if event["type"] == "Telehealth")),
            "Remote visits",
            "💻",
        ),
    ]

    cols = st.columns(len(stats))
    for col, (title, value, trend, icon) in zip(cols, stats):
        with col:
            st_card(title, value, trend=trend, icon=icon)


def _render_month_grid(current_month: datetime, events_by_day: Dict[str, List[Dict]]) -> None:
    cal = calendar.Calendar(firstweekday=0)
    weeks = cal.monthdatescalendar(current_month.year, current_month.month)
    html = ["<div class='calendar-grid'>"]

    for day_name in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]:
        html.append(f"<div class='day-label'>{day_name}</div>")

    for week in weeks:
        for day_obj in week:
            html.append(_day_cell_html(day_obj, current_month, events_by_day.get(day_obj.isoformat(), [])))

    html.append("</div>")
    st.markdown("".join(html), unsafe_allow_html=True)


def _render_agenda_panel(events: List[Dict]) -> None:
    today = date.today()
    todays_events = sorted(
        [event for event in events if event["date"].date() == today],
        key=lambda event: event["date"],
    )
    upcoming = sorted(
        [event for event in events if event["date"].date() > today],
        key=lambda event: event["date"],
    )[:3]

    if not todays_events:
        st.markdown(
            "<div class='smn-panel agenda-panel'><p>No events scheduled for today 🎉</p></div>",
            unsafe_allow_html=True,
        )
    else:
        timeline = ["<div class='smn-panel agenda-panel'>"]
        timeline.append("<p class='panel-title'>Today's timeline</p>")
        for event in todays_events:
            timeline.append(_timeline_item_html(event))
        timeline.append("</div>")
        st.markdown("".join(timeline), unsafe_allow_html=True)

    st.write("")
    upcoming_html = ["<div class='smn-panel agenda-panel'>"]
    upcoming_html.append("<p class='panel-title'>Upcoming</p>")
    if not upcoming:
        upcoming_html.append("<p class='empty-state'>No pending events.</p>")
    else:
        for event in upcoming:
            upcoming_html.append(
                dedent(
                    f"""
                    <div class="upcoming-item">
                        <div>
                            <strong>{event['date'].strftime('%a %b %d')}</strong>
                            <p>{event['time_label']} • {event['title']}</p>
                        </div>
                        <span class="smn-pill" style="background:rgba(99,102,241,0.12); color:#4c1d95;">{event['type']}</span>
                    </div>
                    """
                ).strip()
            )
    upcoming_html.append("</div>")
    st.markdown("".join(upcoming_html), unsafe_allow_html=True)


def _render_followups() -> None:
    st.markdown(
        "<div class='smn-section-header'>Follow-up watchlist</div>",
        unsafe_allow_html=True,
    )
    for follow_up in _mock_followups():
        badge = st_gradient_badge(
            f"{follow_up['priority']} priority",
            tone="danger" if follow_up["priority"] == "High" else "warning",
        )
        st.markdown(
            dedent(
                f"""
                <div class="followup-card">
                    <div>
                        <strong>{follow_up['patient']}</strong>
                        <p class="followup-body">{follow_up['condition']}</p>
                        <small>Last visit · {follow_up['last_visit'].strftime('%b %d')}</small>
                    </div>
                    <div style="text-align:right;">
                        {badge}
                        <div class="followup-next">Next: {follow_up['next_followup'].strftime('%b %d')}</div>
                        <small>{follow_up['notes']}</small>
                    </div>
                </div>
                """
            ).strip(),
            unsafe_allow_html=True,
        )


def _render_quick_create(current_month: datetime) -> None:
    st.markdown(
        "<div class='smn-section-header'>Quick slot</div>",
        unsafe_allow_html=True,
    )
    if not st.session_state.get("access_token"):
        st.info("Log in to schedule new appointments and sync with the team calendar.")

    with st.form("quick-create"):
        patient = st.text_input("Patient / MRN")
        title = st.text_input("Visit title", placeholder="e.g., Cardiology Consult")
        visit_type = st.selectbox(
            "Visit type",
            ["Consultation", "Follow-up", "Procedure", "Telehealth", "Rounding"],
        )
        status = st.selectbox(
            "Status",
            ["confirmed", "pending", "hold", "cancelled"],
            format_func=lambda value: value.title(),
        )
        date_value = st.date_input("Date", value=current_month.date())
        time_value = st.time_input(
            "Time",
            value=datetime.now().replace(second=0, microsecond=0).time(),
        )
        duration_minutes = st.selectbox(
            "Duration",
            DURATION_OPTIONS,
            index=DURATION_OPTIONS.index(60),
            format_func=lambda minutes: f"{minutes} min",
        )
        location = st.text_input("Location / modality", value="Telehealth")
        notes = st.text_area("Notes (optional)", height=80)
        submitted = st.form_submit_button("Schedule slot")
        if submitted:
            if not st.session_state.get("access_token"):
                st.error("Please log in to schedule appointments.")
            elif not patient.strip():
                st.error("Please add the patient name or MRN.")
            elif not title.strip():
                st.error("Please add a visit title.")
            else:
                start_dt = _combine_datetime(date_value, time_value)
                end_dt = start_dt + timedelta(minutes=duration_minutes)
                payload = {
                    "title": title.strip(),
                    "patient_name": patient.strip(),
                    "appointment_type": visit_type,
                    "status": status,
                    "location": location.strip() or "Clinic",
                    "start_time": start_dt.isoformat(),
                    "end_time": end_dt.isoformat(),
                    "notes": notes.strip() or None,
                }
                success, message = _submit_appointment(payload)
                if success:
                    st.success("Appointment scheduled.")
                    st.rerun()
                else:
                    st.error(message or "Unable to create appointment.")


def _day_cell_html(day_obj: date, current_month: datetime, events: List[Dict]) -> str:
    classes = ["calendar-day"]
    if day_obj.month != current_month.month:
        classes.append("muted")
    if day_obj == date.today():
        classes.append("today")

    events_html = "".join(_event_pill_html(event) for event in events[:3])
    if len(events) > 3:
        events_html += f"<div class='more-pill'>+{len(events) - 3} more</div>"

    return (
        f"<div class='{' '.join(classes)}'>"
        f"<div class='cell-date'>{day_obj.day}</div>"
        f"{events_html}"
        "</div>"
    )


def _timeline_item_html(event: Dict) -> str:
    status_value = (event.get("status") or "scheduled").lower()
    color = STATUS_COLORS.get(status_value, "#94a3b8")
    type_color = EVENT_COLORS.get(event.get("type", ""), "#64748b")
    status_label = status_value.replace("_", " ").title()
    return (
        dedent(
            f"""
            <div class="timeline-item">
                <div class="timeline-time">{event['time_label']}</div>
                <div class="timeline-dot" style="background:{color};"></div>
                <div>
                    <strong>{event['title']}</strong>
                    <div class="timeline-meta">{event['patient']} • {event['type']}</div>
                    <small style="color:{type_color};">{event['location']} · {status_label}</small>
                </div>
            </div>
            """
        )
        .strip()
    )


def _event_pill_html(event: Dict) -> str:
    border_color = EVENT_COLORS.get(event["type"], "#94a3b8")
    return (
        dedent(
            f"""
            <div class="event-pill" style="border-left:3px solid {border_color};">
                <div class="event-title">{event['title']}</div>
            </div>
            """
        )
        .strip()
    )


def _group_events_by_day(events: List[Dict]) -> Dict[str, List[Dict]]:
    grouped: Dict[str, List[Dict]] = defaultdict(list)
    for event in events:
        grouped[event["date"].date().isoformat()].append(event)

    for day_events in grouped.values():
        day_events.sort(key=lambda event: event["date"])
    return grouped


def _fetch_appointments(current_month: datetime) -> Tuple[List[Dict], Optional[str], Optional[str]]:
    base_url = st.session_state.get("API_BASE_URL")
    if not base_url:
        return [], "API base URL is not configured.", "error"

    if not st.session_state.get("access_token"):
        return [], "Log in to sync the calendar with live appointments.", "info"

    start = current_month.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    end = _shift_month(start, 1) - timedelta(seconds=1)

    try:
        response = requests.get(
            f"{base_url}/appointments",
            params={"start": start.isoformat(), "end": end.isoformat()},
            headers=_auth_headers(),
            timeout=API_TIMEOUT,
        )
    except requests.RequestException as exc:
        return [], f"Unable to reach the scheduling API: {exc}", "error"

    if response.status_code == 200:
        data = response.json()
        events = [_map_api_event(item) for item in data]
        return events, None, None

    if response.status_code == 401:
        return [], "Session expired—please log in again.", "warning"

    if response.status_code == 404:
        return (
            [],
            "Appointments service not found. Restart the API (./start_api.sh) to enable live scheduling.",
            "warning",
        )

    detail = None
    try:
        payload = response.json()
        detail = payload.get("detail")
    except ValueError:
        detail = response.text

    return [], detail or "Unable to load appointments.", "error"


def _map_api_event(payload: Dict) -> Dict:
    start_dt = _parse_datetime(payload.get("start_time"))
    end_dt = _parse_datetime(payload.get("end_time")) or (start_dt + timedelta(minutes=30))
    visit_type = (payload.get("appointment_type") or "Consultation").title()
    status_value = (payload.get("status") or "pending").lower()
    patient = payload.get("patient_name") or "Patient"
    title = payload.get("title") or visit_type

    return {
        "id": payload.get("id"),
        "title": title,
        "patient": patient,
        "location": payload.get("location") or "Clinic",
        "type": visit_type,
        "status": status_value,
        "date": start_dt,
        "end": end_dt,
        "time_label": start_dt.strftime("%I:%M %p"),
        "notes": payload.get("notes"),
    }


def _auth_headers() -> Dict[str, str]:
    token = st.session_state.get("access_token")
    if not token:
        return {}
    return {"Authorization": f"Bearer {token}"}


def _parse_datetime(value) -> datetime:
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        sanitized = value.replace("Z", "+00:00") if value.endswith("Z") else value
        try:
            return datetime.fromisoformat(sanitized)
        except ValueError:
            try:
                base = sanitized.split(".")[0]
                if "+" in sanitized[-6:] or "-" in sanitized[-6:]:
                    suffix = sanitized[-6:]
                    return datetime.fromisoformat(base + suffix)
                return datetime.fromisoformat(base)
            except ValueError:
                pass
    return datetime.now()


def _combine_datetime(day_value: date, time_value) -> datetime:
    naive = datetime.combine(day_value, time_value)
    tz = datetime.now().astimezone().tzinfo
    return naive.replace(tzinfo=tz)


def _submit_appointment(payload: Dict) -> Tuple[bool, Optional[str]]:
    base_url = st.session_state.get("API_BASE_URL")
    if not base_url:
        return False, "API base URL is not configured."

    headers = _auth_headers()
    if not headers:
        return False, "Log in to schedule appointments."

    try:
        response = requests.post(
            f"{base_url}/appointments",
            json=payload,
            headers=headers,
            timeout=API_TIMEOUT,
        )
    except requests.RequestException as exc:
        return False, f"Unable to reach the scheduling API: {exc}"

    if response.status_code == 201:
        return True, None

    detail = None
    try:
        detail = response.json().get("detail")
    except ValueError:
        detail = response.text
    return False, detail or "Failed to schedule appointment."


def _shift_month(current_month: datetime, delta: int) -> datetime:
    month = current_month.month - 1 + delta
    year = current_month.year + month // 12
    month = month % 12 + 1
    return current_month.replace(year=year, month=month, day=1)


def _generate_mock_events(current_month: datetime) -> List[Dict]:
    base = current_month.replace(day=1, hour=8, minute=0, second=0, microsecond=0)
    template = [
        (2, "Cardiology Consult", "Clinic 4A", "Consultation", "John Smith", "09:00", "Confirmed"),
        (2, "Telehealth Diabetes Check", "Virtual Room", "Telehealth", "Maria Lopez", "11:30", "Confirmed"),
        (4, "Post-op Follow-up", "Clinic 2C", "Follow-up", "Ravi Patel", "08:30", "Pending"),
        (5, "Knee Replacement Prep", "OR Block 3", "Procedure", "Marcus Lee", "13:00", "Confirmed"),
        (8, "Neurology Consult", "Clinic 6B", "Consultation", "Grace Kim", "10:15", "Confirmed"),
        (9, "CHF Telehealth", "Virtual Room", "Telehealth", "Evelyn Chen", "15:30", "Hold"),
        (12, "Oncology Rounding", "Inpatient East", "Rounding", "Ward Team", "07:00", "Confirmed"),
        (16, "Diabetes Follow-up", "Clinic 1A", "Follow-up", "Chris Young", "14:00", "Pending"),
        (21, "Cardiac Procedure", "Cath Lab 2", "Procedure", "Tina Rogers", "08:00", "Confirmed"),
        (24, "GI Telehealth", "Virtual Room", "Telehealth", "Sharon Mills", "12:00", "Confirmed"),
        (27, "Post-discharge Check-in", "Clinic 3D", "Follow-up", "Leo Park", "09:45", "Confirmed"),
    ]

    events: List[Dict] = []
    for day_offset, title, location, event_type, patient, time_str, status in template:
        event_date = base + timedelta(days=day_offset - 1)
        hour, minute = [int(part) for part in time_str.split(":")]
        event_dt = event_date.replace(hour=hour, minute=minute)
        events.append(
            {
                "id": f"{event_dt.isoformat()}-{patient}",
                "title": title,
                "patient": patient,
                "location": location,
                "type": event_type,
                "status": status,
                "date": event_dt,
                "time_label": event_dt.strftime("%I:%M %p"),
            }
        )
    return events


def _mock_followups() -> List[Dict]:
    today = date.today()
    return [
        {
            "patient": "Alice Brown",
            "condition": "Hypertension management",
            "last_visit": today - timedelta(days=7),
            "next_followup": today + timedelta(days=2),
            "priority": "High",
            "notes": "Monitor BP trend and adjust meds.",
        },
        {
            "patient": "Bob Wilson",
            "condition": "Type 2 diabetes",
            "last_visit": today - timedelta(days=14),
            "next_followup": today + timedelta(days=5),
            "priority": "Medium",
            "notes": "Review new CGM upload.",
        },
        {
            "patient": "Carol Davis",
            "condition": "Post-surgical wound care",
            "last_visit": today - timedelta(days=3),
            "next_followup": today + timedelta(days=9),
            "priority": "High",
            "notes": "Confirm suture removal plan.",
        },
    ]


def _calendar_css() -> str:
    return """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

        [data-testid="stAppViewContainer"] {
            background: linear-gradient(145deg, #0e0e10, #1b1b1d);
            color: #f5f5f5;
            font-family: 'Inter', 'Poppins', system-ui, sans-serif;
        }

        [data-testid="stSidebar"] {
            background-color: #202124 !important;
            color: #f5f5f5;
        }

        .smn-panel,
        .agenda-panel,
        .followup-card {
            background: #2b2d31;
            border: 1px solid rgba(255, 255, 255, 0.08);
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.25);
            color: #e0e0e0;
        }

        .calendar-month-title {
            font-size: 2rem;
            font-weight: 700;
            margin-bottom: 0.2rem;
            color: #ffffff;
        }

        .calendar-month-subtitle {
            color: #a0a0a0;
            margin: 0;
        }

        .smn-section-header {
            color: #ffffff !important;
        }

        .calendar-grid {
            display: grid;
            grid-template-columns: repeat(7, minmax(0, 1fr));
            gap: 0.45rem;
            background: rgba(255, 255, 255, 0.02);
            padding: 0.9rem;
            border-radius: 1.3rem;
            border: 1px solid rgba(255, 255, 255, 0.08);
            box-shadow: 0 18px 30px rgba(0, 0, 0, 0.35);
        }

        .day-label {
            font-size: 0.75rem;
            text-transform: uppercase;
            font-weight: 600;
            color: #a0a0a0;
            letter-spacing: 0.08em;
        }

        .calendar-day {
            min-height: 90px;
            background: #2b2d31;
            border-radius: 0.8rem;
            padding: 0.55rem;
            border: 1px solid rgba(255, 255, 255, 0.05);
            display: flex;
            flex-direction: column;
            gap: 0.2rem;
            transition: transform 0.2s ease, border 0.2s ease, box-shadow 0.2s ease;
            color: #f5f5f5;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.25);
        }

        .calendar-day:hover {
            transform: translateY(-2px);
            border: 1px solid #764ba2;
            box-shadow: 0 8px 16px rgba(102, 126, 234, 0.35);
        }

        .calendar-day.today {
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.3), rgba(118, 75, 162, 0.3));
            border: 1px solid rgba(118, 75, 162, 0.8);
        }

        .calendar-day.active {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: #ffffff;
            border: 1px solid transparent;
        }

        .calendar-day.muted {
            background: #3a3b3f;
            color: #888888;
        }

        .cell-date {
            font-weight: 600;
            font-size: 0.95rem;
        }

        .event-pill {
            background: rgba(255, 255, 255, 0.08);
            border-radius: 0.75rem;
            padding: 0.25rem 0.45rem;
            font-size: 0.78rem;
            line-height: 1.2;
            color: #f5f5f5;
        }

        .event-title {
            font-weight: 600;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .more-pill {
            font-size: 0.7rem;
            color: #a0a0a0;
            margin-top: auto;
        }

        .panel-title {
            font-weight: 700;
            margin-bottom: 0.8rem;
            color: #ffffff;
        }

        .timeline-item {
            display: flex;
            gap: 0.75rem;
            margin-bottom: 0.9rem;
            align-items: flex-start;
        }

        .timeline-time {
            font-weight: 600;
            min-width: 70px;
            color: #f5f5f5;
        }

        .timeline-dot {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-top: 0.35rem;
        }

        .timeline-meta {
            color: #a0a0a0;
            font-size: 0.85rem;
        }

        .upcoming-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            padding: 0.6rem 0;
            color: #e0e0e0;
        }

        .upcoming-item:last-child {
            border-bottom: none;
        }

        .followup-card {
            display: flex;
            justify-content: space-between;
            gap: 1rem;
            padding: 1rem 1.1rem;
            border-radius: 1rem;
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 12px 25px rgba(0, 0, 0, 0.35);
            color: #f5f5f5;
        }

        .followup-body {
            margin: 0.2rem 0 0.4rem 0;
            color: #e0e0e0;
        }

        .followup-card small {
            color: #a0a0a0;
        }

        .followup-next {
            font-weight: 600;
            margin: 0.25rem 0;
            color: #ffffff;
        }

        .empty-state {
            color: #a0a0a0;
        }

        input, select, textarea, .stTextInput input, .stSelectbox div, .stDateInput input {
            background-color: #2f3136 !important;
            color: #ffffff !important;
            border: 1px solid #444 !important;
            border-radius: 8px !important;
        }

        .priority-high { color: #ff6b6b !important; font-weight: 600; }
        .priority-medium { color: #ffc048 !important; font-weight: 600; }
        .priority-low { color: #51cf66 !important; font-weight: 600; }
    </style>
    """
