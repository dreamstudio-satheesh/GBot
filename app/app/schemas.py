from pydantic import BaseModel, EmailStr
from typing import List

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

# Knowledge Base Schemas
class KnowledgeBaseSchema(BaseModel):
    title: str
    content: str
    category: str
    source: str  # 'manual' or 'ai_generated'

class KnowledgeBaseResponse(KnowledgeBaseSchema):
    id: int

    class Config:
        from_attributes = True

# Vector Index Schemas
class VectorIndexSchema(BaseModel):
    knowledge_id: int
    embedding_vector: List[float]
    model_used: str

class VectorIndexResponse(VectorIndexSchema):
    id: int

    class Config:
        from_attributes = True
