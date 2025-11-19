"""
Pre-built Note Templates System
"""
import streamlit as st

# Define note templates
NOTE_TEMPLATES = {
    "Emergency Room Note": {
        "category": "Emergency",
        "template": """**Chief Complaint:**
[Enter chief complaint]

**History of Present Illness:**
[Describe the patient's condition and symptoms]

**Physical Examination:**
- Vital Signs: BP___ HR___ RR___ Temp___ SpO2___
- General: [Alert/Oriented]
- HEENT: [Normal findings or abnormalities]
- Cardiovascular: [Heart sounds, rhythm]
- Respiratory: [Breath sounds, effort]
- Abdomen: [Soft, tender, bowel sounds]
- Extremities: [Pulses, edema]
- Neurological: [Consciousness, reflexes]

**Diagnostic Studies:**
[Labs, imaging, EKG findings]

**Assessment:**
[Primary diagnosis and differential diagnoses]

**Plan:**
1. [Treatment plan]
2. [Medications prescribed]
3. [Consultations requested]
4. [Disposition: Admit/Discharge/Transfer]

**Follow-up:**
[Instructions for follow-up care]
"""
    },
    
    "Surgery Note": {
        "category": "Surgical",
        "template": """**Pre-operative Diagnosis:**
[Enter diagnosis]

**Post-operative Diagnosis:**
[Enter diagnosis]

**Procedure:**
[Name of surgical procedure performed]

**Surgeon:**
[Attending surgeon name]

**Assistant:**
[Assistant surgeon/team members]

**Anesthesia:**
[Type: General/Regional/Local]

**Indications:**
[Reason for surgery]

**Findings:**
[Operative findings]

**Procedure Details:**
[Step-by-step description of procedure]

**Estimated Blood Loss:**
[Volume in mL]

**Specimens:**
[Tissue/samples sent to pathology]

**Complications:**
[None or describe complications]

**Disposition:**
- Patient transferred to [PACU/ICU/Floor]
- Condition: [Stable/Critical]
- Vital Signs: BP___ HR___ RR___ SpO2___

**Post-operative Plan:**
1. [Pain management]
2. [Medications]
3. [Activity level]
4. [Diet]
5. [Follow-up appointments]
"""
    },
    
    "Consultation Note": {
        "category": "Consultation",
        "template": """**Consultation Request:**
[Reason for consultation]

**Referring Physician:**
[Name and specialty]

**History of Present Illness:**
[Relevant history]

**Past Medical History:**
[Significant medical conditions]

**Medications:**
[Current medications list]

**Allergies:**
[Drug/food allergies]

**Physical Examination:**
[Focused examination relevant to consultation]

**Review of Systems:**
[Pertinent positives and negatives]

**Diagnostic Data Reviewed:**
[Labs, imaging, studies]

**Assessment:**
[Consultant's diagnosis and opinion]

**Recommendations:**
1. [Specific recommendations]
2. [Further testing needed]
3. [Treatment modifications]
4. [Follow-up plan]

**Thank you for this consultation.**
[Consultant name and signature]
"""
    },
    
    "Follow-up Note": {
        "category": "Follow-up",
        "template": """**Follow-up Visit:**
[Date since last visit]

**Interval History:**
[Changes since last visit]

**Current Symptoms:**
[Patient's current complaints]

**Medication Compliance:**
[Adherence to prescribed medications]

**Vital Signs:**
BP___ HR___ RR___ Temp___ Weight___

**Physical Examination:**
[Focused exam]

**Lab/Imaging Results:**
[Recent test results]

**Assessment:**
[Current status of condition]

**Plan:**
1. [Continue/modify current treatment]
2. [New medications or interventions]
3. [Additional testing needed]
4. [Next follow-up appointment]

**Patient Education:**
[Instructions given to patient]
"""
    },
    
    "Discharge Summary": {
        "category": "Discharge",
        "template": """**Admission Date:**
[Date]

**Discharge Date:**
[Date]

**Length of Stay:**
[Number of days]

**Admitting Diagnosis:**
[Primary diagnosis on admission]

**Discharge Diagnosis:**
1. [Primary diagnosis]
2. [Secondary diagnoses]

**Hospital Course:**
[Summary of hospital stay and treatment]

**Procedures Performed:**
[List of procedures]

**Medications on Admission:**
[List]

**Discharge Medications:**
1. [Medication - Dose - Frequency - Duration]
2. [Medication - Dose - Frequency - Duration]

**Condition on Discharge:**
[Stable/Improved/Unchanged]

**Discharge Instructions:**
1. Activity: [Restrictions/recommendations]
2. Diet: [Dietary recommendations]
3. Wound Care: [If applicable]
4. Warning Signs: [When to seek medical attention]

**Follow-up Appointments:**
- [Provider name] in [timeframe]
- [Additional appointments]

**Discharge Disposition:**
[Home/Skilled Nursing Facility/Rehabilitation]
"""
    },
    
    "Progress Note": {
        "category": "Inpatient",
        "template": """**Date:**
[Current date]

**Hospital Day:**
[Number]

**Subjective:**
[Patient's complaints and concerns]

**Objective:**
Vitals: BP___ HR___ RR___ Temp___ SpO2___
Physical Exam: [Focused findings]
Labs: [Relevant values]
Imaging: [Results]

**Assessment:**
[Current status of each problem]

**Plan:**
Problem 1: [Diagnosis]
- [Treatment plan]

Problem 2: [Diagnosis]
- [Treatment plan]

**Overall Assessment:**
[Patient's overall status]

**Disposition:**
[Continue care/Consider discharge/Transfer]
"""
    },
    
    "Nurse Progress Note": {
        "category": "Nursing",
        "template": """**Shift:**
[Day/Night, Time]

**Patient Status:**
Alert and oriented x [1/2/3/4]

**Vital Signs:**
- Time: [__:__]
- BP: ___/___
- HR: ___
- RR: ___
- Temp: ___°F
- SpO2: ___%
- Pain Level: [0-10]

**Systems Assessment:**
Cardiovascular: [Normal/Abnormal findings]
Respiratory: [Normal/Abnormal findings]
GI: [Bowel sounds, last BM, diet tolerance]
GU: [Urine output, color]
Skin: [Integrity, wounds]
Neuro: [LOC, motor/sensory]

**IV Access:**
[Site, patent, no signs of infection]

**Medications Administered:**
[Time - Medication - Dose - Route]

**Intake/Output:**
Intake: ___ mL
Output: ___ mL

**Activities:**
[Ambulation, PT/OT, procedures]

**Patient/Family Education:**
[Topics covered]

**Plan:**
[Continuing care needs]

**Concerns:**
[Issues requiring follow-up]
"""
    },
    
    "Psychiatric Evaluation": {
        "category": "Psychiatry",
        "template": """**Chief Complaint:**
[In patient's own words]

**History of Present Illness:**
[Detailed psychiatric history]

**Psychiatric History:**
- Previous Diagnoses: [List]
- Previous Hospitalizations: [Dates and reasons]
- Suicide Attempts: [History]
- Self-Harm: [History]

**Substance Use History:**
[Alcohol, drugs, tobacco]

**Medications:**
[Current psychiatric and other medications]

**Social History:**
- Living Situation: [Details]
- Occupation: [Status]
- Support System: [Family, friends]
- Legal Issues: [If any]

**Mental Status Examination:**
- Appearance: [Grooming, dress]
- Behavior: [Cooperative, agitated, etc.]
- Speech: [Rate, tone, volume]
- Mood: [Patient's description]
- Affect: [Observed emotional expression]
- Thought Process: [Linear, tangential, etc.]
- Thought Content: [Delusions, hallucinations]
- Suicidal Ideation: [Present/Absent, plan, intent]
- Homicidal Ideation: [Present/Absent]
- Insight: [Good/Fair/Poor]
- Judgment: [Good/Fair/Poor]
- Cognition: [Orientation, memory, concentration]

**Assessment:**
[DSM-5 diagnoses]

**Safety Assessment:**
[Risk level and protective factors]

**Plan:**
1. [Treatment recommendations]
2. [Medication management]
3. [Therapy recommendations]
4. [Safety plan]
5. [Follow-up schedule]
"""
    }
}

def show_template_selector():
    """Display template selector and return selected template"""
    
    st.subheader("📋 Note Templates Library")
    
    # Category filter
    categories = ["All"] + list(set([t["category"] for t in NOTE_TEMPLATES.values()]))
    selected_category = st.selectbox("Filter by Category", categories)
    
    # Filter templates
    if selected_category == "All":
        filtered_templates = NOTE_TEMPLATES
    else:
        filtered_templates = {k: v for k, v in NOTE_TEMPLATES.items() if v["category"] == selected_category}
    
    # Template selection
    col1, col2 = st.columns([3, 1])
    
    with col1:
        template_name = st.selectbox(
            "Select Template",
            options=["None"] + list(filtered_templates.keys()),
            help="Choose a pre-built template to start your note"
        )
    
    with col2:
        if st.button("Preview Template", disabled=(template_name == "None")):
            st.session_state.show_template_preview = True
    
    # Show preview
    if template_name != "None" and st.session_state.get('show_template_preview', False):
        with st.expander("📄 Template Preview", expanded=True):
            st.markdown(NOTE_TEMPLATES[template_name]["template"])
            
            if st.button("Use This Template"):
                st.session_state.selected_template = NOTE_TEMPLATES[template_name]["template"]
                st.session_state.show_template_preview = False
                st.success(f"Template '{template_name}' loaded!")
                return NOTE_TEMPLATES[template_name]["template"]
    
    return st.session_state.get('selected_template', "")

def get_template_content(template_name):
    """Get template content by name"""
    if template_name in NOTE_TEMPLATES:
        return NOTE_TEMPLATES[template_name]["template"]
    return ""
