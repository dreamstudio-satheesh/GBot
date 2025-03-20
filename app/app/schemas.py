from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, ARRAY, Float
from sqlalchemy.orm import relationship
from app.database import Base
from pydantic import BaseModel, EmailStr
from typing import List, Optional

# User Schemas
class UserCreate(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    is_active: bool

    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class APIKeyResponse(BaseModel):
    id: int
    api_key: str
    status: str

class APIKeyCreate(BaseModel):
    user_id: int

# Knowledge Base Model
class KnowledgeBase(Base):
    __tablename__ = "knowledge_base"
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id", ondelete="CASCADE"))
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    category = Column(String)
    source = Column(String, nullable=False)  # 'manual' or 'ai_generated'
    created_at = Column(TIMESTAMP, server_default="now()")

# Vector Index Model
class VectorIndex(Base):
    __tablename__ = "vector_index"
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id", ondelete="CASCADE"))
    knowledge_id = Column(Integer, ForeignKey("knowledge_base.id", ondelete="CASCADE"))
    embedding_vector = Column(ARRAY(Float))  # Vector embedding storage
    model_used = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, server_default="now()")

# Pydantic Schemas
class KnowledgeBaseSchema(BaseModel):
    title: str
    content: str
    category: str
    source: str

class VectorIndexSchema(BaseModel):
    knowledge_id: int
    embedding_vector: List[float]
    model_used: str

# Knowledge Base Service
from sqlalchemy.orm import Session

def get_all_knowledge_entries(db: Session):
    return db.query(KnowledgeBase).all()

def add_knowledge_entry(db: Session, entry_data: KnowledgeBaseSchema):
    new_entry = KnowledgeBase(**entry_data.dict())
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return new_entry

def update_knowledge_entry(db: Session, entry_id: int, entry_data: KnowledgeBaseSchema):
    db_entry = db.query(KnowledgeBase).filter(KnowledgeBase.id == entry_id).first()
    if not db_entry:
        return None
    for key, value in entry_data.dict().items():
        setattr(db_entry, key, value)
    db.commit()
    return db_entry

def delete_knowledge_entry(db: Session, entry_id: int):
    db_entry = db.query(KnowledgeBase).filter(KnowledgeBase.id == entry_id).first()
    if not db_entry:
        return None
    db.delete(db_entry)
    db.commit()
    return db_entry

# Vector Search Service

def store_vector_embedding(db: Session, vector_data: VectorIndexSchema):
    new_vector = VectorIndex(**vector_data.dict())
    db.add(new_vector)
    db.commit()
    db.refresh(new_vector)
    return new_vector

def get_all_vector_entries(db: Session):
    return db.query(VectorIndex).all()

def delete_vector_entry(db: Session, vector_id: int):
    db_entry = db.query(VectorIndex).filter(VectorIndex.id == vector_id).first()
    if not db_entry:
        return None
    db.delete(db_entry)
    db.commit()
    return db_entry