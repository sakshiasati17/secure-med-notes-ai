git#!/usr/bin/env python3
"""
Sample data seeder for development and testing
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from api.db.database import SessionLocal, engine
from api.models.user import User, UserRole
from api.models.patient import Patient
from api.models.note import Note, NoteType, NoteStatus
from api.deps import get_password_hash
from datetime import date, datetime

def create_sample_data():
    """Create sample users, patients, and notes for testing"""
    db = SessionLocal()
    
    try:
        # Create sample users
        users_data = [
            {
                "email": "dr.smith@hospital.com",
                "full_name": "Dr. John Smith",
                "role": UserRole.DOCTOR,
                "password": "password123"
            },
            {
                "email": "nurse.johnson@hospital.com", 
                "full_name": "Nurse Sarah Johnson",
                "role": UserRole.NURSE,
                "password": "password123"
            },
            {
                "email": "admin@hospital.com",
                "full_name": "Admin User",
                "role": UserRole.ADMIN,
                "password": "password123"
            }
        ]
        
        for user_data in users_data:
            existing_user = db.query(User).filter(User.email == user_data["email"]).first()
            if not existing_user:
                user = User(
                    email=user_data["email"],
                    full_name=user_data["full_name"],
                    role=user_data["role"],
                    hashed_password=get_password_hash(user_data["password"])
                )
                db.add(user)
        
        db.commit()
        
        # Create sample patients
        patients_data = [
            {
                "patient_id": "P001",
                "first_name": "Alice",
                "last_name": "Johnson",
                "date_of_birth": date(1985, 3, 15),
                "medical_record_number": "MRN001",
                "allergies": "Penicillin, Shellfish",
                "medical_history": "Hypertension, Diabetes Type 2"
            },
            {
                "patient_id": "P002", 
                "first_name": "Bob",
                "last_name": "Smith",
                "date_of_birth": date(1972, 7, 22),
                "medical_record_number": "MRN002",
                "allergies": "None known",
                "medical_history": "Previous appendectomy (2019)"
            },
            {
                "patient_id": "P003",
                "first_name": "Carol",
                "last_name": "Williams", 
                "date_of_birth": date(1990, 11, 8),
                "medical_record_number": "MRN003",
                "allergies": "Latex",
                "medical_history": "Asthma, Migraine"
            }
        ]
        
        for patient_data in patients_data:
            existing_patient = db.query(Patient).filter(
                Patient.patient_id == patient_data["patient_id"]
            ).first()
            if not existing_patient:
                patient = Patient(**patient_data)
                db.add(patient)
        
        db.commit()
        
        # Get user and patient IDs for notes
        dr_smith = db.query(User).filter(User.email == "dr.smith@hospital.com").first()
        nurse_johnson = db.query(User).filter(User.email == "nurse.johnson@hospital.com").first()
        alice = db.query(Patient).filter(Patient.patient_id == "P001").first()
        bob = db.query(Patient).filter(Patient.patient_id == "P002").first()
        carol = db.query(Patient).filter(Patient.patient_id == "P003").first()
        
        # Create sample notes
        notes_data = [
            {
                "patient_id": alice.id,
                "author_id": dr_smith.id,
                "note_type": NoteType.DOCTOR_NOTE,
                "title": "Initial Consultation - Hypertension Management",
                "content": "Patient presents with elevated blood pressure readings over the past month. Current medications include Lisinopril 10mg daily. Patient reports compliance with medication but admits to high sodium diet. Discussed dietary modifications and increased exercise. Plan: Continue current medication, follow up in 2 weeks, dietary counseling referral.",
                "status": NoteStatus.FINALIZED
            },
            {
                "patient_id": alice.id,
                "author_id": nurse_johnson.id,
                "note_type": NoteType.NURSE_NOTE,
                "title": "Vital Signs Check - Morning Round",
                "content": "BP: 145/90, HR: 78, Temp: 98.6°F, O2 Sat: 98%. Patient appears comfortable, no acute distress. Reports mild headache this morning. Blood pressure still elevated despite medication. Notified Dr. Smith of readings.",
                "status": NoteStatus.FINALIZED
            },
            {
                "patient_id": bob.id,
                "author_id": dr_smith.id,
                "note_type": NoteType.DOCTOR_NOTE,
                "title": "Post-Surgical Follow-up",
                "content": "Patient recovering well from appendectomy performed 2 weeks ago. Incision site healing properly, no signs of infection. Patient reports minimal pain, taking OTC pain medication as needed. Cleared for light activities, follow up in 4 weeks.",
                "status": NoteStatus.FINALIZED
            },
            {
                "patient_id": carol.id,
                "author_id": nurse_johnson.id,
                "note_type": NoteType.NURSE_NOTE,
                "title": "Asthma Exacerbation - Emergency Visit",
                "content": "Patient presented with acute shortness of breath and wheezing. Peak flow reading 60% of personal best. Administered albuterol nebulizer treatment. Patient responded well, symptoms improved. Discharged with instructions to continue inhaler regimen and follow up with pulmonologist.",
                "status": NoteStatus.FINALIZED
            }
        ]
        
        for note_data in notes_data:
            existing_note = db.query(Note).filter(
                Note.title == note_data["title"]
            ).first()
            if not existing_note:
                note = Note(**note_data)
                db.add(note)
        
        db.commit()
        print("✅ Sample data created successfully!")
        print("📋 Users created: Dr. Smith, Nurse Johnson, Admin")
        print("👥 Patients created: Alice Johnson, Bob Smith, Carol Williams")
        print("📝 Sample notes created for testing")
        print("\n🔑 Login credentials:")
        print("Doctor: dr.smith@hospital.com / password123")
        print("Nurse: nurse.johnson@hospital.com / password123")
        print("Admin: admin@hospital.com / password123")
        
    except Exception as e:
        print(f"❌ Error creating sample data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_sample_data()
