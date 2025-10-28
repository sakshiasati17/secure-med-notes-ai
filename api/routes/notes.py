from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from api.db.database import get_db
from api.schemas.note import NoteCreate, NoteUpdate, NoteResponse, NoteSummary
from api.models.note import Note
from api.models.user import User
from api.deps import get_current_active_user

router = APIRouter(prefix="/notes", tags=["notes"])

@router.post("/", response_model=NoteResponse)
def create_note(
    note: NoteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    db_note = Note(
        **note.dict(),
        author_id=current_user.id
    )
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

@router.get("/", response_model=List[NoteSummary])
def get_notes(
    skip: int = 0,
    limit: int = 100,
    note_type: str = None,
    patient_id: int = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    query = db.query(Note)
    
    if note_type:
        query = query.filter(Note.note_type == note_type)
    if patient_id:
        query = query.filter(Note.patient_id == patient_id)
    
    notes = query.offset(skip).limit(limit).all()
    
    # Convert to NoteSummary format
    note_summaries = []
    for note in notes:
        note_summaries.append(NoteSummary(
            id=note.id,
            title=note.title,
            note_type=note.note_type,
            summary=note.summary,
            risk_level=note.risk_level,
            created_at=note.created_at,
            author_name=note.author.full_name,
            patient_name=f"{note.patient.first_name} {note.patient.last_name}"
        ))
    
    return note_summaries

@router.get("/{note_id}", response_model=NoteResponse)
def get_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(
            status_code=404,
            detail="Note not found"
        )
    return note

@router.put("/{note_id}", response_model=NoteResponse)
def update_note(
    note_id: int,
    note_update: NoteUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(
            status_code=404,
            detail="Note not found"
        )
    
    # Check if user can edit this note
    if note.author_id != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions to edit this note"
        )
    
    update_data = note_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(note, field, value)
    
    db.commit()
    db.refresh(note)
    return note
