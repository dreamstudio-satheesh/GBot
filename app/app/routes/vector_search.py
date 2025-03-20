from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.vector_service import (
    store_vector_embedding,
    search_vector_entries,
    get_all_vector_entries,
    delete_vector_entry
)
from app.services.auth_service import get_current_user

router = APIRouter()

class VectorSearchQuery(BaseModel):
    query_text: str  # Text to search for

class VectorStoreEntry(BaseModel):
    knowledge_id: int
    text: str  # Text to generate embedding from

@router.post("/vector-search/query")
def search_vector(query: VectorSearchQuery, db: Session = Depends(get_db)):
    """Perform a similarity search based on input text."""
    results = search_vector_entries(db, query.query_text)
    if not results:
        raise HTTPException(status_code=404, detail="No similar entries found")
    return results

@router.post("/vector-search/store")
def store_vector(entry: VectorStoreEntry, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    """Store a new vector embedding from text."""
    new_vector = store_vector_embedding(db, entry.knowledge_id, entry.text)
    return {"message": "Vector entry stored successfully", "entry": new_vector}

@router.get("/vector-search/entries")
def get_vector_entries(db: Session = Depends(get_db)):
    """Retrieve all stored vector embeddings."""
    return get_all_vector_entries(db)

@router.delete("/vector-search/delete/{id}")
def delete_vector(id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    """Delete a vector entry by ID."""
    deleted_entry = delete_vector_entry(db, id)
    if not deleted_entry:
        raise HTTPException(status_code=404, detail="Vector entry not found")
    return {"message": "Vector entry deleted successfully"}
