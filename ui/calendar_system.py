"""
Calendar System for Doctors and Nurses
"""
import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta, date
import calendar
import plotly.express as px
import plotly.graph_objects as go

def show_calendar_system():
    """Display calendar system with appointments and follow-ups"""
    
    # Initialize session state for calendar
    if 'calendar_date' not in st.session_state:
        st.session_state.calendar_date = datetime.now()
    
    st.header("📅 Medical Calendar & Scheduling")
    st.markdown("Manage appointments, follow-ups, and patient schedules")
    
    # Calendar tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📅 Calendar View", 
        "📋 Appointments", 
        "🔄 Follow-ups", 
        "📊 Schedule Analytics"
    ])
    
    with tab1:
        st.subheader("📅 Calendar View")
        
        # Calendar navigation
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            if st.button("⬅️ Previous Month"):
                st.session_state.calendar_date = st.session_state.calendar_date - timedelta(days=30)
                st.rerun()
        
        with col2:
            current_date = st.session_state.get('calendar_date', datetime.now())
            st.write(f"**{current_date.strftime('%B %Y')}**")
        
        with col3:
            if st.button("Next Month ➡️"):
                st.session_state.calendar_date = st.session_state.calendar_date + timedelta(days=30)
                st.rerun()
        
        # Calendar display
        display_calendar(current_date)
    
    with tab2:
        st.subheader("📋 Appointments Management")
        
        # Add new appointment
        with st.expander("➕ Add New Appointment", expanded=False):
            with st.form("appointment_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    patient_id = st.text_input("Patient ID")
                    appointment_type = st.selectbox("Type", ["Consultation", "Follow-up", "Procedure", "Emergency"])
                    appointment_date = st.date_input("Date", value=date.today())
                
                with col2:
                    time = st.time_input("Time", value=datetime.now().time())
                    duration = st.selectbox("Duration", ["30 min", "1 hour", "1.5 hours", "2 hours"])
                    notes = st.text_area("Notes")
                
                if st.form_submit_button("Schedule Appointment"):
                    if patient_id and appointment_date and time:
                        # Here you would save to database
                        st.success(f"Appointment scheduled for {appointment_date} at {time}")
                    else:
                        st.error("Please fill in all required fields")
        
        # Today's appointments
        st.subheader("📅 Today's Schedule")
        display_todays_appointments()
    
    with tab3:
        st.subheader("🔄 Patient Follow-ups")
        
        # Follow-up tracking
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.write("**Track patient follow-ups and reminders**")
        
        with col2:
            if st.button("🔄 Refresh Follow-ups"):
                st.rerun()
        
        # Follow-up list
        display_follow_ups()
    
    with tab4:
        st.subheader("📊 Schedule Analytics")
        
        # Analytics charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Appointment distribution
            st.write("**Appointment Distribution**")
            appointment_data = {
                'Type': ['Consultation', 'Follow-up', 'Procedure', 'Emergency'],
                'Count': [15, 8, 3, 2]
            }
            df = pd.DataFrame(appointment_data)
            fig = px.pie(df, values='Count', names='Type', title="Appointment Types")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Weekly schedule
            st.write("**Weekly Schedule Density**")
            days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
            appointments = [8, 12, 10, 15, 9, 3, 1]
            
            fig = px.bar(x=days, y=appointments, title="Appointments by Day")
            st.plotly_chart(fig, use_container_width=True)

def display_calendar(selected_date):
    """Display calendar with appointments"""
    
    # Get calendar data
    year = selected_date.year
    month = selected_date.month
    
    # Create calendar
    cal = calendar.monthcalendar(year, month)
    
    # Calendar header
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    cols = st.columns(7)
    
    for i, day in enumerate(days):
        with cols[i]:
            st.write(f"**{day}**")
    
    # Calendar body
    for week in cal:
        cols = st.columns(7)
        for i, day in enumerate(week):
            with cols[i]:
                if day == 0:
                    st.write("")
                else:
                    # Check for appointments on this day
                    appointment_count = get_appointment_count(day, month, year)
                    
                    if appointment_count > 0:
                        st.write(f"**{day}** 📅")
                        st.caption(f"{appointment_count} appointments")
                    else:
                        st.write(f"{day}")
                    
                    # Add appointment button
                    if st.button("+", key=f"add_{day}_{month}_{year}"):
                        st.session_state.add_appointment_date = date(year, month, day)
                        st.rerun()

def display_todays_appointments():
    """Display today's appointments"""
    
    today = date.today()
    
    # Mock appointment data (in real app, fetch from database)
    appointments = [
        {
            "time": "09:00",
            "patient": "John Smith",
            "type": "Consultation",
            "duration": "1 hour",
            "status": "Confirmed"
        },
        {
            "time": "10:30",
            "patient": "Sarah Johnson", 
            "type": "Follow-up",
            "duration": "30 min",
            "status": "Confirmed"
        },
        {
            "time": "14:00",
            "patient": "Mike Davis",
            "type": "Procedure",
            "duration": "2 hours", 
            "status": "Pending"
        }
    ]
    
    if appointments:
        for apt in appointments:
            with st.container():
                col1, col2, col3, col4 = st.columns([1, 2, 1, 1])
                
                with col1:
                    st.write(f"**{apt['time']}**")
                
                with col2:
                    st.write(f"**{apt['patient']}**")
                    st.caption(f"{apt['type']} - {apt['duration']}")
                
                with col3:
                    status_color = "🟢" if apt['status'] == 'Confirmed' else "🟡"
                    st.write(f"{status_color} {apt['status']}")
                
                with col4:
                    if st.button("View", key=f"view_{apt['time']}"):
                        st.info(f"Viewing appointment for {apt['patient']}")

def display_follow_ups():
    """Display patient follow-ups"""
    
    # Mock follow-up data
    follow_ups = [
        {
            "patient": "Alice Brown",
            "last_visit": "2024-01-15",
            "next_followup": "2024-01-22",
            "condition": "Hypertension",
            "priority": "High",
            "notes": "Monitor blood pressure"
        },
        {
            "patient": "Bob Wilson",
            "last_visit": "2024-01-10", 
            "next_followup": "2024-01-25",
            "condition": "Diabetes",
            "priority": "Medium",
            "notes": "Check blood sugar levels"
        },
        {
            "patient": "Carol Davis",
            "last_visit": "2024-01-12",
            "next_followup": "2024-01-20",
            "condition": "Post-surgery",
            "priority": "High", 
            "notes": "Wound healing check"
        }
    ]
    
    if follow_ups:
        for follow_up in follow_ups:
            with st.container():
                col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
                
                with col1:
                    st.write(f"**{follow_up['patient']}**")
                    st.caption(f"{follow_up['condition']} - {follow_up['notes']}")
                
                with col2:
                    st.write(f"**Next:** {follow_up['next_followup']}")
                
                with col3:
                    priority_color = "🔴" if follow_up['priority'] == 'High' else "🟡"
                    st.write(f"{priority_color} {follow_up['priority']}")
                
                with col4:
                    if st.button("Schedule", key=f"schedule_{follow_up['patient']}"):
                        st.success(f"Scheduling follow-up for {follow_up['patient']}")

def get_appointment_count(day, month, year):
    """Get appointment count for a specific day"""
    # Mock data - in real app, query database
    return 2 if day % 3 == 0 else 0
