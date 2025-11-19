import streamlit as st
import uuid
from typing import List, Optional

THEME_FLAG = "_smn_theme_loaded"
BASE_FLAG = "_smn_theme_base_loaded"

BASE_CSS = """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

            :root {
                --gradient-start: #667eea;
                --gradient-end: #764ba2;
                --bg: #f8f9fa;
                --surface: #ffffff;
                --text: #0f172a;
                --muted: #6b7280;
                --border: #e2e8f0;
                --success: #198754;
                --warning: #ffc107;
                --danger: #dc3545;
                --info: #0d6efd;
            }

            .stApp {
                background: var(--bg);
                font-family: 'Inter', sans-serif;
                color: var(--text);
            }

            .block-container {
                padding-top: 2rem;
                padding-bottom: 4rem;
            }

            /* Streamlit overrides */
            [data-testid="stMetric"] {
                background: linear-gradient(135deg, rgba(102,126,234,0.1), rgba(118,75,162,0.1));
                border: 1px solid rgba(102,126,234,0.2);
                border-radius: 1.25rem;
                padding: 1rem 1.25rem;
            }

            [data-testid="stMetricLabel"] {
                color: var(--muted);
                font-weight: 600;
                text-transform: uppercase;
                font-size: 0.75rem;
            }

            [data-testid="stMetricValue"] {
                font-size: 2rem;
                font-weight: 700;
                color: var(--text);
            }

            div[data-testid="stTabs"] > div > div {
                gap: 0.5rem;
                background: rgba(15,23,42,0.03);
                padding: 0.4rem;
                border-radius: 999px;
                border: 1px solid rgba(102,126,234,0.25);
            }

            div[data-testid="stTabs"] button {
                padding: 0.65rem 1.6rem;
                background: transparent;
                border-radius: 999px;
                font-weight: 600;
                color: var(--muted);
            }

            div[data-testid="stTabs"] button[aria-selected="true"] {
                background: linear-gradient(135deg, var(--gradient-start), var(--gradient-end));
                color: white;
                box-shadow: 0 8px 24px rgba(102,126,234,0.35);
            }

            div[data-testid="stSidebar"] {
                background: var(--surface);
            }

            /* Buttons */
            div[data-testid="stButton"] > button, button[kind="secondary"] {
                border-radius: 999px;
                background: linear-gradient(135deg, var(--gradient-start), var(--gradient-end));
                color: white;
                font-weight: 600;
                border: none;
                transition: transform 0.2s ease, box-shadow 0.2s ease;
                box-shadow: 0 6px 16px rgba(102,126,234,0.35);
            }

            div[data-testid="stButton"] > button:hover {
                transform: translateY(-1px);
                box-shadow: 0 12px 24px rgba(102,126,234,0.35);
            }

            /* Card styles */
            .smn-card {
                background: var(--surface);
                border-radius: 1.5rem;
                border: 1px solid rgba(15,23,42,0.05);
                padding: 1.25rem;
                box-shadow: 0 12px 30px rgba(15,23,42,0.08);
                transition: transform 0.2s ease, box-shadow 0.2s ease;
            }

            .smn-card:hover {
                transform: translateY(-4px);
                box-shadow: 0 20px 35px rgba(102,126,234,0.18);
            }

            .smn-card h4 {
                margin: 0;
                font-size: 0.9rem;
                font-weight: 600;
                color: var(--muted);
                letter-spacing: 0.04em;
                text-transform: uppercase;
            }

            .smn-card-value {
                font-size: 2.35rem;
                font-weight: 700;
                margin: 0.35rem 0;
            }

            .smn-card-trend {
                font-size: 0.9rem;
                color: var(--success);
                font-weight: 600;
                display: inline-flex;
                align-items: center;
                gap: 0.25rem;
            }

            .smn-panel {
                background: var(--surface);
                border-radius: 1.5rem;
                padding: 1.5rem;
                border: 1px solid rgba(15,23,42,0.05);
                box-shadow: 0 15px 35px rgba(15,23,42,0.08);
            }

            .smn-section-header {
                font-size: 1.5rem;
                font-weight: 700;
                margin-bottom: 0.35rem;
            }

            .smn-section-subtitle {
                color: var(--muted);
                margin-bottom: 1.25rem;
            }

            .smn-patient-card {
                display: flex;
                gap: 1rem;
                background: var(--surface);
                border-radius: 1.5rem;
                border: 1px solid rgba(102,126,234,0.1);
                padding: 1.25rem;
                align-items: center;
                box-shadow: 0 10px 25px rgba(15,23,42,0.08);
                margin-bottom: 0.8rem;
            }

            .smn-patient-card .avatar {
                width: 56px;
                height: 56px;
                border-radius: 50%;
                background: linear-gradient(135deg, var(--gradient-start), var(--gradient-end));
                color: white;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 1.35rem;
                font-weight: 600;
                box-shadow: inset 0 0 10px rgba(255,255,255,0.3);
            }

            .smn-badge {
                padding: 0.35rem 0.85rem;
                border-radius: 999px;
                font-size: 0.85rem;
                font-weight: 600;
                background: rgba(102,126,234,0.12);
                color: var(--gradient-end);
            }

            .smn-pill {
                padding: 0.35rem 0.9rem;
                border-radius: 999px;
                font-size: 0.85rem;
                font-weight: 600;
                display: inline-flex;
                gap: 0.35rem;
                align-items: center;
                background: rgba(15,23,42,0.05);
                color: var(--muted);
            }

            .smn-status-dot {
                width: 10px;
                height: 10px;
                border-radius: 999px;
                display: inline-flex;
                margin-right: 6px;
                box-shadow: 0 0 0 0 rgba(25,135,84,0.5);
                animation: pulse 2s infinite;
            }

            @keyframes pulse {
                0% {
                    box-shadow: 0 0 0 0 rgba(25,135,84,0.4);
                }
                70% {
                    box-shadow: 0 0 0 10px rgba(25,135,84,0);
                }
                100% {
                    box-shadow: 0 0 0 0 rgba(25,135,84,0);
                }
            }

            .smn-hero {
                background: radial-gradient(circle at top left, rgba(102,126,234,0.3), transparent),
                            radial-gradient(circle at top right, rgba(118,75,162,0.25), transparent),
                            linear-gradient(135deg, var(--gradient-start), var(--gradient-end));
                padding: 4.5rem 3rem;
                border-radius: 2rem;
                color: white;
                box-shadow: 0 30px 60px rgba(102,126,234,0.4);
                position: relative;
                overflow: hidden;
            }

            .smn-hero::after {
                content: "";
                position: absolute;
                width: 180px;
                height: 180px;
                border-radius: 999px;
                background: rgba(255,255,255,0.08);
                top: -60px;
                right: -40px;
                filter: blur(2px);
            }

            .smn-feature-strip {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
                gap: 1rem;
                margin-top: 1.5rem;
            }

            .smn-feature-chip {
                background: rgba(255,255,255,0.15);
                border-radius: 1rem;
                padding: 0.85rem 1rem;
                backdrop-filter: blur(10px);
                font-weight: 600;
                display: flex;
                align-items: center;
                gap: 0.5rem;
            }

            .smn-login-card {
                background: var(--surface);
                border-radius: 1.75rem;
                padding: 2rem;
                box-shadow: 0 25px 45px rgba(15,23,42,0.15);
                border: 1px solid rgba(15,23,42,0.05);
            }

            .smn-loader {
                display: inline-flex;
                align-items: center;
                gap: 0.7rem;
                font-weight: 600;
                color: var(--text);
            }

            .smn-loader span {
                width: 10px;
                height: 10px;
                border-radius: 50%;
                background: linear-gradient(135deg, var(--gradient-start), var(--gradient-end));
                display: inline-block;
                animation: bounce 0.8s ease infinite alternate;
            }

            .smn-loader span:nth-child(2) { animation-delay: 0.2s; }
            .smn-loader span:nth-child(3) { animation-delay: 0.4s; }

            @keyframes bounce {
                from { transform: translateY(0); opacity: 0.5; }
                to { transform: translateY(-8px); opacity: 1; }
            }
        </style>
"""


def load_theme():
    mode = st.session_state.get("theme_mode", "light")

    if not st.session_state.get(BASE_FLAG):
        st.markdown(BASE_CSS, unsafe_allow_html=True)
        st.session_state[BASE_FLAG] = True

    if st.session_state.get(THEME_FLAG) == mode:
        return

    palettes = {
        "light": {
            "gradient_start": "#667eea",
            "gradient_end": "#764ba2",
            "bg": "#f8f9fa",
            "surface": "#ffffff",
            "text": "#0f172a",
            "muted": "#6b7280",
            "border": "#e2e8f0",
        },
        "dark": {
            "gradient_start": "#818cf8",
            "gradient_end": "#a855f7",
            "bg": "#0f1117",
            "surface": "rgba(32,33,36,0.92)",
            "text": "#f5f5f5",
            "muted": "#a0a0ac",
            "border": "rgba(255,255,255,0.08)",
        },
    }
    palette = palettes.get(mode, palettes["light"])

    st.markdown(
        f"""
        <style>
            :root {{
                --gradient-start: {palette['gradient_start']};
                --gradient-end: {palette['gradient_end']};
                --bg: {palette['bg']};
                --surface: {palette['surface']};
                --text: {palette['text']};
                --muted: {palette['muted']};
                --border: {palette['border']};
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.session_state[THEME_FLAG] = mode


def st_section_header(title: str, subtitle: Optional[str] = None, icon: Optional[str] = None):
    icon_html = f"<span>{icon}</span>" if icon else ""
    st.markdown(
        f"""
        <div class="smn-section-header">{icon_html} {title}</div>
        {'<div class="smn-section-subtitle">' + subtitle + '</div>' if subtitle else ''}
        """,
        unsafe_allow_html=True,
    )


def st_card(title: str, value: str, trend: Optional[str] = None, icon: Optional[str] = None, color: str = "info"):
    icon_html = f'<div class="smn-pill">{icon}</div>' if icon else ""
    trend_html = f'<div class="smn-card-trend">{trend}</div>' if trend else ""

    st.markdown(
        f"""
        <div class="smn-card">
            <div style="display:flex; justify-content: space-between; align-items:center;">
                <h4>{title}</h4>
                {icon_html}
            </div>
            <div class="smn-card-value">{value}</div>
            {trend_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def st_gradient_button(label: str, icon: Optional[str] = None, key: Optional[str] = None, help_text: Optional[str] = None):
    display = f"{icon or ''} {label}"
    return st.button(display, key=key, help=help_text, use_container_width=True)


def st_status_dot(status: str = "active"):
    color = {
        "active": "var(--success)",
        "warning": "var(--warning)",
        "danger": "var(--danger)",
    }.get(status, "var(--info)")
    return f'<span class="smn-status-dot" style="background:{color};"></span>'


def st_patient_card(name: str, mrn: str, risk: str = "LOW", meta: Optional[str] = None):
    initials = "".join([part[0] for part in name.split()[:2]]).upper()
    meta_html = f"<small style='color:var(--muted);'>{meta}</small>" if meta else ""
    badge_color = {
        "LOW": "rgba(25,135,84,0.15); color:#198754;",
        "MEDIUM": "rgba(255,193,7,0.2); color:#b7791f;",
        "HIGH": "rgba(220,53,69,0.2); color:#dc3545;",
    }.get(risk.upper(), "rgba(15,23,42,0.08); color:var(--muted);")
    st.markdown(
        f"""
        <div class="smn-patient-card">
            <div class="avatar">{initials}</div>
            <div>
                <strong>{name}</strong>
                <div style="display:flex; gap:0.75rem; align-items:center; margin:0.35rem 0;">
                    <span class="smn-pill">MRN {mrn}</span>
                    <span class="smn-pill" style="background:{badge_color}">Risk: {risk.title()}</span>
                </div>
                {meta_html}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def st_animated_loader(message: str):
    st.markdown(
        f"""
        <div class="smn-loader">
            <span></span><span></span><span></span>
            <div>{message}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def st_tabbed_navbar(tabs: List[str], current_tab: str, key: Optional[str] = None) -> str:
    selected = st.radio(
        "Navigation",
        tabs,
        index=tabs.index(current_tab) if current_tab in tabs else 0,
        horizontal=True,
        label_visibility="collapsed",
        key=key or f"nav-{uuid.uuid4()}",
    )
    return selected


def st_gradient_badge(label: str, tone: str = "info"):
    tone_map = {
        "info": "rgba(102,126,234,0.15); color:#4c1d95;",
        "success": "rgba(25,135,84,0.15); color:#198754;",
        "warning": "rgba(255,193,7,0.2); color:#b7791f;",
        "danger": "rgba(220,53,69,0.15); color:#dc3545;",
    }
    style = tone_map.get(tone, tone_map["info"])
    return f"<span class='smn-pill' style='background:{style}'>{label}</span>"


def render_error_page(code: int, message: str, action: Optional[str] = None):
    illustration = "🩺" if code == 404 else "🛠️"
    st.markdown(
        f"""
        <div style="text-align:center; padding:4rem 2rem;">
            <div style="font-size:4rem;">{illustration}</div>
            <h1 style="margin-bottom:0;">{code}</h1>
            <p style="color:var(--muted); font-size:1.1rem;">{message}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if action:
        st_gradient_button(action, icon="↩️", key=f"error-{code}")
