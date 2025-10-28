"""
AI Analysis Dashboard for Doctors
"""
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta, timezone
import json

def show_ai_dashboard():
    """Display comprehensive AI analysis dashboard"""
    
    st.header("🤖 AI Analysis Dashboard")
    st.markdown("Advanced AI-powered insights and analytics for clinical decision making")
    
    # Get AI status
    ai_status = requests.get("http://localhost:8000/ai/ai-status", 
                           headers={"Authorization": f"Bearer {st.session_state.access_token}"})
    
    if ai_status.status_code == 200:
        st.success("✅ AI Services: Operational")
    else:
        st.error("❌ AI Services: Not Available")
        return
    
    # Dashboard tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Patient Analytics", 
        "🔍 AI Insights", 
        "⚠️ Risk Monitoring", 
        "📈 Trends & Patterns",
        "🎯 Recommendations"
    ])
    
    with tab1:
        st.subheader("Patient Analytics Overview")
        
        # Get all notes for analysis
        notes_response = requests.get("http://localhost:8000/notes/", 
                                   headers={"Authorization": f"Bearer {st.session_state.access_token}"})
        
        if notes_response.status_code == 200:
            notes = notes_response.json()
            
            # Create analytics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                total_notes = len(notes)
                st.metric("Total Notes", total_notes)
            
            with col2:
                doctor_notes = len([n for n in notes if n.get('note_type') == 'doctor_note'])
                st.metric("Doctor Notes", doctor_notes)
            
            with col3:
                nurse_notes = len([n for n in notes if n.get('note_type') == 'nurse_note'])
                st.metric("Nurse Notes", nurse_notes)
            
            with col4:
                ai_processed = len([n for n in notes if n.get('summary')])
                st.metric("AI Processed", ai_processed)
            
            # Patient activity chart
            if notes:
                st.subheader("📈 Patient Activity Timeline")
                
                # Convert to DataFrame for plotting
                df = pd.DataFrame(notes)
                df['created_at'] = pd.to_datetime(df['created_at'])
                df['date'] = df['created_at'].dt.date
                
                # Daily activity
                daily_activity = df.groupby(['date', 'note_type']).size().reset_index(name='count')
                
                fig = px.bar(daily_activity, x='date', y='count', color='note_type',
                           title="Daily Note Activity by Type",
                           labels={'count': 'Number of Notes', 'date': 'Date'})
                st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("🔍 AI-Generated Insights")
        
        # AI processing controls
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.write("**Process all notes with AI for comprehensive analysis**")
        
        with col2:
            if st.button("🚀 Run Full AI Analysis", type="primary"):
                with st.spinner("Running comprehensive AI analysis..."):
                    # Process all unprocessed notes
                    unprocessed_notes = [n for n in notes if not n.get('summary')]
                    for note in unprocessed_notes:
                        requests.post(f"http://localhost:8000/ai/summarize/{note['id']}", 
                                    headers={"Authorization": f"Bearer {st.session_state.access_token}"})
                    st.success(f"Processed {len(unprocessed_notes)} notes!")
                    st.rerun()
        
        # Display AI insights
        processed_notes = [n for n in notes if n.get('summary')]
        
        if processed_notes:
            st.subheader("📋 AI Analysis Results")
            
            for note in processed_notes[:5]:  # Show first 5
                with st.expander(f"🔬 {note['title']} - {note['created_at'][:10]}"):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.write("**AI Summary:**")
                        st.write(note.get('summary', 'No summary available'))
                        
                        if note.get('recommendations'):
                            st.write("**AI Recommendations:**")
                            st.write(note['recommendations'])
                    
                    with col2:
                        if note.get('risk_level'):
                            risk_color = "🔴" if note['risk_level'].upper() == 'HIGH' else "🟡" if note['risk_level'].upper() == 'MEDIUM' else "🟢"
                            st.write(f"**Risk Level:** {risk_color} {note['risk_level']}")
                        
                        if note.get('tags'):
                            st.write("**Tags:**")
                            tags = note['tags'].split(',') if note['tags'] else []
                            for tag in tags:
                                st.write(f"• {tag.strip()}")
        else:
            st.info("No AI-processed notes available. Click 'Run Full AI Analysis' to start.")
    
    with tab3:
        st.subheader("⚠️ Risk Monitoring Dashboard")
        
        # Get high-risk patients
        risk_response = requests.get("http://localhost:8000/ai/high-risk-patients", 
                                  headers={"Authorization": f"Bearer {st.session_state.access_token}"})
        
        if risk_response.status_code == 200:
            risk_data = risk_response.json()
            high_risk_patients = risk_data.get('high_risk_patients', [])
            
            if high_risk_patients:
                # Risk distribution chart
                risk_levels = [p.get('risk_level', 'UNKNOWN') for p in high_risk_patients]
                risk_counts = pd.Series(risk_levels).value_counts()
                
                fig = px.pie(values=risk_counts.values, names=risk_counts.index,
                           title="Risk Level Distribution",
                           color_discrete_map={
                               'CRITICAL': '#FF0000',
                               'HIGH': '#FF6B6B', 
                               'MEDIUM': '#FFE66D',
                               'LOW': '#4ECDC4'
                           })
                st.plotly_chart(fig, use_container_width=True)
                
                # High-risk patients table
                st.subheader("🚨 High-Risk Patients")
                risk_df = pd.DataFrame(high_risk_patients)
                st.dataframe(risk_df[['patient_name', 'risk_level', 'last_note_date', 'recommendations']], 
                           use_container_width=True)
            else:
                st.info("No high-risk patients identified.")
        else:
            st.error("Could not fetch risk data.")
    
    with tab4:
        st.subheader("📈 Trends & Patterns Analysis")
        
        if notes:
            # Note type trends
            df = pd.DataFrame(notes)
            df['created_at'] = pd.to_datetime(df['created_at'])
            df['hour'] = df['created_at'].dt.hour
            df['day_of_week'] = df['created_at'].dt.day_name()
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Hourly activity
                hourly_activity = df.groupby('hour').size()
                fig = px.bar(x=hourly_activity.index, y=hourly_activity.values,
                           title="Activity by Hour of Day",
                           labels={'x': 'Hour', 'y': 'Number of Notes'})
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Day of week activity
                daily_activity = df.groupby('day_of_week').size()
                fig = px.bar(x=daily_activity.index, y=daily_activity.values,
                           title="Activity by Day of Week",
                           labels={'x': 'Day', 'y': 'Number of Notes'})
                st.plotly_chart(fig, use_container_width=True)
            
            # Content analysis
            st.subheader("📝 Content Analysis")
            
            # Most common words in notes
            all_content = ' '.join([n.get('content', '') for n in notes])
            if all_content:
                # Simple word frequency (basic implementation)
                words = all_content.lower().split()
                word_freq = pd.Series(words).value_counts().head(10)
                
                # Create dataframe for plotly
                word_df = pd.DataFrame({
                    'word': word_freq.index,
                    'count': word_freq.values
                })
                
                fig = px.bar(word_df, x='count', y='word',
                           orientation='h', title="Most Common Words in Notes")
                st.plotly_chart(fig, use_container_width=True)
    
    with tab5:
        st.subheader("🎯 AI Recommendations & Next Steps")
        
        # Generate recommendations based on data
        recommendations = []
        
        if notes:
            # Analyze patterns and generate recommendations
            now_aware = datetime.now(timezone.utc)
            recent_notes = []
            for n in notes:
                try:
                    note_time = datetime.fromisoformat(n['created_at'].replace('Z', '+00:00'))
                    if note_time > now_aware - timedelta(days=7):
                        recent_notes.append(n)
                except (ValueError, TypeError):
                    # Skip notes with invalid dates
                    continue
            
            if len(recent_notes) > 10:
                recommendations.append("📈 High activity detected - consider reviewing patient load")
            
            unprocessed = len([n for n in notes if not n.get('summary')])
            if unprocessed > 0:
                recommendations.append(f"🤖 {unprocessed} notes pending AI analysis")
            
            # Risk-based recommendations
            risk_response = requests.get("http://localhost:8000/ai/high-risk-patients", 
                                      headers={"Authorization": f"Bearer {st.session_state.access_token}"})
            if risk_response.status_code == 200:
                risk_data = risk_response.json()
                high_risk_count = len(risk_data.get('high_risk_patients', []))
                if high_risk_count > 0:
                    recommendations.append(f"⚠️ {high_risk_count} high-risk patients need attention")
        
        if recommendations:
            for i, rec in enumerate(recommendations, 1):
                st.info(f"{i}. {rec}")
        else:
            st.success("✅ All systems running smoothly - no immediate recommendations")
        
        # Action buttons
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📊 Generate Report", help="Generate comprehensive analytics report"):
                st.info("Report generation feature coming soon!")
        
        with col2:
            if st.button("🔔 Set Alerts", help="Configure AI-powered alerts"):
                st.info("Alert configuration coming soon!")
        
        with col3:
            if st.button("📤 Export Data", help="Export analytics data"):
                st.info("Data export feature coming soon!")
