from sqlalchemy.orm import Session
from app.models import KnowledgeBase
from app.schemas import KnowledgeBaseSchema

def get_all_knowledge_entries(db: Session):
    """Retrieves all knowledge base entries."""
    return db.query(KnowledgeBase).all()

def add_knowledge_entry(db: Session, entry_data: KnowledgeBaseSchema):
    """Adds a new knowledge base entry."""
    new_entry = KnowledgeBase(**entry_data.dict())
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return new_entry

def update_knowledge_entry(db: Session, entry_id: int, entry_data: KnowledgeBaseSchema):
    """Updates an existing knowledge base entry."""
    db_entry = db.query(KnowledgeBase).filter(KnowledgeBase.id == entry_id).first()
    if not db_entry:
        return None
    for key, value in entry_data.dict().items():
        setattr(db_entry, key, value)
    db.commit()
    return db_entry

def delete_knowledge_entry(db: Session, entry_id: int):
    """Deletes a knowledge base entry by ID."""
    db_entry = db.query(KnowledgeBase).filter(KnowledgeBase.id == entry_id).first()
    if not db_entry:
        return None
    db.delete(db_entry)
    db.commit()
    return db_entry