from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any
import asyncio

from api.db.database import get_db
from api.models.user import User
from api.models.patient import Patient
from api.models.note import Note
from api.deps import get_current_active_user
from api.agents.summarization_agent import SummarizationAgent
from api.agents.risk_agent import RiskAssessmentAgent

router = APIRouter(prefix="/ai", tags=["ai"])

# Initialize agents
summarization_agent = SummarizationAgent()
risk_agent = RiskAssessmentAgent()

@router.post("/summarize/{note_id}")
async def summarize_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Generate AI summary for a specific note"""
    try:
        # Get note and patient
        note = db.query(Note).filter(Note.id == note_id).first()
        if not note:
            raise HTTPException(status_code=404, detail="Note not found")
        
        patient = db.query(Patient).filter(Patient.id == note.patient_id).first()
        if not patient:
            raise HTTPException(status_code=404, detail="Patient not found")
        
        # Process note with AI
        result = summarization_agent.process_note(note, patient, db)
        
        if result["success"]:
            return {
                "message": "Note summarized successfully",
                "summary": result["summary"],
                "risk_level": result["risk_level"],
                "recommendations": result["recommendations"],
                "tags": result["tags"]
            }
        else:
            raise HTTPException(status_code=500, detail=f"AI processing failed: {result['error']}")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing note: {str(e)}")

@router.get("/risk-report/{patient_id}")
async def get_patient_risk_report(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get comprehensive risk report for a patient"""
    try:
        risk_report = risk_agent.generate_patient_risk_report(patient_id, db)
        
        if "error" in risk_report:
            raise HTTPException(status_code=404, detail=risk_report["error"])
        
        return risk_report
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating risk report: {str(e)}")

@router.get("/high-risk-patients")
async def get_high_risk_patients(
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get list of high-risk patients"""
    try:
        high_risk_patients = risk_agent.get_high_risk_patients(db, limit)
        return {
            "high_risk_patients": high_risk_patients,
            "count": len(high_risk_patients)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching high-risk patients: {str(e)}")

@router.post("/batch-summarize")
async def batch_summarize_notes(
    request_data: Dict[str, List[int]],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Batch process multiple notes for AI summarization"""
    try:
        note_ids = request_data.get("note_ids", [])
        results = []
        
        for note_id in note_ids:
            note = db.query(Note).filter(Note.id == note_id).first()
            if note:
                patient = db.query(Patient).filter(Patient.id == note.patient_id).first()
                if patient:
                    result = summarization_agent.process_note(note, patient, db)
                    results.append({
                        "note_id": note_id,
                        "success": result["success"],
                        "summary": result.get("summary"),
                        "risk_level": result.get("risk_level"),
                        "error": result.get("error")
                    })
        
        return {
            "message": f"Processed {len(results)} notes",
            "results": results
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in batch processing: {str(e)}")

@router.get("/ai-status")
async def get_ai_status():
    """Check AI service status and configuration"""
    try:
        # Test AI service availability
        from api.services.ai_service import MedicalAIService
        ai_service = MedicalAIService()
        
        return {
            "status": "operational" if ai_service.enabled else "disabled",
            "openai_configured": bool(ai_service.enabled and hasattr(ai_service, 'openai_api_key') and ai_service.openai_api_key),
            "models_available": ai_service.enabled,
            "vector_store_ready": ai_service.enabled and ai_service.vectorstore is not None
        }
    
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "openai_configured": False,
            "models_available": False,
            "vector_store_ready": False
        }
