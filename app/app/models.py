from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, func, Text, Float, ARRAY
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(Text, nullable=False)
    role = Column(String(20), nullable=False, default="user")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())

    api_keys = relationship("APIKey", back_populates="owner")

class APIKey(Base):
    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    api_key = Column(String(255), unique=True, nullable=False)
    status = Column(String(20), default="active")
    created_at = Column(DateTime, default=func.now())

    owner = relationship("User", back_populates="api_keys")

class Tenant(Base):
    __tablename__ = "tenants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)
    domain = Column(String(255), unique=True, nullable=False)
    created_at = Column(DateTime, default=func.now())
    
class KnowledgeBase(Base):
    __tablename__ = "knowledge_base"
    __table_args__ = {"extend_existing": True}  # Prevents duplicate definition errors

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id", ondelete="CASCADE"))
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    category = Column(String)
    source = Column(String, nullable=False)  # 'manual' or 'ai_generated'
    created_at = Column(DateTime, default=func.now())

class VectorIndex(Base):
    __tablename__ = "vector_index"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id", ondelete="CASCADE"))
    knowledge_id = Column(Integer, ForeignKey("knowledge_base.id", ondelete="CASCADE"))
    embedding_vector = Column(ARRAY(Float))  # Vector embedding storage
    model_used = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now())

class ChatbotSettings(Base):
    __tablename__ = "chatbot_settings"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id", ondelete="CASCADE"))
    setting_key = Column(String(255), unique=True, nullable=False)
    setting_value = Column(Text, nullable=False)

class ChatLogs(Base):
    __tablename__ = "chat_logs"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id", ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    message = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    source = Column(String(50), nullable=False)  # 'knowledge_base', 'vector_search', 'ai_model'
    user_feedback = Column(String(10))  # 'positive', 'neutral', 'negative'
    intent_detected = Column(String(255))
    created_at = Column(DateTime, default=func.now())