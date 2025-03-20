from sqlalchemy.orm import Session
from sentence_transformers import SentenceTransformer
import numpy as np
from app.models import VectorIndex

# Load sentence-transformer model once
embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def generate_embedding(text: str) -> list:
    """Generate a vector embedding for the given text."""
    embedding = embedding_model.encode(text, convert_to_numpy=True)
    return embedding.tolist()  # Convert NumPy array to a list for DB storage

def store_vector_embedding(db: Session, knowledge_id: int, text: str, model_used: str = "MiniLM"):
    """Generate and store vector embeddings for a knowledge base entry."""
    embedding_vector = generate_embedding(text)

    new_vector = VectorIndex(
        knowledge_id=knowledge_id,
        embedding_vector=embedding_vector,
        model_used=model_used
    )
    db.add(new_vector)
    db.commit()
    db.refresh(new_vector)
    return new_vector

def get_all_vector_entries(db: Session):
    """Retrieve all stored vector embeddings."""
    return db.query(VectorIndex).all()

def search_vector_entries(db: Session, query_text: str):
    """Perform a similarity search using pgvector cosine similarity."""
    query_vector = generate_embedding(query_text)  # Convert input text to vector

    search_query = """
    SELECT id, knowledge_id, embedding_vector, model_used, 
           1 - (embedding_vector <=> CAST(:query_vector AS VECTOR)) AS similarity
    FROM vector_index
    ORDER BY similarity DESC
    LIMIT 5;
    """

    results = db.execute(search_query, {"query_vector": query_vector}).fetchall()
    return [{"id": r[0], "knowledge_id": r[1], "similarity": r[4]} for r in results]

def delete_vector_entry(db: Session, vector_id: int):
    """Delete a vector entry by ID."""
    db_entry = db.query(VectorIndex).filter(VectorIndex.id == vector_id).first()
    if not db_entry:
        return None
    db.delete(db_entry)
    db.commit()
    return db_entry
