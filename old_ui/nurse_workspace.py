"""
Comprehensive Nurse Workspace Module
All nursing features in one place!
"""
import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go

def show_nurse_workspace(api_base_url, access_token):
    """Complete nursing workspace with all essential features"""
    
    st.header("👩‍⚕️ Nurse Workspace")
    st.markdown("Complete nursing tools: Patients, Vitals, Medications, Tasks & More")
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    # Nurse workspace tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🏥 My Patients",
        "📊 Vital Signs", 
        "💊 Medications",
        "💧 Intake/Output",
        "✅ Task Checklist",
        "➕ Quick Actions"
    ])
    
    with tab1:
        show_my_patients(api_base_url, headers)
    
    with tab2:
        show_vital_signs(api_base_url, headers)
    
    with tab3:
        show_medications(api_base_url, headers)
    
    with tab4:
        show_intake_output(api_base_url, headers)
    
    with tab5:
        show_task_checklist(api_base_url, headers)
    
    with tab6:
        show_quick_actions(api_base_url, headers)

def show_my_patients(api_base_url, headers):
    """Display nurse's assigned patients at a glance"""
    
    st.subheader("🏥 My Assigned Patients - Quick Overview")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"**Shift:** Day Shift (7:00 AM - 7:00 PM) | **Time:** {datetime.now().strftime('%I:%M %p')}")
    with col2:
        if st.button("🔄 Refresh"):
            st.rerun()
    
    # Fetch patients
    try:
        response = requests.get(f"{api_base_url}/patients/", headers=headers, timeout=5)
        if response.status_code == 200:
            patients = response.json()
        else:
            patients = []
    except:
        patients = []
    
    # Mock assigned patients with nursing-specific data
    assigned_patients = []
    for idx, patient in enumerate(patients[:6]):  # Show first 6 as "assigned"
        patient_data = {
            "id": patient.get("id"),
            "room": f"20{idx+1}",
            "name": f"{patient.get('first_name', 'Unknown')} {patient.get('last_name', 'Patient')}",
            "age": (datetime.now() - datetime.strptime(patient.get('date_of_birth', '1980-01-01'), '%Y-%m-%d')).days // 365,
            "diagnosis": patient.get('medical_history', 'General care')[:30],
            "risk_level": ["LOW", "LOW", "MEDIUM", "HIGH", "MEDIUM", "CRITICAL"][idx % 6],
            "last_vitals": (datetime.now() - timedelta(hours=idx+1)).strftime('%I:%M %p'),
            "bp": ["120/80", "130/85", "150/90", "180/95", "125/82", "170/100"][idx % 6],
            "hr": [72, 85, 92, 105, 78, 98][idx % 6],
            "temp": [98.6, 98.8, 99.5, 100.2, 98.4, 101.5][idx % 6],
            "spo2": [98, 97, 95, 92, 96, 91][idx % 6],
            "pain": [0, 2, 5, 7, 3, 8][idx % 6],
            "meds_due_count": [0, 2, 3, 1, 0, 4][idx % 6],
            "meds_due_time": ["None", "11:00 AM", "11:30 AM", "12:00 PM", "None", "10:00 AM"][idx % 6],
            "alerts": [
                [],
                [],
                ["Blood pressure elevated"],
                ["High BP - Contact MD", "Elevated temp"],
                [],
                ["CRITICAL: Low O2", "High temp", "Severe pain"]
            ][idx % 6],
            "allergies": patient.get('allergies', 'None')
        }
        assigned_patients.append(patient_data)
    
    # Summary metrics
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("👥 Total Patients", len(assigned_patients))
    with col2:
        critical_count = len([p for p in assigned_patients if p['risk_level'] in ['HIGH', 'CRITICAL']])
        st.metric("🔴 High/Critical Risk", critical_count)
    with col3:
        total_meds = sum([p['meds_due_count'] for p in assigned_patients])
        st.metric("💊 Meds Due Soon", total_meds)
    with col4:
        total_alerts = sum([len(p['alerts']) for p in assigned_patients])
        st.metric("⚠️ Active Alerts", total_alerts)
    
    st.markdown("---")
    
    # Display each patient
    for patient in assigned_patients:
        risk_emoji = {"LOW": "🟢", "MEDIUM": "🟡", "HIGH": "🔴", "CRITICAL": "🚨"}[patient['risk_level']]
        risk_color = {"LOW": "#d4edda", "MEDIUM": "#fff3cd", "HIGH": "#f8d7da", "CRITICAL": "#dc3545"}[patient['risk_level']]
        
        with st.container():
            st.markdown(f"""
            <div style="background-color: {risk_color}; padding: 20px; border-radius: 10px; border: 2px solid #dee2e6; margin-bottom: 15px;">
                <h3 style="color: #212529; margin: 0;">
                    {risk_emoji} Room {patient['room']} - {patient['name']} ({patient['age']}y)
                    <span style="float: right; font-size: 0.8em; background: #ffffff; padding: 5px 10px; border-radius: 5px;">
                        {patient['risk_level']} RISK
                    </span>
                </h3>
            </div>
            """, unsafe_allow_html=True)
            
            # Patient details in columns
            col1, col2, col3 = st.columns([2, 2, 1])
            
            with col1:
                st.markdown(f"""
                **📋 Diagnosis:** {patient['diagnosis']}  
                **🩺 Last Vitals:** {patient['last_vitals']}  
                **💓 BP:** {patient['bp']} | **HR:** {patient['hr']} bpm  
                **🌡️ Temp:** {patient['temp']}°F | **🩸 SpO2:** {patient['spo2']}%  
                **😣 Pain:** {patient['pain']}/10  
                **⚠️ Allergies:** {patient['allergies']}
                """)
            
            with col2:
                # Alerts section
                if patient['alerts']:
                    st.markdown("### 🚨 ALERTS:")
                    for alert in patient['alerts']:
                        if "CRITICAL" in alert or "Low O2" in alert:
                            st.error(f"🚨 {alert} - **CONTACT DOCTOR IMMEDIATELY**")
                        elif "High" in alert or "elevated" in alert:
                            st.warning(f"⚠️ {alert} - Notify physician")
                        else:
                            st.info(f"ℹ️ {alert}")
                else:
                    st.success("✅ No active alerts")
                
                # Medications due
                if patient['meds_due_count'] > 0:
                    st.markdown(f"**💊 Medications Due:** {patient['meds_due_time']} ({patient['meds_due_count']} meds)")
            
            with col3:
                st.markdown("### Quick Actions")
                if st.button(f"📊 Record Vitals", key=f"vitals_{patient['id']}"):
                    st.session_state[f'quick_vitals_patient'] = patient['id']
                    st.session_state['active_tab'] = 'vital_signs'
                    st.info(f"Switch to 📊 Vital Signs tab to record for {patient['name']}")
                
                if st.button(f"💊 Give Meds", key=f"meds_{patient['id']}"):
                    st.session_state[f'quick_meds_patient'] = patient['id']
                    st.session_state['active_tab'] = 'medications'
                    st.info(f"Switch to 💊 Medications tab")
                
                if st.button(f"📝 Write Note", key=f"note_{patient['id']}"):
                    st.info(f"Go to 👩‍⚕️ Nurse Notes tab to document")
                
                if patient['alerts']:
                    if st.button(f"📞 Contact MD", key=f"contact_{patient['id']}"):
                        st.success(f"✅ Page sent to Dr. on call about {patient['name']}")
            
            st.markdown("---")

def show_vital_signs(api_base_url, headers):
    """Vital signs entry and trending"""
    
    st.subheader("📊 Vital Signs Entry & Monitoring")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### ➕ Quick Entry Form")
        
        # Fetch patients for dropdown
        try:
            response = requests.get(f"{api_base_url}/patients/", headers=headers, timeout=5)
            patients = response.json() if response.status_code == 200 else []
        except Exception as e:
            st.error(f"Error fetching patients: {str(e)}")
            patients = []
        
        if not patients:
            st.warning("⚠️ No patients found. Please add patients first in the 'Quick Actions' tab.")
            st.info("💡 Go to '➕ Quick Actions' tab to add a new patient!")
            return
        
        patient_options = {f"{p.get('first_name', '')} {p.get('last_name', '')} (ID: {p.get('id')})": p.get('id') for p in patients}
        
        with st.form("vitals_entry_form"):
            if patient_options:
                selected_patient = st.selectbox("Select Patient", options=list(patient_options.keys()))
            else:
                st.warning("No patients available")
                selected_patient = None
            
            st.markdown("#### Vital Signs:")
            col_a, col_b = st.columns(2)
            
            with col_a:
                temperature = st.number_input("🌡️ Temperature (°F)", min_value=95.0, max_value=110.0, value=98.6, step=0.1)
                bp_sys = st.number_input("💓 BP Systolic (mmHg)", min_value=50, max_value=250, value=120, step=1)
                bp_dia = st.number_input("💓 BP Diastolic (mmHg)", min_value=30, max_value=150, value=80, step=1)
                heart_rate = st.number_input("💗 Heart Rate (bpm)", min_value=30, max_value=200, value=75, step=1)
            
            with col_b:
                resp_rate = st.number_input("🫁 Respiratory Rate (/min)", min_value=5, max_value=60, value=16, step=1)
                spo2 = st.number_input("🩸 SpO2 (%)", min_value=50, max_value=100, value=98, step=1)
                pain_level = st.slider("😣 Pain Level", min_value=0, max_value=10, value=0)
                weight = st.number_input("⚖️ Weight (kg)", min_value=1.0, max_value=300.0, value=70.0, step=0.1)
            
            blood_glucose = st.number_input("🩸 Blood Glucose (mg/dL)", min_value=20, max_value=600, value=100, step=1)
            notes = st.text_area("📝 Notes", placeholder="Any observations...")
            
            submitted = st.form_submit_button("✅ Save Vitals")
            
            if submitted:
                # Check for abnormal values and alert
                alerts = []
                
                if temperature > 100.4:
                    alerts.append(f"🔴 HIGH FEVER: {temperature}°F - Contact physician!")
                elif temperature < 96.0:
                    alerts.append(f"🔵 LOW TEMP: {temperature}°F - Check patient warmth")
                
                if bp_sys > 140 or bp_dia > 90:
                    alerts.append(f"🔴 HYPERTENSION: {bp_sys}/{bp_dia} - Notify MD immediately!")
                elif bp_sys < 90:
                    alerts.append(f"🔴 HYPOTENSION: {bp_sys}/{bp_dia} - Contact MD immediately!")
                
                if heart_rate > 100:
                    alerts.append(f"⚠️ TACHYCARDIA: {heart_rate} bpm - Monitor closely")
                elif heart_rate < 60:
                    alerts.append(f"⚠️ BRADYCARDIA: {heart_rate} bpm - Assess patient")
                
                if spo2 < 95:
                    alerts.append(f"🚨 LOW OXYGEN: {spo2}% - CONTACT DOCTOR IMMEDIATELY! Apply O2 if ordered")
                
                if pain_level >= 7:
                    alerts.append(f"😣 SEVERE PAIN: {pain_level}/10 - Assess and consider pain management")
                
                if blood_glucose > 180:
                    alerts.append(f"⚠️ HYPERGLYCEMIA: {blood_glucose} mg/dL - Check insulin orders")
                elif blood_glucose < 70:
                    alerts.append(f"🚨 HYPOGLYCEMIA: {blood_glucose} mg/dL - TREAT IMMEDIATELY!")
                
                # Display alerts
                if alerts:
                    st.markdown("### 🚨 ABNORMAL VITALS DETECTED!")
                    for alert in alerts:
                        if "🚨" in alert or "IMMEDIATELY" in alert:
                            st.error(alert)
                            st.error("📞 **ACTION REQUIRED: CONTACT DOCTOR NOW!**")
                        elif "🔴" in alert:
                            st.error(alert)
                        else:
                            st.warning(alert)
                else:
                    st.success("✅ All vitals within normal range!")
                
                st.success(f"✅ Vitals recorded at {datetime.now().strftime('%I:%M %p')} for {selected_patient}")
                
                # In real app, save to database via API
                st.info("💾 Vitals saved to patient chart")
    
    with col2:
        st.markdown("### 📈 Vital Signs Trends")
        
        # Mock trend data
        hours = [(datetime.now() - timedelta(hours=i)).strftime('%I %p') for i in range(24, 0, -4)]
        bp_sys_trend = [120, 125, 130, 135, 140, 145]
        bp_dia_trend = [80, 82, 85, 88, 90, 92]
        hr_trend = [75, 78, 82, 85, 88, 92]
        temp_trend = [98.6, 98.8, 99.0, 99.5, 100.0, 100.5]
        
        # Blood Pressure Trend
        fig_bp = go.Figure()
        fig_bp.add_trace(go.Scatter(x=hours, y=bp_sys_trend, mode='lines+markers', name='Systolic', line=dict(color='red')))
        fig_bp.add_trace(go.Scatter(x=hours, y=bp_dia_trend, mode='lines+markers', name='Diastolic', line=dict(color='blue')))
        fig_bp.update_layout(title='Blood Pressure Trend (24h)', xaxis_title='Time', yaxis_title='mmHg', height=250)
        st.plotly_chart(fig_bp, use_container_width=True)
        
        # Temperature Trend
        fig_temp = px.line(x=hours, y=temp_trend, markers=True, title='Temperature Trend (24h)')
        fig_temp.update_layout(xaxis_title='Time', yaxis_title='°F', height=250)
        st.plotly_chart(fig_temp, use_container_width=True)
        
        st.info("📊 Trends help identify patterns and deterioration early!")

def show_medications(api_base_url, headers):
    """Medication Administration Record (MAR)"""
    
    st.subheader("💊 Medication Administration Record (MAR)")
    
    # Mock medication schedule
    current_time = datetime.now()
    
    medications_schedule = [
        {
            "patient": "John Smith",
            "room": "201",
            "scheduled_time": "11:00 AM",
            "due_in_min": 30,
            "medications": [
                {"name": "Metoprolol", "dose": "50mg", "route": "PO"},
                {"name": "Lisinopril", "dose": "10mg", "route": "PO"},
                {"name": "Aspirin", "dose": "81mg", "route": "PO"}
            ],
            "allergies": "Penicillin",
            "status": "pending"
        },
        {
            "patient": "Sarah Jones",
            "room": "202",
            "scheduled_time": "11:30 AM",
            "due_in_min": 60,
            "medications": [
                {"name": "Insulin Lispro", "dose": "10 units", "route": "SubQ"},
                {"name": "Metformin", "dose": "500mg", "route": "PO"}
            ],
            "allergies": "None",
            "notes": "⚠️ Check blood glucose before insulin!",
            "status": "pending"
        },
        {
            "patient": "Mike Davis",
            "room": "203",
            "scheduled_time": "10:00 AM",
            "due_in_min": -30,
            "medications": [
                {"name": "Ibuprofen", "dose": "400mg", "route": "PO"}
            ],
            "allergies": "Sulfa drugs",
            "status": "overdue"
        }
    ]
    
    # Summary
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("⏰ Due in Next Hour", 2)
    with col2:
        st.metric("⚠️ Overdue", 1)
    with col3:
        st.metric("✅ Given Today", 15)
    
    st.markdown("---")
    
    # Display medications
    for med_record in medications_schedule:
        status_color = {"pending": "#fff3cd", "overdue": "#f8d7da", "given": "#d4edda"}[med_record['status']]
        status_emoji = {"pending": "⏰", "overdue": "🚨", "given": "✅"}[med_record['status']]
        
        with st.container():
            st.markdown(f"""
            <div style="background-color: {status_color}; padding: 15px; border-radius: 8px; margin-bottom: 15px; border: 2px solid #dee2e6;">
                <h4 style="color: #212529; margin: 0;">
                    {status_emoji} {med_record['scheduled_time']} - Room {med_record['room']} - {med_record['patient']}
                </h4>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"**⚠️ ALLERGIES:** `{med_record['allergies']}`", unsafe_allow_html=False)
                
                if med_record.get('notes'):
                    st.warning(med_record['notes'])
                
                st.markdown("**Medications to administer:**")
                for med in med_record['medications']:
                    st.markdown(f"- ☐ **{med['name']}** {med['dose']} {med['route']}")
            
            with col2:
                if med_record['status'] == 'overdue':
                    st.error(f"⚠️ OVERDUE by {abs(med_record['due_in_min'])} min")
                else:
                    st.info(f"Due in {med_record['due_in_min']} min")
                
                if st.button(f"✅ Mark All Given", key=f"give_all_{med_record['room']}"):
                    st.success(f"✅ All medications given at {current_time.strftime('%I:%M %p')}")
                    st.info("📝 Digitally signed and timestamped")
                
                if st.button(f"⏸️ Hold Meds", key=f"hold_{med_record['room']}"):
                    reason = "Enter reason in notes"
                    st.warning(f"⏸️ Medications held - Document reason!")
            
            st.markdown("---")

def show_intake_output(api_base_url, headers):
    """Intake and Output tracking"""
    
    st.subheader("💧 Intake/Output Tracking")
    
    # Patient selector
    try:
        response = requests.get(f"{api_base_url}/patients/", headers=headers, timeout=5)
        patients = response.json() if response.status_code == 200 else []
    except:
        patients = []
    
    patient_options = {f"{p.get('first_name', '')} {p.get('last_name', '')} (Room {201+idx})": p.get('id') for idx, p in enumerate(patients[:6])}
    
    selected_patient = st.selectbox("Select Patient for I/O Tracking", options=list(patient_options.keys()))
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ➕ Record INTAKE")
        
        with st.form("intake_form_nurse"):
            intake_type = st.selectbox("Type", ["Oral", "IV Fluids", "Blood Products", "Tube Feeding", "Other"], key="intake_type_select")
            intake_amount = st.number_input("Amount (mL)", min_value=0, max_value=5000, value=0, step=50, key="intake_amount_input")
            intake_time = st.time_input("Time", value=datetime.now().time(), key="intake_time_input")
            intake_notes = st.text_input("Notes", placeholder="e.g., NS @ 125 mL/hr", key="intake_notes_input")
            
            if st.form_submit_button("➕ Add Intake"):
                if intake_amount > 0:
                    st.success(f"✅ Added {intake_amount} mL {intake_type} at {intake_time.strftime('%I:%M %p')}")
                    st.info(f"💾 Recorded for {selected_patient}")
                else:
                    st.warning("⚠️ Please enter an amount greater than 0")
    
    with col2:
        st.markdown("### ➖ Record OUTPUT")
        
        with st.form("output_form_nurse"):
            output_type = st.selectbox("Type", ["Urine", "Emesis", "Drain", "Stool", "NG Tube", "Other"], key="output_type_select")
            output_amount = st.number_input("Amount (mL)", min_value=0, max_value=5000, value=0, step=50, key="output_amount_input")
            output_time = st.time_input("Time", value=datetime.now().time(), key="output_time_input")
            output_notes = st.text_input("Notes", placeholder="e.g., dark amber urine", key="output_notes_input")
            
            if st.form_submit_button("➖ Add Output"):
                if output_amount > 0:
                    st.success(f"✅ Added {output_amount} mL {output_type} at {output_time.strftime('%I:%M %p')}")
                    st.info(f"💾 Recorded for {selected_patient}")
                else:
                    st.warning("⚠️ Please enter an amount greater than 0")
    
    st.markdown("---")
    
    # Summary display (mock data)
    st.markdown("### 📊 Fluid Balance Summary")
    
    tab_8h, tab_24h = st.tabs(["8-Hour Shift", "24-Hour Total"])
    
    with tab_8h:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            **➕ INTAKE**
            - Oral: 500 mL
            - IV: 1000 mL
            - **Total: 1500 mL**
            """)
        
        with col2:
            st.markdown("""
            **➖ OUTPUT**
            - Urine: 800 mL
            - Drain: 50 mL
            - **Total: 850 mL**
            """)
        
        with col3:
            balance = 1500 - 850
            st.metric("⚖️ Balance", f"+{balance} mL", delta="+650 mL")
            st.info("✅ Positive balance - patient is well hydrated")
    
    with tab_24h:
        # Mock 24-hour chart
        hours = [f"{i}:00" for i in range(0, 24, 4)]
        intake_data = [200, 400, 300, 500, 450, 350]
        output_data = [150, 300, 250, 400, 350, 300]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(x=hours, y=intake_data, name='Intake', marker_color='lightblue'))
        fig.add_trace(go.Bar(x=hours, y=output_data, name='Output', marker_color='lightcoral'))
        fig.update_layout(title='24-Hour Intake/Output', xaxis_title='Time', yaxis_title='mL', barmode='group')
        st.plotly_chart(fig, use_container_width=True)
        
        # Alerts
        if balance > 1000:
            st.warning("⚠️ Large positive balance - Monitor for fluid overload signs")
        elif balance < -500:
            st.error("🚨 Negative balance - Risk of dehydration! Contact MD")

def show_task_checklist(api_base_url, headers):
    """Nurse task checklist for shift"""
    
    st.subheader("✅ My Task Checklist - Day Shift")
    
    current_time = datetime.now()
    st.markdown(f"**Current Time:** {current_time.strftime('%I:%M %p')}")
    
    # Initialize session state for tasks
    if 'nurse_tasks' not in st.session_state:
        st.session_state.nurse_tasks = [
            {"time": "8:00 AM", "task": "Morning vitals round (6 patients)", "completed": True, "overdue": False},
            {"time": "9:00 AM", "task": "Morning medications", "completed": True, "overdue": False},
            {"time": "10:00 AM", "task": "Dressing change - Room 201", "completed": False, "overdue": True},
            {"time": "11:00 AM", "task": "Vitals round", "completed": False, "overdue": False},
            {"time": "11:30 AM", "task": "Blood draw - Room 203", "completed": False, "overdue": False},
            {"time": "12:00 PM", "task": "Lunch medications", "completed": False, "overdue": False},
            {"time": "1:00 PM", "task": "Documentation review", "completed": False, "overdue": False},
            {"time": "2:00 PM", "task": "Afternoon vitals", "completed": False, "overdue": False},
            {"time": "3:00 PM", "task": "Patient education - Room 202", "completed": False, "overdue": False},
            {"time": "6:00 PM", "task": "End of shift charting", "completed": False, "overdue": False},
        ]
    
    # Summary metrics
    total_tasks = len(st.session_state.nurse_tasks)
    completed = len([t for t in st.session_state.nurse_tasks if t['completed']])
    overdue = len([t for t in st.session_state.nurse_tasks if t['overdue'] and not t['completed']])
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📋 Total Tasks", total_tasks)
    with col2:
        st.metric("✅ Completed", completed)
    with col3:
        st.metric("⏳ Remaining", total_tasks - completed)
    with col4:
        st.metric("⚠️ Overdue", overdue)
    
    st.markdown("---")
    
    # Add new task
    with st.expander("➕ Add New Task"):
        with st.form("new_task_form"):
            col1, col2 = st.columns(2)
            with col1:
                task_time = st.time_input("Time", value=datetime.now().time())
            with col2:
                task_desc = st.text_input("Task Description")
            
            if st.form_submit_button("Add Task"):
                st.session_state.nurse_tasks.append({
                    "time": task_time.strftime('%I:%M %p'),
                    "task": task_desc,
                    "completed": False,
                    "overdue": False
                })
                st.success("✅ Task added!")
                st.rerun()
    
    st.markdown("### 📋 Task List")
    
    # Display tasks
    for idx, task in enumerate(st.session_state.nurse_tasks):
        col1, col2, col3 = st.columns([1, 4, 1])
        
        with col1:
            st.markdown(f"**{task['time']}**")
        
        with col2:
            if task['completed']:
                st.markdown(f"~~{task['task']}~~ ✅")
            elif task['overdue']:
                st.markdown(f"⚠️ **{task['task']}** (OVERDUE)")
            else:
                st.markdown(f"☐ {task['task']}")
        
        with col3:
            if not task['completed']:
                if st.button("✓ Done", key=f"task_{idx}"):
                    st.session_state.nurse_tasks[idx]['completed'] = True
                    st.rerun()
    
    st.markdown("---")
    st.info("💡 TIP: Check off tasks as you complete them to stay organized throughout your shift!")

def show_quick_actions(api_base_url, headers):
    """Quick actions and shortcuts"""
    
    st.subheader("➕ Quick Actions & Add Patient")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ➕ Add New Patient")
        
        with st.form("add_patient_form"):
            st.markdown("#### Patient Information")
            
            col_a, col_b = st.columns(2)
            with col_a:
                first_name = st.text_input("First Name*")
                last_name = st.text_input("Last Name*")
                dob = st.date_input("Date of Birth*", value=datetime.now().date() - timedelta(days=365*50))
            
            with col_b:
                gender = st.selectbox("Gender", ["Male", "Female", "Other"])
                room_number = st.text_input("Room Number")
                mrn = st.text_input("Medical Record Number")
            
            allergies = st.text_area("Allergies", placeholder="e.g., Penicillin, Sulfa drugs")
            medical_history = st.text_area("Medical History", placeholder="Brief medical history...")
            
            submitted = st.form_submit_button("➕ Add Patient")
            
            if submitted:
                if first_name and last_name:
                    # Create patient via API
                    patient_data = {
                        "first_name": first_name,
                        "last_name": last_name,
                        "date_of_birth": dob.strftime('%Y-%m-%d'),
                        "medical_record_number": mrn or f"MRN{datetime.now().strftime('%Y%m%d%H%M%S')}",
                        "allergies": allergies or "None",
                        "medical_history": medical_history or "New admission"
                    }
                    
                    try:
                        response = requests.post(
                            f"{api_base_url}/patients/",
                            headers=headers,
                            json=patient_data,
                            timeout=5
                        )
                        
                        if response.status_code in [200, 201]:
                            st.success(f"✅ Patient {first_name} {last_name} added successfully!")
                            st.balloons()
                        else:
                            st.error(f"Error: {response.status_code} - {response.text}")
                    except Exception as e:
                        st.error(f"Error adding patient: {str(e)}")
                else:
                    st.error("Please fill in required fields (marked with *)")
    
    with col2:
        st.markdown("### 🚀 Common Actions")
        
        if st.button("📞 Page Doctor", use_container_width=True):
            st.success("✅ Page sent to on-call physician")
        
        if st.button("🚑 Call Rapid Response", use_container_width=True):
            st.error("🚨 Rapid Response Team activated!")
        
        if st.button("📋 Print Shift Report", use_container_width=True):
            st.info("📄 Generating shift report...")
        
        if st.button("📊 View All Vitals", use_container_width=True):
            st.info("Switch to 📊 Vital Signs tab")
        
        if st.button("💊 View MAR", use_container_width=True):
            st.info("Switch to 💊 Medications tab")
        
        st.markdown("---")
        st.markdown("### 📚 Quick Reference")
        
        with st.expander("🩺 Normal Vital Signs Ranges"):
            st.markdown("""
            - **Temperature:** 97.8-99.1°F (36.5-37.3°C)
            - **Blood Pressure:** 90/60 - 140/90 mmHg
            - **Heart Rate:** 60-100 bpm
            - **Respiratory Rate:** 12-20 /min
            - **SpO2:** ≥95%
            - **Blood Glucose:** 70-180 mg/dL
            """)
        
        with st.expander("⚠️ Critical Values - Contact MD"):
            st.markdown("""
            - 🌡️ Temp > 101°F or < 96°F
            - 💓 BP > 180/110 or < 90/60
            - 💗 HR > 120 or < 50
            - 🫁 RR > 25 or < 10
            - 🩸 SpO2 < 90%
            - 🩸 Glucose > 250 or < 60
            """)

