from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import KnowledgeBase
from app.services.auth_service import get_current_user

router = APIRouter()

class KnowledgeBaseEntry(BaseModel):
    title: str
    content: str
    category: str
    source: str  # 'manual' or 'ai_generated'

@router.get("/knowledge-base/entries")
def get_knowledge_entries(db: Session = Depends(get_db)):
    """Retrieve all knowledge base entries."""
    entries = db.query(KnowledgeBase).all()
    return entries

@router.post("/knowledge-base/add")
def add_knowledge_entry(entry: KnowledgeBaseEntry, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    """Add a new knowledge base entry."""
    new_entry = KnowledgeBase(**entry.dict())
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return {"message": "Entry added successfully", "entry": new_entry}

@router.put("/knowledge-base/update/{id}")
def update_knowledge_entry(id: int, entry: KnowledgeBaseEntry, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    """Update an existing knowledge base entry."""
    db_entry = db.query(KnowledgeBase).filter(KnowledgeBase.id == id).first()
    if not db_entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    for key, value in entry.dict().items():
        setattr(db_entry, key, value)
    db.commit()
    return {"message": "Entry updated successfully"}

@router.delete("/knowledge-base/delete/{id}")
def delete_knowledge_entry(id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    """Delete a knowledge base entry."""
    db_entry = db.query(KnowledgeBase).filter(KnowledgeBase.id == id).first()
    if not db_entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    db.delete(db_entry)
    db.commit()
    return {"message": "Entry deleted successfully"}
