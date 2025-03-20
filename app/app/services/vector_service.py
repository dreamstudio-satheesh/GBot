from sqlalchemy.orm import Session
from app.models import VectorIndex
from app.schemas import VectorIndexSchema

def store_vector_embedding(db: Session, vector_data: VectorIndexSchema):
    """Stores a new vector embedding in the database."""
    new_vector = VectorIndex(**vector_data.dict())
    db.add(new_vector)
    db.commit()
    db.refresh(new_vector)
    return new_vector

def get_all_vector_entries(db: Session):
    """Retrieves all stored vector embeddings."""
    return db.query(VectorIndex).all()

def search_vector_entries(db: Session, query_vector: list):
    """Performs a similarity search using pgvector cosine similarity."""
    try:
        search_query = """
        SELECT id, knowledge_id, embedding_vector, model_used, 
               1 - (embedding_vector <=> CAST(:query_vector AS VECTOR)) AS similarity
        FROM vector_index
        ORDER BY similarity DESC
        LIMIT 5;
        """
        results = db.execute(search_query, {"query_vector": query_vector}).fetchall()
        return results
    except Exception as e:
        return {"error": str(e)}

def delete_vector_entry(db: Session, vector_id: int):
    """Deletes a vector entry by ID."""
    db_entry = db.query(VectorIndex).filter(VectorIndex.id == vector_id).first()
    if not db_entry:
        return None
    db.delete(db_entry)
    db.commit()
    return db_entry
