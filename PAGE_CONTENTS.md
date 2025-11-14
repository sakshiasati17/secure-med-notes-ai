# Page Contents Summary

## 🏗️ Application Structure

### Current Setup
- **Active:** Original monolithic `app.py` (restored from backup)
- **Available:** New modular structure in `/ui/pages/` folders
- **Status:** ✅ Running on http://localhost:8501
- **API:** ✅ Running on http://localhost:8000

---

## 📄 Page Content Details

### **DOCTOR PAGES** (`/ui/pages/doctor/`)

#### 1. **dashboard.py** (Dashboard)
**Purpose:** Doctor's main landing page with overview stats

**Content:**
```python
- Stats Cards (4):
  * Total Patients: 5 (+2 this week)
  * Active Notes: 73 (+15 today)  
  * High Risk: 2 (⚠️)
  * Pending Reviews: 8 (📋)

- Recent Activity Section:
  * Left Column: Recent Notes (fetched from /notes API)
    - Shows last 5 notes
    - Displays: Title, Patient ID, Date
    - Styled cards with shadows
  
  * Right Column: High-Risk Patients
    - Warning alerts for critical patients
    - Manual list (can be API-driven)

- Quick Actions (4 buttons):
  * 📝 New Note → "Navigate to Clinical Notes tab"
  * 👥 View Patients → "Navigate to Patients tab"
  * 🤖 AI Analysis → "Navigate to AI & Analytics tab"
  * 📊 Reports → "Generate reports"
```

**API Calls:**
- `GET /notes` with authorization headers
- Returns JSON array of notes

**Dependencies:**
- `streamlit`, `requests`, `pandas`, `plotly`

---

#### 2. **patients.py** (Patient Management)
**Purpose:** View and manage patient records

**Content:**
```python
- Imports: show_patient_dashboard()
- Delegates to existing patient_dashboard.py module

Features from patient_dashboard:
- 3 Tabs:
  1. Patient Overview
     * All patients in grid
     * Patient cards with demographics
  
  2. Individual Patient
     * Patient selector
     * View Details button (uses real API IDs)
     * Visit History (2-column layout)
     * Recent notes with styled cards
  
  3. Analytics
     * Demographics chart (white bg, black text)
     * Diagnosis distribution
     * Age distribution  
     * Notes by type
```

**API Calls:**
- `GET /patients` - List all patients
- `GET /patients/{id}` - Individual patient details

**Chart Styling:**
```python
layout = {
    'plot_bgcolor': '#FFFFFF',
    'paper_bgcolor': '#FFFFFF',
    'font': {'color': '#000000', 'size': 12},
    'title': {'font': {'color': '#000000', 'size': 16}},
    'xaxis': {'gridcolor': '#E5E5E5', 'tickfont': {'color': '#000000'}},
    'yaxis': {'gridcolor': '#E5E5E5', 'tickfont': {'color': '#000000'}},
    'legend': {'font': {'color': '#000000'}}
}
```

---

#### 3. **clinical_notes.py** (Clinical Notes)
**Purpose:** Create, view, and search clinical notes

**Content:**
```python
- 3 Tabs:

TAB 1: Create Note
-------
- Template selector (imported from note_templates)
- Form with:
  * Patient Selection (dropdown from /patients API)
  * Note Type dropdown:
    - Progress Note
    - SOAP Note
    - Consultation
    - Discharge Summary
    - Procedure Note
  * Visit Date (date picker)
  * Chief Complaint (text input)
  * Subjective - Patient's Description (textarea, 100px)
  * Objective - Clinical Findings (textarea, 100px)
  * Assessment - Diagnosis (textarea, 100px)
  * Plan - Treatment Plan (textarea, 100px)
  * 💾 Save Note button (primary, full width)

- On Submit:
  * Creates note_data dict
  * POSTs to /notes endpoint
  * Shows success message with balloons
  * Or error message if failed

TAB 2: View Notes
-------
- Fetches all notes from /notes
- Each note in expandable card showing:
  * Title and date
  * Patient ID
  * Note type
  * Created timestamp
  * Full content (markdown formatted)
  * Action buttons: ✏️ Edit, 🗑️ Delete

TAB 3: Search Notes
-------
- Search input field
- Filter by type dropdown
- Search button
- (Currently shows info message)
```

**API Calls:**
- `GET /patients` - For patient dropdown
- `POST /notes` - Create new note
- `GET /notes` - List all notes

**Note Data Structure:**
```json
{
  "patient_id": 1,
  "title": "Progress Note - Chief Complaint",
  "content": "**Subjective:** ...\n**Objective:** ...\n**Assessment:** ...\n**Plan:** ...",
  "note_type": "progress_note"
}
```

---

#### 4. **ai_analytics.py** (AI & Analytics)
**Purpose:** AI-powered insights and analytics

**Content:**
```python
- Imports: show_ai_dashboard()
- Delegates to existing ai_dashboard.py module

Features from ai_dashboard:
- AI Summarization
- Risk Assessment
- Clinical Recommendations
- Patient Trends Analysis
- GPT-4o-mini integration
- FAISS vector search
- LangChain processing
```

**Dependencies:**
- OpenAI API
- LangChain
- FAISS
- Vector embeddings

---

#### 5. **more.py** (Settings & More)
**Purpose:** Additional features and settings

**Content:**
```python
- 3 Tabs:

TAB 1: Calendar
-------
- Imports: show_calendar_system()
- Calendar view
- Appointment management
- Follow-up scheduling

TAB 2: Notifications
-------
- Imports: show_notifications()
- Alert system
- Real-time notifications
- Critical updates

TAB 3: Settings
-------
Profile Settings (2 columns):
- Left:
  * Name (text input, pre-filled from session)
  * Email (text input, read-only)
- Right:
  * Specialty (text input, placeholder)
  * License Number (text input, placeholder)

Notification Preferences:
- ☑️ Email notifications for high-risk patients (checked)
- ☑️ Daily summary reports (checked)
- ☑️ Real-time AI insights (checked)

Display Settings:
- Theme dropdown: Light / Dark / Auto
- Dashboard refresh rate slider: 10-60 seconds (default 30)

💾 Save Settings button (primary)
- Shows success message on save
```

---

### **NURSE PAGES** (`/ui/pages/nurse/`)

#### 1. **dashboard.py** (Nurse Dashboard)
**Purpose:** Nurse's main landing page

**Content:**
```python
- Stats Cards (4):
  * Assigned Patients: 12 (+3 today)
  * Tasks Pending: 8 (📋)
  * Vitals Due: 5 (🩺)
  * Medications Due: 15 (💊)

- Today's Schedule (2 columns):
  
  Left: Upcoming Tasks
  ---------------------
  * 10:00 AM - Vitals check - Room 305 [RED border - High]
  * 10:30 AM - Medication administration - Room 307 [RED border - High]
  * 11:00 AM - Patient education - Room 310 [YELLOW border - Medium]
  * 02:00 PM - Wound dressing - Room 312 [YELLOW border - Medium]
  * 03:30 PM - Discharge prep - Room 305 [GREEN border - Low]
  
  Right: Quick Stats
  -------------------
  * ✅ 4 tasks completed (info box)
  * ⏰ 3 tasks overdue (warning box)
  * 📊 85% completion rate (success box)

- Quick Actions (4 buttons):
  * 📝 Add Note
  * 🩺 Record Vitals
  * 💊 Medications
  * 📋 Tasks
```

**Task Card Styling:**
```python
color_map = {
    "high": "#dc3545",    # Red
    "medium": "#ffc107",  # Yellow
    "low": "#198754"      # Green
}

Card HTML:
- White background
- Colored left border (4px)
- Padding: 1rem
- Border-radius: 4px
- Box shadow
- Time in bold with priority color
- Task description below
```

---

#### 2. **patient_care.py** (Patient Care)
**Purpose:** Nursing-specific patient care workflows

**Content:**
```python
- Imports: show_nurse_workspace()
- Delegates to existing nurse_workspace.py module

Features:
- Patient monitoring
- Care plans
- Nursing assessments
- Treatment tracking
```

---

#### 3. **notes_tasks.py** (Notes & Task Management)
**Purpose:** Create nurse notes, manage tasks, record vitals

**Content:**
```python
- 3 Tabs:

TAB 1: Nurse Notes
------------------
Add Nurse Note Form:
- 2 columns:
  Left:
    * Patient ID (number input)
    * Note Type dropdown:
      - Assessment Note
      - Progress Note
      - Shift Report
      - Incident Report
  Right:
    * Date (date picker)
    * Time (time picker)

- Full width fields:
  * Vital Signs (textarea, placeholder)
  * Observations (textarea, 100px)
  * Interventions/Care Provided (textarea, 100px)
  * Patient Response (textarea, 80px)
  * 💾 Save Note button (primary, full width)

Recent Nurse Notes:
- Last 5 notes from /notes
- Expandable cards
- Shows full content

TAB 2: Task Management
----------------------
Left Column (2/3 width): Pending Tasks
- Sample tasks with 3 columns:
  * Task description + due time
  * Priority indicator (🔴 🟡 🟢)
  * ✓ Done button
- Tasks:
  * Administer medication - Room 305 (10:30 AM) [High]
  * Wound dressing change - Room 307 (11:00 AM) [Medium]
  * Patient education - Room 310 (02:00 PM) [Low]

Right Column (1/3 width): Add Task
- Form:
  * Task (text input)
  * Due Time (time picker)
  * Priority (High/Medium/Low dropdown)
  * Add button
- Success message on add

TAB 3: Vitals Records
---------------------
Record Vital Signs Form (2 columns):

Left Column:
- Patient ID (number, min 1)
- BP Systolic (number, 50-250, default 120)
- BP Diastolic (number, 30-150, default 80)
- Heart Rate bpm (number, 30-200, default 72)

Right Column:
- Temperature °F (number, 95.0-106.0, step 0.1, default 98.6)
- Respiratory Rate (number, 8-40, default 16)
- SpO2 % (number, 70-100, default 98)
- Pain Scale (slider, 0-10, default 0)

Additional Notes (textarea, full width)
💾 Save Vitals button (primary, full width)
- Shows success + balloons on save
```

**API Calls:**
- `POST /notes` - Save nurse note
- `GET /notes` - Get recent notes

---

#### 4. **calendar.py** (Calendar)
**Purpose:** Nurse scheduling and appointments

**Content:**
```python
- Imports: show_calendar_system()
- Delegates to existing calendar_system.py module

Features:
- Shift calendar
- Appointment tracking
- Task deadlines
- Schedule management
```

---

## 🎨 UI Components

### Header Banner (All Pages)
```html
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            padding: 1.5rem 2rem; 
            border-radius: 10px; 
            margin-bottom: 1.5rem;">
  <h1>🏥 Secure Medical Notes AI</h1>
  <p>AI-Powered Clinical Documentation Platform</p>
</div>
```

### Greeting Bar (When Logged In)
```html
Left (3/4 width):
<div style="background: gradient(#667eea to #764ba2); padding: 1.5rem 2rem;">
  <h2>👋 Hello, Dr Williams</h2>
  <p>Doctor</p>
</div>

Right (1/4 width):
<div style="background: white; padding: 1.5rem;">
  <div>Session Status</div>
  <div>
    <span style="green dot, pulsing animation"></span>
    Active
  </div>
</div>
```

### Navigation Tabs
**Doctor (6 buttons):**
- 🏥 Dashboard | 👥 Patients | 📋 Clinical Notes | 🤖 AI & Analytics | ⚙️ More | 🚪

**Nurse (5 buttons):**
- 🏥 Dashboard | 📊 Patient Care | 📋 Notes & Tasks | 📅 Calendar | 🚪

**Active tab:** Primary button style (blue)
**Inactive tabs:** Secondary button style (gray)

---

## 🔄 Navigation Flow

```
Welcome Page
    ↓
Login Page
    ↓ (successful login)
    ├─→ DOCTOR
    │   ├─→ Dashboard (default)
    │   ├─→ Patients
    │   ├─→ Clinical Notes
    │   ├─→ AI & Analytics
    │   └─→ More
    │
    └─→ NURSE
        ├─→ Dashboard (default)
        ├─→ Patient Care
        ├─→ Notes & Tasks
        └─→ Calendar

Any Page → 🚪 Logout → Welcome Page
```

---

## 📊 Data Sources

### API Endpoints Used
```
GET  /health              - API health check
POST /auth/login          - Authentication
GET  /patients            - List all patients
GET  /patients/{id}       - Get patient details
GET  /notes               - List all notes
POST /notes               - Create new note
GET  /notes/{id}          - Get note details
```

### Session State
```python
st.session_state = {
    'access_token': "eyJ0eXAi...",  # JWT token
    'user_role': "doctor",           # or "nurse"
    'user_name': "dr.williams",      # from email
    'show_login_page': False,        # Boolean
    'current_page': "dashboard",     # Active page
    'API_BASE_URL': "http://localhost:8000"
}
```

---

## ✅ Testing Status

### Current Implementation
- ✅ All doctor pages created
- ✅ All nurse pages created
- ✅ Page modules properly structured
- ✅ API integration included
- ✅ Forms and inputs implemented
- ⚠️ Using original monolithic app.py (not modular router)

### To Test Each Page
1. Login as doctor (dr.williams@hospital.com)
2. Navigate through each tab
3. Test forms and buttons
4. Check API calls in network tab
5. Logout and login as nurse (nurse.davis@hospital.com)
6. Repeat for nurse pages

---

## 🚀 Running the Application

```bash
# Terminal 1: Start API
source venv/bin/activate
uvicorn api.main:app --reload --port 8000

# Terminal 2: Start UI
source venv/bin/activate
streamlit run ui/app.py --server.port 8501

# Access
UI: http://localhost:8501
API Docs: http://localhost:8000/docs
```

---

**Status:** ✅ All pages created and documented
**Next Step:** Optionally implement modular routing in main app.py to use these pages
**Current:** Using original monolithic app.py (fully functional)
