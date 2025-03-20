-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Tenants Table (Multi-Tenant Support)
CREATE TABLE tenants (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    domain VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Users Table (Multi-Tenant Aware)
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    tenant_id INT REFERENCES tenants(id) ON DELETE CASCADE,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role VARCHAR(20) CHECK (role IN ('admin', 'support', 'user')) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Knowledge Base (Tenant-Specific)
CREATE TABLE knowledge_base (
    id SERIAL PRIMARY KEY,
    tenant_id INT REFERENCES tenants(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    file_url TEXT,  -- Stores document location (Hetzner S3)
    category VARCHAR(100),
    source VARCHAR(50) CHECK (source IN ('manual', 'ai_generated')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Vector Index Table (For AI Retrieval)
CREATE TABLE vector_index (
    id SERIAL PRIMARY KEY,
    tenant_id INT REFERENCES tenants(id) ON DELETE CASCADE,
    knowledge_id INT REFERENCES knowledge_base(id) ON DELETE CASCADE,
    embedding_vector VECTOR(384), -- OpenAI Embedding Size
    model_used VARCHAR(100),
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Chatbot Settings (Tenant-Specific)
CREATE TABLE chatbot_settings (
    id SERIAL PRIMARY KEY,
    tenant_id INT REFERENCES tenants(id) ON DELETE CASCADE,
    setting_key VARCHAR(255) UNIQUE NOT NULL,
    setting_value TEXT NOT NULL
);

-- API Keys Table (For Secure Access)
CREATE TABLE api_keys (
    id SERIAL PRIMARY KEY,
    tenant_id INT REFERENCES tenants(id) ON DELETE CASCADE,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    api_key TEXT UNIQUE NOT NULL,
    status VARCHAR(20) CHECK (status IN ('active', 'revoked')) DEFAULT 'active',
    last_used TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP
);

-- Chat Logs Table (For Tracking Conversations)
CREATE TABLE chat_logs (
    id SERIAL PRIMARY KEY,
    tenant_id INT REFERENCES tenants(id) ON DELETE CASCADE,
    user_id INT REFERENCES users(id) ON DELETE SET NULL,
    message TEXT NOT NULL,
    response TEXT NOT NULL,
    source VARCHAR(50) CHECK (source IN ('knowledge_base', 'ai_model')) NOT NULL,
    user_feedback VARCHAR(10) CHECK (user_feedback IN ('positive', 'neutral', 'negative')),
    intent_detected VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);