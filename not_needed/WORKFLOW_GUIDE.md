# Secure Medical Notes AI - Workflow Guide

## 🚀 Application Startup

### Prerequisites
1. Docker containers running (PostgreSQL on port 5434, Redis on port 6379)
2. API server running on port 8000
3. UI server running on port 8501

### Start Commands
```bash
# Start API
./start_api.sh

# Or manually:
source venv/bin/activate
uvicorn api.main:app --reload --port 8000
```

---

## 📱 User Interface Workflow

### **Welcome Page** (Not Logged In)
**URL:** http://localhost:8501

**Features:**
- Slim header banner with application branding
- Welcome message
- Centered "Login to Get Started" button
- Feature showcase (when implemented)

**Actions:**
- Click "🚀 Login to Get Started" → Navigate to Login Page

---

### **Login Page**
**Features:**
- Clean, centered login form
- Quick login buttons:
  - 👨‍⚕️ Login as Doctor (dr.williams@hospital.com / password123)
  - 👩‍⚕️ Login as Nurse (nurse.davis@hospital.com / password123)
- Manual login form with email and password
- Back button to return to welcome page
- Demo credentials display

**Actions:**
- Click quick login button → Auto-login and redirect to dashboard
- Enter credentials manually → Click "🚀 Login" → Redirect to dashboard
- Click "← Back" → Return to welcome page

---

## 👨‍⚕️ Doctor Workflow

### After Login (Doctor)
**Top Bar:**
- Greeting: "👋 Hello, Dr Williams" with role
- Session status indicator (🟢 Active - pulsing green dot)

**Navigation Tabs:**
1. 🏥 Dashboard
2. 👥 Patients
3. 📋 Clinical Notes
4. 🤖 AI & Analytics
5. ⚙️ More
6. 🚪 (Logout button)

---

### **1. Doctor Dashboard** (`pages/doctor/dashboard.py`)

**Features:**
- **Stats Cards:**
  - Total Patients: 5 (+2 this week)
  - Active Notes: 73 (+15 today)
  - High Risk: 2 (⚠️)
  - Pending Reviews: 8 (📋)

- **Recent Activity (2 columns):**
  - Left: Recent Notes (last 5 notes from API)
  - Right: High-Risk Patients list

- **Quick Actions (4 buttons):**
  - 📝 New Note → Navigate to Clinical Notes
  - 👥 View Patients → Navigate to Patients
  - 🤖 AI Analysis → Navigate to AI & Analytics
  - 📊 Reports → Generate reports

**Data Source:** 
- Fetches from `/notes` API endpoint
- Shows patient IDs and creation dates
- Real-time data from database

---

### **2. Doctor Patients** (`pages/doctor/patients.py`)

**Features:**
- **Imports existing `patient_dashboard` module**
- **3 Tabs:**
  1. **Patient Overview** - All patients with cards
  2. **Individual Patient** - Detailed patient view with:
     - Patient grid with "View Details" buttons
     - Visit history in 2-column layout
     - Recent notes display
  3. **Analytics** - Charts with white backgrounds:
     - Patient demographics
     - Diagnosis distribution
     - Age distribution
     - Notes by type

**Data Source:**
- Fetches from `/patients` API endpoint
- Shows patient details, visit history, notes
- All Plotly charts with white background (#FFFFFF) and black text (#000000)

---

### **3. Doctor Clinical Notes** (`pages/doctor/clinical_notes.py`)

**Features:**
- **3 Tabs:**

#### Tab 1: Create Note
- Template selector (uses `note_templates.py`)
- **Form Fields:**
  - Patient Selection (dropdown from API)
  - Note Type (Progress Note, SOAP Note, Consultation, Discharge Summary, Procedure Note)
  - Visit Date
  - Chief Complaint
  - Subjective (Patient's Description)
  - Objective (Clinical Findings)
  - Assessment (Diagnosis)
  - Plan (Treatment Plan)
- **Save Button:** Posts to `/notes` API endpoint

#### Tab 2: View Notes
- Lists all clinical notes from API
- Expandable cards showing:
  - Patient ID
  - Note type
  - Created date
  - Full content
  - Edit and Delete buttons

#### Tab 3: Search Notes
- Search by keyword
- Filter by note type
- Search button

**Data Source:**
- GET `/notes` for listing
- POST `/notes` for creating
- Patient list from GET `/patients`

---

### **4. Doctor AI & Analytics** (`pages/doctor/ai_analytics.py`)

**Features:**
- **Imports existing `ai_dashboard` module**
- AI-powered insights:
  - Note summarization
  - Risk assessment
  - Clinical recommendations
  - Patient trends analysis

**Data Source:**
- Uses AI service (OpenAI GPT-4o-mini)
- FAISS vector search
- LangChain integration

---

### **5. Doctor More** (`pages/doctor/more.py`)

**Features:**
- **3 Tabs:**

#### Tab 1: Calendar
- Uses existing `calendar_system` module
- Appointment management
- Schedule view

#### Tab 2: Notifications
- Uses existing `notifications` module
- Alert system
- Real-time updates

#### Tab 3: Settings
- **Profile Settings:**
  - Name
  - Email
  - Specialty
  - License Number

- **Notification Preferences:**
  - Email notifications for high-risk patients
  - Daily summary reports
  - Real-time AI insights

- **Display Settings:**
  - Theme selection (Light/Dark/Auto)
  - Dashboard refresh rate (10-60 seconds)

- **Save Button:** Saves preferences

---

## 👩‍⚕️ Nurse Workflow

### After Login (Nurse)
**Top Bar:**
- Greeting: "👋 Hello, Nurse Davis" with role
- Session status indicator (🟢 Active - pulsing green dot)

**Navigation Tabs:**
1. 🏥 Dashboard
2. 📊 Patient Care
3. 📋 Notes & Tasks
4. 📅 Calendar
5. 🚪 (Logout button)

---

### **1. Nurse Dashboard** (`pages/nurse/dashboard.py`)

**Features:**
- **Stats Cards:**
  - Assigned Patients: 12 (+3 today)
  - Tasks Pending: 8 (📋)
  - Vitals Due: 5 (🩺)
  - Medications Due: 15 (💊)

- **Today's Schedule (2 columns):**
  - Left: Upcoming Tasks with priority colors
    - High Priority: Red border
    - Medium Priority: Yellow border
    - Low Priority: Green border
  - Right: Quick Stats
    - Tasks completed
    - Tasks overdue
    - Completion rate

- **Quick Actions (4 buttons):**
  - 📝 Add Note
  - 🩺 Record Vitals
  - 💊 Medications
  - 📋 Tasks

**Sample Tasks:**
```
10:00 AM - Vitals check - Room 305 (High)
10:30 AM - Medication administration - Room 307 (High)
11:00 AM - Patient education - Room 310 (Medium)
02:00 PM - Wound dressing - Room 312 (Medium)
03:30 PM - Discharge prep - Room 305 (Low)
```

---

### **2. Nurse Patient Care** (`pages/nurse/patient_care.py`)

**Features:**
- **Imports existing `nurse_workspace` module**
- Patient care management
- Nursing-specific workflows
- Patient monitoring

---

### **3. Nurse Notes & Tasks** (`pages/nurse/notes_tasks.py`)

**Features:**
- **3 Tabs:**

#### Tab 1: Nurse Notes
- **Create Note Form:**
  - Patient ID
  - Note Type (Assessment Note, Progress Note, Shift Report, Incident Report)
  - Date and Time
  - Vital Signs field
  - Observations
  - Interventions/Care Provided
  - Patient Response
- **Save Button:** Posts to `/notes` API

- **Recent Nurse Notes:**
  - Last 5 notes from API
  - Expandable view

#### Tab 2: Task Management
- **Pending Tasks (Left):**
  - Task list with checkboxes
  - Due times
  - Priority indicators
  - "✓ Done" button for each task

- **Add Task (Right):**
  - Task description
  - Due time
  - Priority selector
  - Add button

**Sample Tasks:**
```
- Administer medication - Room 305 (10:30 AM) 🔴 High
- Wound dressing change - Room 307 (11:00 AM) 🟡 Medium
- Patient education - Room 310 (02:00 PM) 🟢 Low
```

#### Tab 3: Vitals Records
- **Record Form:**
  - Patient ID
  - Blood Pressure (Systolic/Diastolic)
  - Heart Rate (bpm)
  - Temperature (°F)
  - Respiratory Rate
  - SpO2 (%)
  - Pain Scale (0-10 slider)
  - Additional Notes
- **Save Button:** Records vitals

---

### **4. Nurse Calendar** (`pages/nurse/calendar.py`)

**Features:**
- **Imports existing `calendar_system` module**
- Shift scheduling
- Appointment tracking
- Task deadlines

---

## 🔐 Logout Workflow

**From Any Page:**
1. Click 🚪 logout button in navigation
2. Session cleared:
   - `access_token` = None
   - `user_role` = None
   - `user_name` = None
   - `current_page` = 'dashboard'
3. Redirected to Welcome Page
4. Success message: "Logged out successfully!"

---

## 📊 Data Flow

### Authentication Flow
```
Welcome Page → Login Page → POST /auth/login → Token Received → Dashboard
```

### Note Creation Flow (Doctor)
```
Clinical Notes Tab → Create Note Form → POST /notes → Success → Note Saved
```

### Note Creation Flow (Nurse)
```
Notes & Tasks Tab → Nurse Notes Form → POST /notes → Success → Note Saved
```

### Patient Data Flow
```
Patients Tab → GET /patients → Patient List → View Details → Patient Info
```

---

## 🎨 UI Design Elements

### Colors
- **Primary:** #667eea to #764ba2 (Purple gradient)
- **Success:** #198754 (Green)
- **Warning:** #ffc107 (Yellow)
- **Danger:** #dc3545 (Red)
- **Info:** #0d6efd (Blue)
- **Background:** #f8f9fa (Light gray)

### Status Indicators
- **Active Session:** 🟢 Pulsing green dot with "Active" text
- **High Priority:** 🔴 Red
- **Medium Priority:** 🟡 Yellow
- **Low Priority:** 🟢 Green

### Typography
- **Headers:** 2.5rem, bold
- **Subheaders:** 1.8rem
- **Body:** 1rem
- **Font Family:** -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto

---

## 🔧 Technical Architecture

### File Structure
```
ui/
├── app.py                          # Main application (current version)
├── app_old.py                      # Backup of original monolithic app
├── pages/
│   ├── doctor/
│   │   ├── dashboard.py           # Doctor dashboard
│   │   ├── patients.py            # Patient management
│   │   ├── clinical_notes.py     # Note creation/viewing
│   │   ├── ai_analytics.py       # AI insights
│   │   └── more.py                # Settings & calendar
│   └── nurse/
│       ├── dashboard.py           # Nurse dashboard
│       ├── patient_care.py        # Patient care
│       ├── notes_tasks.py         # Notes & task management
│       └── calendar.py            # Calendar
├── ai_dashboard.py                # AI functionality
├── calendar_system.py             # Calendar component
├── notifications.py               # Notifications
├── note_templates.py              # Note templates
├── patient_dashboard.py           # Patient dashboard component
└── nurse_workspace.py             # Nurse workspace component
```

### Session State Variables
- `access_token`: JWT token from authentication
- `user_role`: "doctor" or "nurse"
- `user_name`: Extracted from email
- `show_login_page`: Boolean for login page display
- `current_page`: Active page identifier
- `API_BASE_URL`: "http://localhost:8000"

---

## 🧪 Testing Each Page

### Manual Testing Checklist

#### ✅ Welcome & Login
- [ ] Welcome page loads with banner
- [ ] Login button navigates to login page
- [ ] Quick login buttons work for doctor
- [ ] Quick login buttons work for nurse
- [ ] Manual login works
- [ ] Back button returns to welcome

#### ✅ Doctor Pages
- [ ] Dashboard shows stats and recent notes
- [ ] Patients page displays all patients
- [ ] View Details button works
- [ ] Clinical Notes can be created
- [ ] Notes are saved to database
- [ ] AI Analytics loads
- [ ] More page shows calendar and settings

#### ✅ Nurse Pages
- [ ] Dashboard shows tasks and schedule
- [ ] Patient Care workspace loads
- [ ] Nurse notes can be created
- [ ] Task management works
- [ ] Vitals can be recorded
- [ ] Calendar displays

#### ✅ Navigation
- [ ] Tab navigation works for doctors (5 tabs)
- [ ] Tab navigation works for nurses (4 tabs)
- [ ] Active tab is highlighted
- [ ] Logout works from any page

---

## 🚨 Common Issues & Solutions

### Issue: Page doesn't load
**Solution:** Check if module imports work
```python
from pages.doctor import dashboard
dashboard.show()
```

### Issue: API calls fail
**Solution:** Verify API is running on port 8000
```bash
curl http://localhost:8000/health
```

### Issue: Session lost
**Solution:** Check session state initialization in app.py

### Issue: Charts not visible
**Solution:** Ensure plotly layout has white background and black text

---

## 📝 Demo Credentials

### Doctor Account
- **Email:** dr.williams@hospital.com
- **Password:** password123
- **Access:** Full doctor dashboard with all features

### Nurse Account
- **Email:** nurse.davis@hospital.com
- **Password:** password123
- **Access:** Full nurse dashboard with all features

---

## 🎯 Next Steps

### Current Status
- ✅ Modular page structure created
- ✅ Separate doctor and nurse workflows
- ✅ All pages implemented
- ⚠️ Currently using original monolithic app.py

### To Activate Modular Structure
Would need to implement navigation routing in main app.py to load pages dynamically based on user role and selected tab.

### Future Enhancements
- Add page transition animations
- Implement real-time updates with WebSockets
- Add more comprehensive error handling
- Create unit tests for each page
- Add loading states and spinners
- Implement pagination for large data sets

---

## 📞 Support

For issues or questions:
1. Check this workflow guide
2. Review individual page files in `/ui/pages/`
3. Check API documentation at http://localhost:8000/docs
4. Review session state in Streamlit debugger

---

**Last Updated:** November 13, 2025
**Version:** 2.0 (Modular Structure)
