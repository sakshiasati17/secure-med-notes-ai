import streamlit as st
import requests
import json
from datetime import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configure page - MUST be first Streamlit command
st.set_page_config(
    page_title="Secure Medical Notes AI",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"  # Ensure sidebar is always visible
)

# Import new modules
try:
    from ai_dashboard import show_ai_dashboard
    from calendar_system import show_calendar_system
    from notifications import show_notifications
    from note_templates import show_template_selector
    from language_support import show_language_selector, get_text, init_language
    from patient_dashboard import show_patient_dashboard
    from nurse_workspace import show_nurse_workspace
except ImportError:
    # If running from different directory
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
    from ai_dashboard import show_ai_dashboard
    from calendar_system import show_calendar_system
    from notifications import show_notifications
    from note_templates import show_template_selector
    from language_support import show_language_selector, get_text, init_language
    from patient_dashboard import show_patient_dashboard
    from nurse_workspace import show_nurse_workspace

# Initialize language support
init_language()

# Custom CSS for professional medical UI - Works on all platforms
CUSTOM_CSS = """
<style>
    /* Reset and base styles */
    * {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif !important;
    }
    
    /* Main background */
    .stApp {
        background-color: #f8f9fa !important;
    }
    
    /* Force sidebar to always be visible and on the right */
    [data-testid="stSidebar"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-width: 320px !important;
        max-width: 320px !important;
    }
    
    /* Sidebar content styling */
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h1,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h2,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h3,
    [data-testid="stSidebar"] label {
        color: white !important;
    }
    
    /* Sidebar buttons */
    [data-testid="stSidebar"] .stButton button {
        background-color: white !important;
        color: #667eea !important;
        font-weight: 600;
        border: none;
    }
    
    [data-testid="stSidebar"] .stButton button:hover {
        background-color: #f0f0f0 !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(255,255,255,0.3);
    }
    
    /* Sidebar inputs */
    [data-testid="stSidebar"] input {
        background-color: rgba(255,255,255,0.2) !important;
        color: white !important;
        border: 2px solid rgba(255,255,255,0.3) !important;
        -webkit-text-fill-color: white !important;
    }
    
    [data-testid="stSidebar"] input::placeholder {
        color: rgba(255,255,255,0.7) !important;
        -webkit-text-fill-color: rgba(255,255,255,0.7) !important;
    }
    
    /* Success/info boxes in sidebar */
    [data-testid="stSidebar"] [data-testid="stNotification"] {
        background-color: rgba(255,255,255,0.2) !important;
        color: white !important;
    }
    
    /* All text should be dark and visible */
    body, p, span, div, label, li, td, th {
        color: #212529 !important;
        font-size: 16px !important;
    }
    
    /* Headers - clear hierarchy */
    h1 {
        color: #0d6efd !important;
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        margin-bottom: 1rem !important;
    }
    
    h2 {
        color: #495057 !important;
        font-size: 2rem !important;
        font-weight: 600 !important;
        margin-top: 1.5rem !important;
        margin-bottom: 1rem !important;
    }
    
    h3 {
        color: #495057 !important;
        font-size: 1.5rem !important;
        font-weight: 600 !important;
    }
    
    /* Buttons - clear and clickable */
    .stButton > button {
        background-color: #0d6efd !important;
        color: white !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 0.5rem 1rem !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        cursor: pointer !important;
    }
    
    .stButton > button:hover {
        background-color: #0b5ed7 !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.15) !important;
    }
    
    /* Form inputs - clear labels */
    label {
        color: #212529 !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Input fields - FORCE DARK TEXT */
    input, textarea, select {
        border: 2px solid #dee2e6 !important;
        border-radius: 6px !important;
        padding: 0.5rem !important;
        font-size: 16px !important;
        color: #212529 !important;
        background-color: #ffffff !important;
    }
    
    /* Password fields specifically */
    input[type="password"] {
        color: #212529 !important;
        background-color: #ffffff !important;
        -webkit-text-fill-color: #212529 !important;
    }
    
    /* Select boxes / Dropdowns - FORCE DARK TEXT */
    [data-baseweb="select"] {
        background-color: #ffffff !important;
    }
    
    [data-baseweb="select"] > div {
        background-color: #ffffff !important;
        color: #212529 !important;
    }
    
    [data-baseweb="select"] span {
        color: #212529 !important;
    }
    
    /* Dropdown menu items - SUPER AGGRESSIVE TARGETING */
    [data-baseweb="menu"] {
        background-color: #ffffff !important;
    }
    
    [data-baseweb="menu"] li {
        color: #212529 !important;
        background-color: #ffffff !important;
    }
    
    [data-baseweb="menu"] li:hover {
        background-color: #e9ecef !important;
        color: #212529 !important;
    }
    
    [data-baseweb="menu"] ul {
        background-color: #ffffff !important;
    }
    
    [data-baseweb="menu"] li > div {
        color: #212529 !important;
    }
    
    /* Dropdown options text */
    [role="option"] {
        color: #212529 !important;
        background-color: #ffffff !important;
    }
    
    [role="option"]:hover {
        background-color: #e9ecef !important;
        color: #212529 !important;
    }
    
    [role="option"] span {
        color: #212529 !important;
    }
    
    /* Listbox items */
    [role="listbox"] {
        background-color: #ffffff !important;
    }
    
    [role="listbox"] li {
        color: #212529 !important;
        background-color: #ffffff !important;
    }
    
    /* Ensure all st.selectbox elements are visible */
    .stSelectbox > div > div {
        background-color: #ffffff !important;
        color: #212529 !important;
    }
    
    .stSelectbox label {
        color: #212529 !important;
    }
    
    /* Selectbox dropdown popup */
    .stSelectbox [data-baseweb="popover"] {
        background-color: #ffffff !important;
    }
    
    .stSelectbox [data-baseweb="popover"] > div {
        background-color: #ffffff !important;
    }
    
    /* All dropdown text */
    [data-baseweb="popover"] * {
        color: #212529 !important;
    }
    
    /* Force all select elements to be white background with dark text */
    .stSelectbox [data-baseweb="select"] > div {
        background-color: #ffffff !important;
        color: #212529 !important;
    }
    
    /* Selected option text */
    .stSelectbox [data-baseweb="select"] > div > div {
        color: #212529 !important;
    }
    
    /* Placeholder text */
    .stSelectbox [data-baseweb="select"] [role="button"] {
        color: #212529 !important;
        background-color: #ffffff !important;
    }
    
    /* All text inside select boxes */
    .stSelectbox * {
        color: #212529 !important;
    }
    
    /* Fix ALL button styles - ensure they're always visible */
    button, .stButton button, [data-testid="baseButton-secondary"] {
        background-color: #0d6efd !important;
        color: white !important;
        border: none !important;
        font-weight: 600 !important;
        min-height: 38px !important;
    }
    
    /* Secondary buttons */
    [data-testid="baseButton-secondary"] {
        background-color: #6c757d !important;
        color: white !important;
    }
    
    /* All text boxes and input areas */
    textarea, [data-baseweb="textarea"], .stTextArea textarea {
        background-color: #ffffff !important;
        color: #212529 !important;
        border: 2px solid #dee2e6 !important;
    }
    
    /* Date inputs */
    input[type="date"], input[type="time"] {
        background-color: #ffffff !important;
        color: #212529 !important;
    }
    
    /* Number inputs */
    input[type="number"] {
        background-color: #ffffff !important;
        color: #212529 !important;
    }
    
    /* All containers */
    .stContainer, [data-testid="stContainer"] {
        background-color: transparent !important;
    }
    
    /* Expander headers */
    .streamlit-expanderHeader {
        background-color: #ffffff !important;
        color: #212529 !important;
        border: 2px solid #dee2e6 !important;
    }
    
    /* Radio buttons and checkboxes - make labels visible */
    .stRadio label, .stCheckbox label {
        color: #212529 !important;
    }
    
    /* Multiselect */
    .stMultiSelect [data-baseweb="tag"] {
        background-color: #e7f1ff !important;
        color: #212529 !important;
    }
    
    /* Metrics - big and clear */
    [data-testid="stMetricValue"] {
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        color: #0d6efd !important;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 1rem !important;
        color: #6c757d !important;
        font-weight: 600 !important;
    }
    
    /* Tabs - clear separation */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px !important;
        background-color: #e9ecef !important;
        padding: 4px !important;
        border-radius: 8px !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent !important;
        color: #495057 !important;
        border-radius: 6px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        font-size: 16px !important;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: white !important;
        color: #0d6efd !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
    }
    
    /* Info/Success/Warning/Error boxes */
    .stAlert {
        border-radius: 8px !important;
        border: 2px solid !important;
        padding: 1rem !important;
    }
    
    .stSuccess {
        background-color: #d1e7dd !important;
        border-color: #0f5132 !important;
        color: #0f5132 !important;
    }
    
    .stInfo {
        background-color: #cfe2ff !important;
        border-color: #084298 !important;
        color: #084298 !important;
    }
    
    .stWarning {
        background-color: #fff3cd !important;
        border-color: #997404 !important;
        color: #997404 !important;
    }
    
    .stError {
        background-color: #f8d7da !important;
        border-color: #842029 !important;
        color: #842029 !important;
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        background-color: white !important;
        border: 2px solid #dee2e6 !important;
        border-radius: 8px !important;
        padding: 1rem !important;
        font-weight: 600 !important;
        color: #212529 !important;
        font-size: 16px !important;
    }
    
    /* DataFrames */
    .dataframe {
        font-size: 14px !important;
        color: #212529 !important;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 2px solid #dee2e6 !important;
    }
    
    /* Make sure ALL text is visible */
    .stMarkdown, .stText, .element-container {
        color: #212529 !important;
    }
    
    /* Container backgrounds */
    .element-container {
        background-color: transparent !important;
    }
</style>
"""

# Page configuration
st.set_page_config(
    page_title="Secure Medical Notes AI",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API Configuration
API_BASE_URL = "http://localhost:8000"

# Initialize session state
if 'access_token' not in st.session_state:
    st.session_state.access_token = None
if 'user_role' not in st.session_state:
    st.session_state.user_role = None
if 'user_name' not in st.session_state:
    st.session_state.user_name = None
if 'show_login_page' not in st.session_state:
    st.session_state.show_login_page = False

def make_api_request(endpoint, method="GET", data=None, headers=None):
    """Make API request with error handling"""
    try:
        url = f"{API_BASE_URL}{endpoint}"
        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers)
        elif method == "PUT":
            response = requests.put(url, json=data, headers=headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Error: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to API. Make sure the API server is running on localhost:8000")
        return None

def login_user(email, password):
    """Login user and store token"""
    data = {"email": email, "password": password}
    response = make_api_request("/auth/login", method="POST", data=data)
    
    if response:
        st.session_state.access_token = response["access_token"]
        # Get user info (simplified - in real app, decode JWT)
        st.session_state.user_name = email.split("@")[0]
        
        # Determine role from email (in real app, decode from JWT)
        if "dr." in email.lower() or "doctor" in email.lower():
            st.session_state.user_role = "doctor"
        elif "nurse" in email.lower():
            st.session_state.user_role = "nurse"
        elif "admin" in email.lower():
            st.session_state.user_role = "admin"
        else:
            st.session_state.user_role = "staff"
        
        st.success(f"Login successful! Welcome {st.session_state.user_role.title()}!")
        return True
    return False

def logout_user():
    """Logout user and clear session"""
    st.session_state.access_token = None
    st.session_state.user_role = None
    st.session_state.user_name = None
    st.success("Logged out successfully!")

def get_auth_headers():
    """Get authorization headers for API requests"""
    if st.session_state.access_token:
        return {"Authorization": f"Bearer {st.session_state.access_token}"}
    return {}

# Main App
def main():
    # Apply custom CSS
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    
    # Hide sidebar always (not needed anymore)
    st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            display: none;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Enhanced Hero Header - Slimmer version
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1.5rem 2rem; border-radius: 10px; margin-bottom: 1.5rem; box-shadow: 0 4px 15px rgba(0,0,0,0.15);">
        <h1 style="color: white !important; font-size: 2.5rem !important; margin: 0 !important; text-align: center; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); font-weight: 700; letter-spacing: -0.5px;">
            🏥 Secure Medical Notes AI
        </h1>
        <p style="color: rgba(255,255,255,0.95) !important; font-size: 1rem !important; text-align: center; margin-top: 0.5rem !important; font-weight: 500;">
            AI-Powered Clinical Documentation Platform
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Show greeting and status above main content when logged in
    if st.session_state.access_token:
        # Top bar with greeting and session status
        col1, col2 = st.columns([3, 1])
        with col1:
            user_name = st.session_state.user_name.replace('.', ' ').replace('_', ' ').title()
            role = st.session_state.user_role.title()
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        padding: 1.5rem 2rem; border-radius: 10px; margin-bottom: 1rem;">
                <h2 style="color: white !important; margin: 0; font-size: 1.8rem;">
                    👋 Hello, {user_name}
                </h2>
                <p style="color: rgba(255,255,255,0.9) !important; margin: 0.5rem 0 0 0; font-size: 1.1rem;">
                    {role}
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # Session status with green dot
            st.markdown("""
            <div style="background: white; padding: 1.5rem; border-radius: 10px; margin-bottom: 1rem; 
                        box-shadow: 0 2px 8px rgba(0,0,0,0.1); text-align: center; height: 100%;">
                <div style="font-size: 0.9rem; color: #6c757d; margin-bottom: 0.5rem;">Session Status</div>
                <div style="font-size: 1.2rem; font-weight: 600; color: #198754;">
                    <span style="display: inline-block; width: 12px; height: 12px; background-color: #198754; 
                                 border-radius: 50%; margin-right: 8px; animation: pulse 2s infinite;"></span>
                    Active
                </div>
            </div>
            <style>
                @keyframes pulse {
                    0%, 100% { opacity: 1; }
                    50% { opacity: 0.5; }
                }
            </style>
            """, unsafe_allow_html=True)
        
        # Logout button in a separate row
        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            if st.button("🚪 Logout", use_container_width=True, type="primary"):
                logout_user()
                st.session_state.show_login_page = False
                st.rerun()
    
    # Main content based on authentication status
    if not st.session_state.access_token:
        # Improved welcome message
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 2rem; border-radius: 15px; margin: 1rem 0; color: white; text-align: center;">
            <h2 style="color: white !important; margin: 0;">� Welcome to Secure Medical Notes AI</h2>
            <p style="color: white !important; font-size: 1.2rem; margin-top: 1rem;">
                Please login using the sidebar to access your personalized dashboard →
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("")
        
        # Center login button
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            st.markdown("""
            <div style="text-align: center; margin: 2rem 0;">
                <p style="font-size: 1.1rem; color: #495057; margin-bottom: 1rem;">
                    Ready to get started?
                </p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("🚀 Login to Get Started", use_container_width=True, type="primary", key="main_login_btn"):
                st.session_state.show_login_page = True
                st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Feature showcase in 2 columns for better layout
        if not st.session_state.show_login_page:
            col1, col2 = st.columns(2)
        
            with col1:
                st.markdown("""
            <div style="background-color: white; padding: 2rem; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); 
                        height: 280px; margin-bottom: 1rem;">
                <h2 style="color: #0d6efd !important; text-align: center; margin-bottom: 1rem;">📝</h2>
                <h3 style="color: #212529 !important; text-align: center; margin-bottom: 1rem;">Smart Documentation</h3>
                <p style="color: #6c757d !important; text-align: center; font-size: 1rem; line-height: 1.6;">
                    Create and manage clinical notes with pre-built templates and AI-powered suggestions for faster documentation
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div style="background-color: white; padding: 2rem; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); 
                        height: 280px;">
                <h2 style="color: #dc3545 !important; text-align: center; margin-bottom: 1rem;">🔒</h2>
                <h3 style="color: #212529 !important; text-align: center; margin-bottom: 1rem;">Enterprise Security</h3>
                <p style="color: #6c757d !important; text-align: center; font-size: 1rem; line-height: 1.6;">
                    HIPAA-compliant with role-based access, encryption, and complete audit trails for maximum data security
                </p>
            </div>
            """, unsafe_allow_html=True)
        
            with col2:
                st.markdown("""
            <div style="background-color: white; padding: 2rem; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); 
                        height: 280px; margin-bottom: 1rem;">
                <h2 style="color: #198754 !important; text-align: center; margin-bottom: 1rem;">🤖</h2>
                <h3 style="color: #212529 !important; text-align: center; margin-bottom: 1rem;">AI Analysis</h3>
                <p style="color: #6c757d !important; text-align: center; font-size: 1rem; line-height: 1.6;">
                    Automatic summarization, risk assessment, and clinical insights powered by GPT-4 for better patient care
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div style="background-color: white; padding: 2rem; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); 
                        height: 280px;">
                <h2 style="color: #ffc107 !important; text-align: center; margin-bottom: 1rem;">�</h2>
                <h3 style="color: #212529 !important; text-align: center; margin-bottom: 1rem;">Real-time Analytics</h3>
                <p style="color: #6c757d !important; text-align: center; font-size: 1rem; line-height: 1.6;">
                    Comprehensive dashboards with patient trends, risk monitoring, and actionable insights in real-time
                </p>
            </div>
            """, unsafe_allow_html=True)
        
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Additional features
            st.markdown("""
            <div style="background-color: white; padding: 2rem; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-top: 2rem;">
                <h3 style="color: #212529 !important;">✨ Key Features</h3>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 1rem;">
                    <div style="color: #212529 !important;">✅ <strong>Role-Based Access</strong> - Separate workflows for doctors and nurses</div>
                    <div style="color: #212529 !important;">✅ <strong>Patient Dashboard</strong> - Comprehensive patient history and insights</div>
                    <div style="color: #212529 !important;">✅ <strong>Calendar System</strong> - Manage appointments and follow-ups</div>
                    <div style="color: #212529 !important;">✅ <strong>Real-time Notifications</strong> - Stay updated on critical events</div>
                    <div style="color: #212529 !important;">✅ <strong>Multi-language Support</strong> - Available in multiple languages</div>
                    <div style="color: #212529 !important;">✅ <strong>Report Generation</strong> - Automated PDF reports and analytics</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        else:
            # Login Page
            st.markdown("""
            <div style="background: white; padding: 3rem; border-radius: 15px; max-width: 500px; margin: 3rem auto; box-shadow: 0 10px 30px rgba(0,0,0,0.1); text-align: center;">
                <h2 style="color: #667eea !important; margin-bottom: 2rem;">🔐 Login to Your Account</h2>
                <p style="color: #6c757d !important;">Please enter your credentials to continue</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Center the login form
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.markdown("### Quick Login")
                st.markdown("")
                
                # Quick login buttons
                if st.button("👨‍⚕️ Login as Doctor", use_container_width=True, key="quick_doctor_main"):
                    if login_user("dr.williams@hospital.com", "password123"):
                        st.session_state.show_login_page = False
                        st.rerun()
                
                if st.button("👩‍⚕️ Login as Nurse", use_container_width=True, key="quick_nurse_main"):
                    if login_user("nurse.davis@hospital.com", "password123"):
                        st.session_state.show_login_page = False
                        st.rerun()
                
                st.markdown("---")
                st.markdown("### Or Enter Your Credentials")
                
                with st.form("main_login_form"):
                    email = st.text_input("📧 Email", placeholder="")
                    password = st.text_input("🔒 Password", type="password", placeholder="")
                    
                    col_a, col_b = st.columns(2)
                    with col_a:
                        submit = st.form_submit_button("🚀 Login", use_container_width=True, type="primary")
                    with col_b:
                        back = st.form_submit_button("← Back", use_container_width=True)
                    
                    if submit:
                        if email and password:
                            if login_user(email, password):
                                st.session_state.show_login_page = False
                                st.rerun()
                        else:
                            st.error("Please enter both email and password")
                    
                    if back:
                        st.session_state.show_login_page = False
                        st.rerun()
                
                st.markdown("---")
                st.info("**💡 Demo Credentials:**\n\nDoctor: `dr.williams@hospital.com`\n\nNurse: `nurse.davis@hospital.com`\n\nPassword: `password123`")
    
    else:
        # Role-based tabs - Show role badge
        user_role = st.session_state.get('user_role', 'staff')
        
        role_colors = {"doctor": "#0d6efd", "nurse": "#198754", "admin": "#dc3545", "staff": "#6c757d"}
        role_emoji = {"doctor": "👨‍⚕️", "nurse": "👩‍⚕️", "admin": "👤", "staff": "👤"}
        
        # Role badge with navigation tip
        st.markdown(f"""
        <div style="background-color: {role_colors.get(user_role, '#6c757d')}; color: white; padding: 0.5rem 1rem; border-radius: 8px; margin-bottom: 0.5rem; text-align: center;">
            <strong>{role_emoji.get(user_role, '👤')} Logged in as: {user_role.upper()}</strong>
        </div>
        """, unsafe_allow_html=True)
        
        # Navigation tip removed - not showing properly
        
        # SIMPLIFIED ROLE-SPECIFIC TABS
        if user_role == "nurse":
            # NURSE: 4 simple tabs
            tab1, tab2, tab3, tab4 = st.tabs([
                "🏥 Dashboard",
                "📊 Patient Care",
                "📋 Notes & Tasks", 
                "📅 Calendar"
            ])
            # Create dummy tabs for code compatibility
            tab5 = tab6 = tab7 = tab8 = tab9 = None
        else:
            # DOCTOR: 5 simple tabs
            tab1, tab2, tab3, tab4, tab5 = st.tabs([
                "🏥 Dashboard",
                "👥 Patients",
                "📋 Clinical Notes",
                "🤖 AI & Analytics", 
                "⚙️ More"
            ])
            # Create dummy tabs for code compatibility
            tab6 = tab7 = tab8 = tab9 = None
        
        # TAB 1: DASHBOARD (both roles)
        with tab1:
            if user_role == "nurse":
                # ======== NURSE DASHBOARD ========
                st.header("🏥 Nurse Dashboard")
                
                # Emergency button at top
                col1, col2 = st.columns([2, 1])
                with col1:
                    if st.button("🚨 MEDICAL EMERGENCY - Alert Doctor", use_container_width=True, type="primary"):
                        if 'doctor_notifications' not in st.session_state:
                            st.session_state.doctor_notifications = []
                        st.session_state.doctor_notifications.append({
                            'type': 'medical_emergency',
                            'message': f'🚨 MEDICAL EMERGENCY reported by Nurse {st.session_state.user_name}',
                            'time': datetime.now().strftime('%I:%M %p'),
                            'priority': 'critical',
                            'from': st.session_state.user_name
                        })
                        st.error("🚨 EMERGENCY ALERT SENT TO ALL DOCTORS!")
                
                with col2:
                    st.metric("👩‍⚕️ My Shift", "Day (7a-7p)")
                
                st.markdown("---")
                
                # NURSE: Show assigned patients with vital alerts
                st.subheader("👥 My Assigned Patients")
                
                # Quick stats for nurse
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("👥 Assigned", "6 patients")
                with col2:
                    st.metric("⚠️ Alerts", "2 abnormal vitals")
                with col3:
                    st.metric("💊 Meds Due", "8 medications")
                with col4:
                    st.metric("✅ Tasks", "5 pending")
                
                st.markdown("---")
                
                # Simple patient list for nurse
                st.markdown("### 📋 Today's Patient List")
                
                patients_nurse = [
                    {"id": 1, "name": "John Smith", "room": "101", "status": "🟢 Stable", "vitals": "Normal", "meds_due": "2"},
                    {"id": 2, "name": "Mary Johnson", "room": "102", "status": "🟡 Monitor", "vitals": "⚠️ BP High", "meds_due": "3"},
                    {"id": 3, "name": "Robert Williams", "room": "103", "status": "🟢 Stable", "vitals": "Normal", "meds_due": "1"},
                    {"id": 4, "name": "Patricia Brown", "room": "104", "status": "🔴 Alert", "vitals": "🚨 Temp 102°F", "meds_due": "2"},
                    {"id": 5, "name": "James Davis", "room": "105", "status": "🟢 Stable", "vitals": "Normal", "meds_due": "0"},
                    {"id": 6, "name": "Jennifer Garcia", "room": "106", "status": "🟡 Monitor", "vitals": "⚠️ O2 Low", "meds_due": "4"},
                ]
                
                for patient in patients_nurse:
                    with st.expander(f"{patient['status']} Room {patient['room']}: {patient['name']} - Vitals: {patient['vitals']}"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**Patient ID:** {patient['id']}")
                            st.write(f"**Room:** {patient['room']}")
                            st.write(f"**Vital Status:** {patient['vitals']}")
                        with col2:
                            st.write(f"**Status:** {patient['status']}")
                            st.write(f"**Meds Due:** {patient['meds_due']}")
                            if st.button(f"Quick Actions", key=f"nurse_action_{patient['id']}"):
                                st.info("Navigate to Patient Care tab for vitals/meds")
                
                # Show notifications
                st.markdown("---")
                st.subheader("🔔 Recent Notifications")
                if 'nurse_notifications' in st.session_state and st.session_state.nurse_notifications:
                    for notif in st.session_state.nurse_notifications[:3]:
                        st.warning(f"📞 {notif['message']} at {notif['time']}")
                else:
                    st.success("✅ No new notifications")
            
            else:
                # ======== DOCTOR DASHBOARD ========
                st.header("🏥 Doctor Dashboard")
                
                # Quick stats
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("👥 Total Patients", "24")
                with col2:
                    st.metric("📋 Notes Today", "8")
                with col3:
                    st.metric("⚠️ High Risk", "3")
                with col4:
                    st.metric("🔔 Alerts", "2")
                
                st.markdown("---")
                
                # Emergency alerts from nurses
                if 'doctor_notifications' in st.session_state and st.session_state.doctor_notifications:
                    st.markdown("### 🚨 EMERGENCY ALERTS")
                    for notif in st.session_state.doctor_notifications:
                        st.error(f"🚨 {notif['message']} at {notif['time']}")
                        if st.button(f"✅ Responding", key=f"resp_{notif['time']}"):
                            st.success("Marked as responding!")
                else:
                    st.success("✅ No emergency alerts")
                
                st.markdown("---")
                
                # Doctor: Show quick patient summary (no duplicate widgets)
                st.subheader("📊 Quick Patient Summary")
                
                summary_col1, summary_col2 = st.columns(2)
                
                with summary_col1:
                    st.markdown("#### 🟢 Recent Patients")
                    recent_patients = [
                        {"name": "John Smith", "last_visit": "2024-01-15", "status": "Stable"},
                        {"name": "Mary Johnson", "last_visit": "2024-01-14", "status": "Follow-up needed"},
                        {"name": "Robert Williams", "last_visit": "2024-01-13", "status": "Improving"},
                    ]
                    for p in recent_patients:
                        st.write(f"• **{p['name']}** - {p['status']} ({p['last_visit']})")
                
                with summary_col2:
                    st.markdown("#### ⚠️ High Priority")
                    priority_patients = [
                        {"name": "Patricia Brown", "reason": "Post-op monitoring", "level": "High"},
                        {"name": "James Davis", "reason": "Medication adjustment", "level": "Medium"},
                        {"name": "Jennifer Garcia", "reason": "Follow-up scan", "level": "Medium"},
                    ]
                    for p in priority_patients:
                        color = "red" if p['level'] == "High" else "orange"
                        st.write(f"• **{p['name']}** - :{color}[{p['level']}] {p['reason']}")
                
                st.info("💡 Go to 'Patients' tab for full patient management dashboard")
        
        # TAB 2: Different for each role
        with tab2:
            if user_role == "nurse":
                # NURSE: Patient Care (Vitals + Meds + I/O combined!)
                st.header("📊 Patient Care")
                
                care_subtab1, care_subtab2, care_subtab3 = st.tabs(["💉 Vitals", "💊 Medications", "💧 Intake/Output"])
                
                with care_subtab1:
                    st.subheader("📊 Record Vital Signs")
                    st.info("Quick vital signs entry with automatic abnormal alerts")
                    # Import and show just vital signs from workspace
                    from nurse_workspace import show_vital_signs
                    show_vital_signs(API_BASE_URL, {"Authorization": f"Bearer {st.session_state.access_token}"})
                
                with care_subtab2:
                    st.subheader("💊 Medication Administration")
                    st.info("MAR with allergy warnings")
                    from nurse_workspace import show_medications
                    show_medications(API_BASE_URL, {"Authorization": f"Bearer {st.session_state.access_token}"})
                
                with care_subtab3:
                    st.subheader("💧 Fluid Balance Tracking")
                    from nurse_workspace import show_intake_output
                    show_intake_output(API_BASE_URL, {"Authorization": f"Bearer {st.session_state.access_token}"})
            
            else:
                # DOCTOR: Patients list
                show_patient_dashboard(API_BASE_URL, st.session_state.access_token)
        
        # TAB 3: Different for each role
        with tab3:
            if user_role == "nurse":
                # NURSE: Notes & Tasks combined
                st.header("📋 Notes & Tasks")
                
                notes_tabs = st.tabs(["📝 Create Note", "✅ My Tasks"])
                
                with notes_tabs[0]:
                    st.subheader("Create Nurse Note")
                    with st.form("nurse_note_quick"):
                        patient_id = st.text_input("Patient ID")
                        title = st.text_input("Note Title")
                        content = st.text_area("Note Content", height=150)
                        if st.form_submit_button("Create Note"):
                            if patient_id and title and content:
                                data = {
                                    "patient_id": int(patient_id) if patient_id.isdigit() else 1,
                                    "title": title,
                                    "content": content,
                                    "note_type": "nurse_note"
                                }
                                response = make_api_request("/notes/", method="POST", data=data, headers=get_auth_headers())
                                if response:
                                    st.success("Note created!")
                            else:
                                st.error("Please fill all fields")
                
                with notes_tabs[1]:
                    st.subheader("✅ Task Checklist")
                    from nurse_workspace import show_task_checklist
                    show_task_checklist(API_BASE_URL, {"Authorization": f"Bearer {st.session_state.access_token}"})
            
            else:
                # DOCTOR: Clinical Notes
                st.header("📋 Clinical Notes Management")
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.subheader("Create New Note")
                    template_content = show_template_selector()
                    
                    with st.form("doctor_note_form"):
                        patient_id = st.text_input("Patient ID")
                        title = st.text_input("Note Title")
                        content = st.text_area("Note Content", value=template_content, height=200)
                        submit = st.form_submit_button("Create Note")
                        
                        if submit:
                            if patient_id and title and content:
                                data = {
                                    "patient_id": int(patient_id) if patient_id.isdigit() else 1,
                                    "title": title,
                                    "content": content,
                                    "note_type": "doctor_note"
                                }
                                response = make_api_request("/notes/", method="POST", data=data, headers=get_auth_headers())
                                if response:
                                    st.success("Note created successfully!")
                            else:
                                st.error("Please fill in all fields")
                
                with col2:
                    st.subheader("Recent Notes")
                    notes = make_api_request("/notes/", headers=get_auth_headers())
                    if notes:
                        for note in notes[:5]:
                            # Display each note in a card for better separation
                            st.markdown(f"""
                            <div style="padding: 12px; border-radius: 8px; background-color: #f8f9fa; 
                                        border-left: 4px solid #0d6efd; margin-bottom: 10px;">
                                <h5 style="color: #0d6efd; margin: 0 0 5px 0;">{note.get('title', 'Untitled')}</h5>
                                <p style="color: #6c757d; margin: 0; font-size: 14px;">📅 {note.get('created_at', '')[:10]}</p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Add expander for more details
                            with st.expander("View Details"):
                                st.write(f"**Type:** {note.get('note_type', 'N/A')}")
                                st.write(f"**Patient ID:** {note.get('patient_id', 'N/A')}")
                                if note.get('summary'):
                                    st.write(f"**AI Summary:** {note['summary']}")
                    else:
                        st.info("No notes available")
        
        # TAB 4: Different for each role
        with tab4:
            if user_role == "nurse":
                # NURSE: Calendar
                st.header("📅 Calendar & Schedule")
                show_calendar_system()
            
            else:
                # DOCTOR: AI & Analytics (combined AI Dashboard + Summaries + Risk)
                st.header("🤖 AI & Analytics")
                
                ai_tabs = st.tabs(["📊 Dashboard", "📝 Summaries", "⚠️ Risk Reports"])
                
                with ai_tabs[0]:
                    show_ai_dashboard()
                
                with ai_tabs[1]:
                    st.subheader("AI-Generated Summaries")
                    st.info("View and process notes with AI analysis")
                
                with ai_tabs[2]:
                    st.subheader("Risk Assessment Reports")
                    st.info("Patient risk assessments and recommendations")
        
        # TAB 5: DOCTOR ONLY - More (Calendar + Audit + Help)
        if tab5 and user_role == "doctor":
            with tab5:
                st.header("⚙️ More Tools & Settings")
                
                more_tabs = st.tabs(["📅 Calendar", "📝 Audit Trail", "ℹ️ Help", "📞 Quick Actions"])
                
                with more_tabs[0]:
                    show_calendar_system()
                
                with more_tabs[1]:
                    st.subheader("📝 Audit Trail")
                    st.info("Complete audit logging of all system access")
                    audit_data = {
                        "Timestamp": ["2024-01-15 10:30:00", "2024-01-15 10:25:00"],
                        "User": ["Dr. Smith", "Nurse Johnson"],
                        "Action": ["Created Note", "Viewed Patient"],
                        "Resource": ["Note #123", "Patient #456"],
                        "IP Address": ["192.168.1.100", "192.168.1.101"]
                    }
                    df = pd.DataFrame(audit_data)
                    st.dataframe(df, use_container_width=True)
                
                with more_tabs[2]:
                    st.subheader("ℹ️ Help & Support")
                    st.markdown("""
                    ### Quick Guide
                    - Use templates in Clinical Notes for faster documentation
                    - AI & Analytics tab shows trends and insights
                    - Check Dashboard for emergency alerts
                    
                    **Support:** support@hospital.com
                    """)
                
                with more_tabs[3]:
                    st.subheader("📞 Quick Communication")
                    if st.button("📞 Call Nurse", use_container_width=True, type="primary"):
                        if 'nurse_notifications' not in st.session_state:
                            st.session_state.nurse_notifications = []
                        st.session_state.nurse_notifications.append({
                            'type': 'call_from_doctor',
                            'message': f'Dr. {st.session_state.user_name} is calling for assistance',
                            'time': datetime.now().strftime('%I:%M %p'),
                            'priority': 'high',
                            'from': st.session_state.user_name
                        })
                        st.success("✅ Nurse has been notified!")
        
        # Remove all old tab code - simplified structure complete

if __name__ == "__main__":
    main()
