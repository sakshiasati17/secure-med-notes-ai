"""
Comprehensive Patient Dashboard
Shows patient history, visits, common problems, disease tracking, follow-ups
"""
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from collections import Counter

def show_patient_dashboard(API_BASE_URL, access_token):
    """Display comprehensive patient dashboard"""
    
    st.header("👥 Patient Management Dashboard")
    st.markdown("Complete patient history, visits, and health tracking")
    
    # Get all patients from API
    headers = {"Authorization": f"Bearer {access_token}"}
    
    # Fetch real patients from API
    try:
        response = requests.get(f"{API_BASE_URL}/patients/", headers=headers, timeout=5)
        if response.status_code == 200:
            api_patients = response.json()
            # Debug info
            st.sidebar.info(f"📊 Total Patients in DB: {len(api_patients)}")
        else:
            api_patients = []
            st.sidebar.warning(f"⚠️ API returned status: {response.status_code}")
    except Exception as e:
        api_patients = []
        st.sidebar.error(f"❌ Error loading patients: {str(e)}")
    
    # Search patient
    st.markdown("### 🔍 Search Patient")
    col1, col2 = st.columns([3, 1])
    
    with col1:
        patient_search = st.text_input("Search by ID or Name", placeholder="Enter patient ID or name...", key="patient_search_input")
    
    with col2:
        search_button = st.button("🔎 Search", type="primary")
    
    # Handle search
    if search_button and patient_search:
        st.markdown("---")
        st.subheader("🔍 Search Results")
        
        # Try searching by ID first
        if patient_search.isdigit():
            patient_id = int(patient_search)
            try:
                response = requests.get(f"{API_BASE_URL}/patients/{patient_id}", headers=headers, timeout=5)
                if response.status_code == 200:
                    patient = response.json()
                    
                    # Display found patient
                    st.success(f"✅ Patient found!")
                    
                    col_a, col_b = st.columns([2, 1])
                    
                    with col_a:
                        st.markdown(f"""
                        <div style="padding: 25px; border-radius: 10px; background-color: #e8f5e9; border: 3px solid #4caf50;">
                            <h2 style="color: #2e7d32; margin: 0;">👤 {patient.get('first_name', '')} {patient.get('last_name', '')}</h2>
                            <hr style="border: 1px solid #4caf50;">
                            <p style="color: #212529; font-size: 16px; margin: 8px 0;"><strong>📋 Patient ID:</strong> {patient.get('id', 'N/A')}</p>
                            <p style="color: #212529; font-size: 16px; margin: 8px 0;"><strong>🎂 Date of Birth:</strong> {patient.get('date_of_birth', 'N/A')}</p>
                            <p style="color: #212529; font-size: 16px; margin: 8px 0;"><strong>🏥 MRN:</strong> {patient.get('medical_record_number', 'N/A')}</p>
                            <p style="color: #212529; font-size: 16px; margin: 8px 0;"><strong>⚠️ Allergies:</strong> {patient.get('allergies', 'None')}</p>
                            <p style="color: #212529; font-size: 16px; margin: 8px 0;"><strong>📝 Medical History:</strong> {patient.get('medical_history', 'None')}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col_b:
                        st.markdown("### Quick Actions")
                        if st.button("📝 Create Note", key="search_create_note"):
                            st.info("Navigate to Notes tab to create")
                        if st.button("📊 View All Notes", key="search_view_notes"):
                            st.info("Fetching notes...")
                            # Fetch patient notes
                            try:
                                notes_resp = requests.get(f"{API_BASE_URL}/notes/", headers=headers, timeout=5)
                                if notes_resp.status_code == 200:
                                    all_notes = notes_resp.json()
                                    patient_notes = [n for n in all_notes if n.get('patient_id') == patient_id]
                                    
                                    if patient_notes:
                                        st.success(f"Found {len(patient_notes)} notes")
                                        for note in patient_notes[:5]:
                                            with st.expander(f"📄 {note.get('title', 'Untitled')}"):
                                                st.write(f"**Date:** {note.get('created_at', '')[:10]}")
                                                st.write(f"**Type:** {note.get('note_type', 'N/A')}")
                                                st.write(f"**Content:** {note.get('content', '')[:200]}...")
                                    else:
                                        st.info("No notes found for this patient")
                            except:
                                st.error("Error fetching notes")
                else:
                    st.error(f"❌ Patient with ID {patient_id} not found")
            except Exception as e:
                st.error(f"Error searching: {str(e)}")
        else:
            # Search by name (search in both first and last name)
            search_lower = patient_search.lower().strip()
            
            # More comprehensive search
            matching_patients = []
            for p in api_patients:
                first_name = (p.get('first_name', '') or '').lower()
                last_name = (p.get('last_name', '') or '').lower()
                full_name = f"{first_name} {last_name}".strip()
                
                # Check if search term is in first name, last name, or full name
                if (search_lower in first_name or 
                    search_lower in last_name or 
                    search_lower in full_name):
                    matching_patients.append(p)
            
            if matching_patients:
                st.success(f"✅ Found {len(matching_patients)} matching patient(s) for '{patient_search}'")
                
                # Show all matching patients in cards (not expanders for better visibility)
                for idx, patient in enumerate(matching_patients):
                    st.markdown(f"""
                    <div style="padding: 20px; border-radius: 10px; background-color: #e3f2fd; border: 2px solid #2196f3; margin-bottom: 15px;">
                        <h3 style="color: #1565c0; margin: 0;">👤 {patient.get('first_name', '')} {patient.get('last_name', '')} (ID: {patient.get('id', 'N/A')})</h3>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    col_a, col_b, col_c = st.columns([2, 2, 1])
                    with col_a:
                        st.write(f"**📋 Patient ID:** {patient.get('id', 'N/A')}")
                        st.write(f"**🎂 DOB:** {patient.get('date_of_birth', 'N/A')}")
                    with col_b:
                        st.write(f"**🏥 MRN:** {patient.get('medical_record_number', 'N/A')}")
                        st.write(f"**⚠️ Allergies:** {patient.get('allergies', 'None')}")
                    with col_c:
                        if st.button(f"📄 Details", key=f"details_{patient.get('id')}_{idx}", use_container_width=True):
                            st.session_state.selected_patient = patient.get('id')
                            st.rerun()
                    
                    # Show more info in expander
                    with st.expander(f"View Medical History & Notes"):
                        st.write(f"**📝 Medical History:**")
                        st.info(patient.get('medical_history', 'No medical history recorded'))
                        
                        # Try to fetch notes
                        try:
                            notes_resp = requests.get(f"{API_BASE_URL}/notes/", headers=headers, timeout=5)
                            if notes_resp.status_code == 200:
                                all_notes = notes_resp.json()
                                patient_notes = [n for n in all_notes if n.get('patient_id') == patient.get('id')]
                                
                                if patient_notes:
                                    st.write(f"**📋 Notes ({len(patient_notes)} total):**")
                                    for note in patient_notes[:3]:
                                        st.markdown(f"- **{note.get('title', 'Untitled')}** ({note.get('created_at', '')[:10]})")
                                else:
                                    st.write("No notes found")
                        except:
                            st.write("Could not fetch notes")
            else:
                st.warning(f"❌ No patients found matching '{patient_search}'")
                st.info(f"💡 Searched in {len(api_patients)} total patients. Try searching by first name, last name, or patient ID.")
        
        st.markdown("---")
    
    # Tabs for different views
    tab1, tab2, tab3 = st.tabs(["📊 Patient Overview", "🏥 Individual Patient", "📈 Analytics"])
    
    with tab1:
        st.subheader("All Patients Overview")
        
        # Mock patient data - in production, fetch from API
        patients_data = [
            {
                "id": 1,
                "name": "John Smith",
                "age": 45,
                "last_visit": "2024-01-15",
                "total_visits": 12,
                "common_conditions": ["Hypertension", "Diabetes Type 2"],
                "risk_level": "MEDIUM",
                "next_followup": "2024-02-15"
            },
            {
                "id": 2,
                "name": "Sarah Johnson",
                "age": 32,
                "last_visit": "2024-01-18",
                "total_visits": 5,
                "common_conditions": ["Asthma", "Seasonal Allergies"],
                "risk_level": "LOW",
                "next_followup": "2024-03-01"
            },
            {
                "id": 3,
                "name": "Mike Davis",
                "age": 58,
                "last_visit": "2024-01-20",
                "total_visits": 28,
                "common_conditions": ["Heart Disease", "High Cholesterol", "Hypertension"],
                "risk_level": "HIGH",
                "next_followup": "2024-01-25"
            }
        ]
        
        # Display patient cards
        cols = st.columns(3)
        for idx, patient in enumerate(patients_data):
            with cols[idx % 3]:
                risk_color = "🔴" if patient['risk_level'] == "HIGH" else "🟡" if patient['risk_level'] == "MEDIUM" else "🟢"
                
                with st.container():
                    st.markdown(f"""
                    <div style="padding: 20px; border-radius: 10px; background-color: #ffffff; border: 2px solid #e0e0e0; margin-bottom: 10px;">
                        <h3 style="color: #1976d2; margin-bottom: 10px;">{patient['name']}</h3>
                        <p style="color: #2c3e50; margin: 5px 0;"><strong>Age:</strong> {patient['age']}</p>
                        <p style="color: #2c3e50; margin: 5px 0;"><strong>Total Visits:</strong> {patient['total_visits']}</p>
                        <p style="color: #2c3e50; margin: 5px 0;"><strong>Last Visit:</strong> {patient['last_visit']}</p>
                        <p style="color: #2c3e50; margin: 5px 0;"><strong>Risk:</strong> {risk_color} {patient['risk_level']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button(f"View Details", key=f"view_{patient['id']}"):
                        st.session_state.selected_patient = patient['id']
                        st.rerun()
        
        # Summary statistics
        st.markdown("---")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Patients", len(patients_data))
        with col2:
            high_risk = len([p for p in patients_data if p['risk_level'] == "HIGH"])
            st.metric("High Risk", high_risk, delta=f"{high_risk/len(patients_data)*100:.1f}%")
        with col3:
            avg_visits = sum([p['total_visits'] for p in patients_data]) / len(patients_data)
            st.metric("Avg Visits", f"{avg_visits:.1f}")
        with col4:
            pending_followups = len([p for p in patients_data if p['next_followup']])
            st.metric("Pending Follow-ups", pending_followups)
    
    with tab2:
        st.subheader("Individual Patient Details")
        
        # Select patient
        selected_id = st.session_state.get('selected_patient', 1)
        
        # Mock detailed patient data
        patient_detail = {
            "id": 1,
            "name": "John Smith",
            "age": 45,
            "gender": "Male",
            "blood_type": "O+",
            "phone": "+1-555-0123",
            "email": "john.smith@email.com",
            "address": "123 Main St, City, State",
            "emergency_contact": "Jane Smith (Wife) - +1-555-0124",
            "insurance": "Blue Cross Blue Shield - #ABC123456",
            "allergies": ["Penicillin", "Peanuts"],
            "total_visits": 12,
            "first_visit": "2022-03-15",
            "last_visit": "2024-01-15",
            "common_conditions": ["Hypertension", "Diabetes Type 2"],
            "current_medications": [
                "Lisinopril 10mg - Daily",
                "Metformin 500mg - Twice daily",
                "Aspirin 81mg - Daily"
            ],
            "visit_history": [
                {"date": "2024-01-15", "reason": "Routine checkup", "doctor": "Dr. Smith", "summary": "BP controlled, continue medications"},
                {"date": "2023-12-10", "reason": "Follow-up", "doctor": "Dr. Smith", "summary": "Blood sugar levels improving"},
                {"date": "2023-11-05", "reason": "Urgent - Chest pain", "doctor": "Dr. Johnson", "summary": "ECG normal, anxiety-related"},
                {"date": "2023-10-15", "reason": "Routine checkup", "doctor": "Dr. Smith", "summary": "All vitals stable"},
                {"date": "2023-09-20", "reason": "Follow-up", "doctor": "Dr. Smith", "summary": "Medication adjustment needed"}
            ],
            "vital_trends": {
                "dates": ["Sep", "Oct", "Nov", "Dec", "Jan"],
                "blood_pressure_sys": [140, 135, 130, 128, 125],
                "blood_pressure_dia": [90, 88, 85, 84, 82],
                "blood_sugar": [180, 165, 150, 145, 140],
                "weight": [185, 183, 180, 178, 176]
            }
        }
        
        # Patient Header
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f"## 👤 {patient_detail['name']}")
            st.markdown(f"**Age:** {patient_detail['age']} | **Gender:** {patient_detail['gender']} | **Blood Type:** {patient_detail['blood_type']}")
            st.markdown(f"**Total Visits:** {patient_detail['total_visits']} | **First Visit:** {patient_detail['first_visit']} | **Last Visit:** {patient_detail['last_visit']}")
        
        with col2:
            st.info(f"📞 {patient_detail['phone']}\n📧 {patient_detail['email']}")
        
        # Main content tabs
        ptab1, ptab2, ptab3, ptab4, ptab5 = st.tabs([
            "📋 Overview", 
            "🏥 Visit History", 
            "📊 Health Trends", 
            "💊 Medications",
            "🔔 Alerts & Follow-ups"
        ])
        
        with ptab1:
            st.subheader("Patient Overview")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Contact Information:**")
                st.write(f"📍 {patient_detail['address']}")
                st.write(f"🚨 Emergency: {patient_detail['emergency_contact']}")
                st.write(f"🏥 Insurance: {patient_detail['insurance']}")
                
                st.markdown("**Common Conditions:**")
                for condition in patient_detail['common_conditions']:
                    st.write(f"• {condition}")
            
            with col2:
                st.markdown("**Allergies:** ⚠️")
                for allergy in patient_detail['allergies']:
                    st.error(f"🚫 {allergy}")
                
                st.markdown("**Current Medications:**")
                for med in patient_detail['current_medications']:
                    st.write(f"💊 {med}")
        
        with ptab2:
            st.subheader("Complete Visit History")
            
            st.write(f"**Total Visits:** {patient_detail['total_visits']}")
            st.write(f"**Period:** {patient_detail['first_visit']} to {patient_detail['last_visit']}")
            
            # Visit timeline
            for visit in patient_detail['visit_history']:
                with st.expander(f"📅 {visit['date']} - {visit['reason']}"):
                    st.write(f"**Doctor:** {visit['doctor']}")
                    st.write(f"**Summary:** {visit['summary']}")
                    
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.info(f"💡 **For Nurses:** Monitor patient's response to treatment adjustments made during this visit.")
                    with col2:
                        if st.button("View Full Note", key=f"note_{visit['date']}"):
                            st.info("Full clinical note would be displayed here")
        
        with ptab3:
            st.subheader("Health Trends & Vitals")
            
            # Blood Pressure Trend
            fig_bp = go.Figure()
            fig_bp.add_trace(go.Scatter(
                x=patient_detail['vital_trends']['dates'],
                y=patient_detail['vital_trends']['blood_pressure_sys'],
                name='Systolic',
                line=dict(color='red', width=3)
            ))
            fig_bp.add_trace(go.Scatter(
                x=patient_detail['vital_trends']['dates'],
                y=patient_detail['vital_trends']['blood_pressure_dia'],
                name='Diastolic',
                line=dict(color='blue', width=3)
            ))
            fig_bp.update_layout(title="Blood Pressure Trends", xaxis_title="Month", yaxis_title="mmHg")
            st.plotly_chart(fig_bp, use_container_width=True)
            
            # Blood Sugar Trend
            fig_bs = px.line(
                x=patient_detail['vital_trends']['dates'],
                y=patient_detail['vital_trends']['blood_sugar'],
                title="Blood Sugar Trends",
                labels={'x': 'Month', 'y': 'mg/dL'}
            )
            st.plotly_chart(fig_bs, use_container_width=True)
            
            # Weight Trend
            fig_wt = px.bar(
                x=patient_detail['vital_trends']['dates'],
                y=patient_detail['vital_trends']['weight'],
                title="Weight Trends",
                labels={'x': 'Month', 'y': 'lbs'}
            )
            st.plotly_chart(fig_wt, use_container_width=True)
            
            # Insights
            st.success("✅ **Positive Trends:** Blood pressure is decreasing, indicating good medication response.")
            st.info("💡 **For Nurses:** Continue monitoring BP at each visit and report any readings above 140/90.")
        
        with ptab4:
            st.subheader("Medication Management")
            
            st.markdown("**Current Active Medications:**")
            
            for idx, med in enumerate(patient_detail['current_medications'], 1):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"{idx}. {med}")
                with col2:
                    if st.button("Details", key=f"med_{idx}"):
                        st.info(f"Full medication details for: {med}")
            
            st.markdown("---")
            st.markdown("**Medication History:**")
            st.write("• Previous medications discontinued: None")
            st.write("• Last medication change: 2023-11-05")
            
            st.warning("⚠️ **Nurse Alert:** Patient is on blood thinners (Aspirin). Monitor for bleeding.")
        
        with ptab5:
            st.subheader("Alerts & Follow-ups")
            
            # Active alerts
            st.markdown("**Active Alerts:** 🔔")
            st.error("🚨 **HIGH PRIORITY:** Follow-up appointment due in 5 days (Jan 25)")
            st.warning("⚠️ **MEDIUM:** Lab work needed - Fasting blood sugar and HbA1c")
            
            # Follow-up schedule
            st.markdown("**Follow-up Schedule:**")
            followups = [
                {"date": "2024-01-25", "type": "Routine Check-up", "doctor": "Dr. Smith", "status": "Scheduled"},
                {"date": "2024-02-15", "type": "Lab Review", "doctor": "Dr. Smith", "status": "Pending"},
                {"date": "2024-03-15", "type": "3-Month Review", "doctor": "Dr. Smith", "status": "To Schedule"}
            ]
            
            for followup in followups:
                status_color = "🟢" if followup['status'] == "Scheduled" else "🟡"
                st.write(f"{status_color} **{followup['date']}** - {followup['type']} with {followup['doctor']} ({followup['status']})")
            
            # Recommendations
            st.markdown("**Doctor's Recommendations:**")
            st.info("""
            1. Continue current medication regimen
            2. Monitor blood pressure at home daily
            3. Follow diabetic diet plan
            4. Exercise 30 minutes daily
            5. Schedule lab work before next visit
            """)
            
            st.markdown("**Nursing Care Plan:**")
            st.success("""
            • Verify medication compliance at each visit
            • Educate on proper BP monitoring technique
            • Review diet diary and provide feedback
            • Assess foot health (diabetic foot care)
            • Check injection sites if patient starts insulin
            """)
    
    with tab3:
        st.subheader("Patient Analytics")
        
        # Visit frequency analysis
        col1, col2 = st.columns(2)
        
        with col1:
            # Most common conditions
            all_conditions = ["Hypertension", "Diabetes", "Asthma", "Heart Disease", "Allergies", "Hypertension", "Diabetes"]
            condition_counts = Counter(all_conditions)
            
            fig = px.pie(
                values=list(condition_counts.values()),
                names=list(condition_counts.keys()),
                title="Most Common Conditions"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Visit frequency by month
            months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
            visits = [45, 52, 48, 55, 50, 53]
            
            fig = px.bar(x=months, y=visits, title="Patient Visits by Month")
            st.plotly_chart(fig, use_container_width=True)
        
        # Risk distribution
        st.subheader("Risk Level Distribution")
        risk_data = {"HIGH": 5, "MEDIUM": 15, "LOW": 30}
        fig = px.bar(x=list(risk_data.keys()), y=list(risk_data.values()), 
                    title="Patient Risk Distribution",
                    color=list(risk_data.keys()),
                    color_discrete_map={"HIGH": "red", "MEDIUM": "orange", "LOW": "green"})
        st.plotly_chart(fig, use_container_width=True)
