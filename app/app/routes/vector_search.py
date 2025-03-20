from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import VectorIndex
from app.services.auth_service import get_current_user

router = APIRouter()

class VectorSearchQuery(BaseModel):
    query_vector: list  # Embedding vector for search

class VectorStoreEntry(BaseModel):
    knowledge_id: int
    embedding_vector: list
    model_used: str

@router.post("/vector-search/query")
def search_vector_entries(query: VectorSearchQuery, db: Session = Depends(get_db)):
    """Perform a similarity search using vector embeddings."""
    try:
        # TODO: Implement similarity search logic (pgvector cosine similarity)
        results = db.query(VectorIndex).all()
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/vector-search/store")
def store_vector_entry(entry: VectorStoreEntry, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    """Store a new vector embedding."""
    new_entry = VectorIndex(**entry.dict())
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return {"message": "Vector entry stored successfully", "entry": new_entry}

@router.get("/vector-search/entries")
def get_vector_entries(db: Session = Depends(get_db)):
    """Retrieve all stored vector embeddings."""
    return db.query(VectorIndex).all()

@router.delete("/vector-search/delete/{id}")
def delete_vector_entry(id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    """Delete a vector entry by ID."""
    db_entry = db.query(VectorIndex).filter(VectorIndex.id == id).first()
    if not db_entry:
        raise HTTPException(status_code=404, detail="Vector entry not found")
    db.delete(db_entry)
    db.commit()
    return {"message": "Vector entry deleted successfully"}
