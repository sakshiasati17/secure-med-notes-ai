"""
Notifications and Alerts System
"""
import streamlit as st
import requests
from datetime import datetime, timedelta
import json

def show_notifications():
    """Display notifications and alerts system"""
    
    st.header("🔔 Notifications & Alerts")
    st.markdown("Stay updated with important patient alerts and system notifications")
    
    # Notification tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "🚨 Critical Alerts", 
        "📋 Patient Alerts", 
        "⚙️ System Notifications", 
        "🔧 Alert Settings"
    ])
    
    with tab1:
        st.subheader("🚨 Critical Alerts")
        
        # Critical alerts
        critical_alerts = [
            {
                "type": "High Risk Patient",
                "patient": "John Smith",
                "message": "Blood pressure critically high - immediate attention required",
                "timestamp": "2024-01-15 14:30",
                "priority": "Critical",
                "action_required": True
            },
            {
                "type": "Medication Alert", 
                "patient": "Sarah Johnson",
                "message": "Patient missed 2 consecutive medication doses",
                "timestamp": "2024-01-15 12:15",
                "priority": "High",
                "action_required": True
            },
            {
                "type": "System Alert",
                "patient": "System",
                "message": "AI analysis service temporarily unavailable",
                "timestamp": "2024-01-15 10:45",
                "priority": "Medium",
                "action_required": False
            }
        ]
        
        for alert in critical_alerts:
            with st.container():
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    priority_color = "🔴" if alert['priority'] == 'Critical' else "🟡" if alert['priority'] == 'High' else "🟢"
                    st.write(f"{priority_color} **{alert['type']}**")
                    st.write(f"**Patient:** {alert['patient']}")
                    st.write(f"**Message:** {alert['message']}")
                    st.caption(f"Time: {alert['timestamp']}")
                
                with col2:
                    if alert['action_required']:
                        if st.button("Take Action", key=f"action_{alert['timestamp']}"):
                            st.success("Action taken - alert acknowledged")
                    else:
                        st.info("No action required")
                
                with col3:
                    if st.button("Dismiss", key=f"dismiss_{alert['timestamp']}"):
                        st.info("Alert dismissed")
                
                st.divider()
    
    with tab2:
        st.subheader("📋 Patient Alerts")
        
        # Patient-specific alerts
        patient_alerts = [
            {
                "patient": "Mike Davis",
                "alert_type": "Follow-up Due",
                "message": "Follow-up appointment scheduled for tomorrow",
                "due_date": "2024-01-16",
                "status": "Pending"
            },
            {
                "patient": "Alice Brown", 
                "alert_type": "Test Results",
                "message": "Lab results available for review",
                "due_date": "2024-01-15",
                "status": "New"
            },
            {
                "patient": "Bob Wilson",
                "alert_type": "Medication Review",
                "message": "Medication effectiveness review due",
                "due_date": "2024-01-18",
                "status": "Scheduled"
            }
        ]
        
        # Filter options
        col1, col2 = st.columns([2, 1])
        
        with col1:
            filter_status = st.selectbox("Filter by Status", ["All", "New", "Pending", "Scheduled"])
        
        with col2:
            if st.button("🔄 Refresh Alerts"):
                st.rerun()
        
        # Display filtered alerts
        filtered_alerts = [a for a in patient_alerts if filter_status == "All" or a['status'] == filter_status]
        
        for alert in filtered_alerts:
            with st.container():
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    status_color = "🔵" if alert['status'] == 'New' else "🟡" if alert['status'] == 'Pending' else "🟢"
                    st.write(f"{status_color} **{alert['patient']}** - {alert['alert_type']}")
                    st.write(f"**Message:** {alert['message']}")
                    st.caption(f"Due: {alert['due_date']}")
                
                with col2:
                    if st.button("View Details", key=f"details_{alert['patient']}"):
                        st.info(f"Viewing details for {alert['patient']}")
                
                with col3:
                    if st.button("Mark Done", key=f"done_{alert['patient']}"):
                        st.success(f"Alert for {alert['patient']} marked as done")
                
                st.divider()
    
    with tab3:
        st.subheader("⚙️ System Notifications")
        
        # System notifications
        system_notifications = [
            {
                "type": "System Update",
                "message": "New AI features available - enhanced risk assessment",
                "timestamp": "2024-01-15 09:00",
                "read": False
            },
            {
                "type": "Maintenance",
                "message": "Scheduled maintenance tonight 2:00 AM - 4:00 AM",
                "timestamp": "2024-01-15 08:30",
                "read": True
            },
            {
                "type": "Feature Update",
                "message": "Calendar system updated with new appointment types",
                "timestamp": "2024-01-14 16:45",
                "read": True
            }
        ]
        
        # Notification controls
        col1, col2 = st.columns([2, 1])
        
        with col1:
            show_read = st.checkbox("Show read notifications", value=False)
        
        with col2:
            if st.button("Mark All Read"):
                st.success("All notifications marked as read")
        
        # Display notifications
        filtered_notifications = [n for n in system_notifications if show_read or not n['read']]
        
        for notification in filtered_notifications:
            with st.container():
                col1, col2 = st.columns([4, 1])
                
                with col1:
                    read_indicator = "✅" if notification['read'] else "🔵"
                    st.write(f"{read_indicator} **{notification['type']}**")
                    st.write(notification['message'])
                    st.caption(f"Time: {notification['timestamp']}")
                
                with col2:
                    if not notification['read']:
                        if st.button("Mark Read", key=f"read_{notification['timestamp']}"):
                            st.success("Notification marked as read")
                            st.rerun()
                
                st.divider()
    
    with tab4:
        st.subheader("🔧 Alert Settings")
        
        # Alert preferences
        st.write("**Configure your notification preferences**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Critical Alerts**")
            critical_email = st.checkbox("Email notifications", value=True)
            critical_sms = st.checkbox("SMS notifications", value=True)
            critical_push = st.checkbox("Push notifications", value=True)
            
            st.write("**Patient Alerts**")
            patient_email = st.checkbox("Email for patient alerts", value=True)
            patient_push = st.checkbox("Push for patient alerts", value=False)
        
        with col2:
            st.write("**System Notifications**")
            system_email = st.checkbox("Email for system updates", value=False)
            system_push = st.checkbox("Push for system updates", value=True)
            
            st.write("**Schedule Alerts**")
            schedule_email = st.checkbox("Email for appointments", value=True)
            schedule_push = st.checkbox("Push for appointments", value=True)
        
        # Alert frequency
        st.write("**Alert Frequency**")
        frequency = st.selectbox("How often to check for alerts", 
                               ["Real-time", "Every 5 minutes", "Every 15 minutes", "Every hour"])
        
        # Save settings
        if st.button("💾 Save Settings", type="primary"):
            settings = {
                "critical_email": critical_email,
                "critical_sms": critical_sms,
                "critical_push": critical_push,
                "patient_email": patient_email,
                "patient_push": patient_push,
                "system_email": system_email,
                "system_push": system_push,
                "schedule_email": schedule_email,
                "schedule_push": schedule_push,
                "frequency": frequency
            }
            st.success("Settings saved successfully!")
            st.json(settings)
