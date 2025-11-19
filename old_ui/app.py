import streamlit as st
import requests
from datetime import datetime

from design_system import (
    load_theme,
    st_status_dot,
    st_gradient_button,
    st_section_header,
    st_tabbed_navbar,
)

from language_support import init_language, show_language_selector

from pages.doctor import (
    dashboard as doctor_dashboard,
    patients as doctor_patients,
    clinical_notes as doctor_notes,
    ai_analytics as doctor_ai,
    more as doctor_more,
)

from pages.nurse import (
    dashboard as nurse_dashboard,
    patient_care as nurse_patient_care,
    notes_tasks as nurse_notes_tasks,
    calendar as nurse_calendar,
)


# --- Page Configuration ---
st.set_page_config(
    page_title="Secure Medical Notes AI",
    page_icon="🏥",
    layout="wide",
)

load_theme()
init_language()


def init_state():
    defaults = {
        "access_token": None,
        "user_role": None,
        "user_name": "",
        "show_login_page": False,
        "API_BASE_URL": "http://localhost:8000",
        "theme_mode": "light",
    }
    for key, value in defaults.items():
        st.session_state.setdefault(key, value)


init_state()


def make_api_request(endpoint: str, method: str = "GET", data=None):
    url = f"{st.session_state.API_BASE_URL}{endpoint}"
    headers = {}
    if st.session_state.access_token:
        headers["Authorization"] = f"Bearer {st.session_state.access_token}"

    try:
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers, timeout=10)
        elif method == "PUT":
            response = requests.put(url, json=data, headers=headers, timeout=10)
        else:
            raise ValueError("Unsupported HTTP method")

        if response.status_code in (200, 201):
            return response.json()
        st.error(f"API Error {response.status_code}: {response.text}")
    except requests.exceptions.ConnectionError:
        st.error("Unable to reach API. Ensure FastAPI is running on port 8000.")
    except Exception as ex:
        st.error(f"Unexpected error: {ex}")
    return None


def guess_role(email: str) -> str:
    lowered = email.lower()
    if "nurse" in lowered:
        return "nurse"
    if "admin" in lowered:
        return "admin"
    return "doctor"


def login_user(email: str, password: str):
    payload = {"email": email, "password": password}
    response = make_api_request("/auth/login", method="POST", data=payload)
    if response:
        st.session_state.access_token = response["access_token"]
        st.session_state.user_name = email.split("@")[0].replace(".", " ").title()
        st.session_state.user_role = guess_role(email)
        st.session_state.show_login_page = False
        st.success("✅ Login successful. Secure session established.")
        st.rerun()


def logout_user():
    st.session_state.access_token = None
    st.session_state.user_role = None
    st.session_state.user_name = ""
    st.session_state.show_login_page = False


def render_sidebar():
    with st.sidebar:
        st.markdown("### ⚙️ Environment")
        st.write(f"API: {st.session_state.API_BASE_URL}")
        st.write("PostgreSQL → port 5434")
        st.write("Redis → port 6379")
        st.divider()
        show_language_selector()
        st.divider()
        st.markdown(
            """
            **Demo Credentials**

            • Doctor — `dr.williams@hospital.com` / `password123`  
            • Nurse — `nurse.davis@hospital.com` / `password123`
            """,
        )


def render_welcome():
    st.markdown(
        """
        <div class="smn-hero">
            <div class="smn-pill">HIPAA-Compliant • AI Accelerated</div>
            <h1 style="font-size:3.2rem; margin:0.6rem 0;">Secure Medical Notes AI</h1>
            <p style="font-size:1.2rem;">Secure. Smart. Simplified Medical Documentation.</p>
            <div class="smn-feature-strip">
                <div class="smn-feature-chip">🔐 Enterprise Security</div>
                <div class="smn-feature-chip">🤖 AI Summarization</div>
                <div class="smn-feature-chip">☁️ Encrypted Cloud</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        if st_gradient_button("Login to Get Started", icon="🚀", key="welcome_login"):
            st.session_state.show_login_page = True
            st.rerun()


def render_login():
    st_section_header("🔐 Secure Login", "Select your role and authenticate to continue.")

    role_choice = st.radio(
        "Login context",
        ["Doctor Workspace", "Nurse Workspace"],
        horizontal=True,
        key="login_role_choice",
    )

    with st.form("login_form"):
        email = st.text_input("Email Address")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("🚀 Login")
        if submitted:
            login_user(email, password)

    st.markdown("###### Quick Access")
    quick_cols = st.columns(2)
    with quick_cols[0]:
        if st.button("👨‍⚕️ Doctor Login", use_container_width=True):
            login_user("dr.williams@hospital.com", "password123")
    with quick_cols[1]:
        if st.button("👩‍⚕️ Nurse Login", use_container_width=True):
            login_user("nurse.davis@hospital.com", "password123")

    if st.button("← Back to welcome", key="back_to_welcome"):
        st.session_state.show_login_page = False
        st.rerun()


def render_top_nav():
    toggle_col, _ = st.columns([1, 5])
    with toggle_col:
        dark_enabled = st.toggle(
            "🌙 Dark Mode",
            value=st.session_state.get("theme_mode", "light") == "dark",
        )
    desired_mode = "dark" if dark_enabled else "light"
    if desired_mode != st.session_state.get("theme_mode"):
        st.session_state["theme_mode"] = desired_mode
        load_theme()

    top_left, top_right = st.columns([4, 1])
    with top_left:
        st.markdown(
            f"""
            <div class="smn-panel">
                <div class="smn-pill">{st_status_dot('active')} Session Active</div>
                <h2 style="margin:0.2rem 0;">👋 Hello, {st.session_state.user_name or 'Clinician'}</h2>
                <p style="color:var(--muted); margin:0;">Secure workspace • {st.session_state.user_role.title()}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with top_right:
        st.markdown(
            f"""
            <div class="smn-panel" style="text-align:right;">
                <div class="smn-pill">🕒 {datetime.now().strftime('%b %d, %I:%M %p')}</div>
                <p style="margin:0; color:var(--muted);">HIPAA Mode</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("🚪 Logout", key="logout_btn"):
            logout_user()
            st.rerun()


def render_doctor_workspace():
    nav_items = [
        "🏥 Dashboard",
        "👥 Patients",
        "📋 Clinical Notes",
        "🤖 AI & Analytics",
        "📅 Calendar",
    ]
    current = st.session_state.get("doctor_nav", nav_items[0])
    selection = st_tabbed_navbar(nav_items, current_tab=current, key="doctor-nav")
    st.session_state["doctor_nav"] = selection

    if selection == "🏥 Dashboard":
        doctor_dashboard.show()
    elif selection == "👥 Patients":
        doctor_patients.show()
    elif selection == "📋 Clinical Notes":
        doctor_notes.show()
    elif selection == "🤖 AI & Analytics":
        doctor_ai.show()
    else:
        doctor_more.show()


def render_nurse_workspace():
    nav_items = [
        "🏥 Dashboard",
        "📊 Patient Care",
        "📋 Notes & Tasks",
        "📅 Calendar",
    ]
    if "next_nurse_nav" in st.session_state:
        st.session_state["nurse_nav"] = st.session_state.pop("next_nurse_nav")
    current = st.session_state.get("nurse_nav", nav_items[0])
    selection = st_tabbed_navbar(nav_items, current_tab=current, key="nurse-nav")
    st.session_state["nurse_nav"] = selection

    if selection == "🏥 Dashboard":
        nurse_dashboard.show()
    elif selection == "📊 Patient Care":
        nurse_patient_care.show()
    elif selection == "📋 Notes & Tasks":
        nurse_notes_tasks.show()
    else:
        nurse_calendar.show()


def render_authenticated_workspace():
    render_top_nav()
    if st.session_state.user_role == "nurse":
        render_nurse_workspace()
    else:
        render_doctor_workspace()


def main():
    render_sidebar()

    if not st.session_state.access_token:
        if st.session_state.show_login_page:
            render_login()
        else:
            render_welcome()
    else:
        render_authenticated_workspace()


if __name__ == "__main__":
    main()
