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

-- Insert Dummy Tenants
INSERT INTO tenants (name, domain) VALUES 
    ('E-Commerce Store', 'store.example.com'),
    ('Tech Support', 'support.example.com'),
    ('Healthcare Chatbot', 'healthcare.example.com');

-- Insert Dummy Users
INSERT INTO users (tenant_id, first_name, last_name, username, email, password_hash, role) VALUES
    (1, 'Admin', 'Store', 'admin_store', 'admin@store.com', '$2b$12$y6tJ8Z6f8FbK4rGwQ9dIveJjDfpzCXYU2/Gp1pJH4dsmAld5T1fJS', 'admin'),
    (1, 'Support', 'Agent', 'support_store', 'support@store.com', '$2b$12$y6tJ8Z6f8FbK4rGwQ9dIveJjDfpzCXYU2/Gp1pJH4dsmAld5T1fJS', 'support'),
    (1, 'Customer', 'User', 'customer1', 'customer1@store.com', '$2b$12$y6tJ8Z6f8FbK4rGwQ9dIveJjDfpzCXYU2/Gp1pJH4dsmAld5T1fJS', 'user'),
    
    (2, 'Admin', 'Support', 'admin_support', 'admin@support.com', '$2b$12$y6tJ8Z6f8FbK4rGwQ9dIveJjDfpzCXYU2/Gp1pJH4dsmAld5T1fJS', 'admin'),
    (2, 'Support', 'Agent', 'agent_support', 'agent@support.com', '$2b$12$y6tJ8Z6f8FbK4rGwQ9dIveJjDfpzCXYU2/Gp1pJH4dsmAld5T1fJS', 'support'),
    
    (3, 'Admin', 'Health', 'admin_health', 'admin@health.com', '$2b$12$y6tJ8Z6f8FbK4rGwQ9dIveJjDfpzCXYU2/Gp1pJH4dsmAld5T1fJS', 'admin'),
    (3, 'Doctor', 'Smith', 'doctor_smith', 'smith@health.com', '$2b$12$y6tJ8Z6f8FbK4rGwQ9dIveJjDfpzCXYU2/Gp1pJH4dsmAld5T1fJS', 'support');

-- Insert Dummy Knowledge Base Entries
INSERT INTO knowledge_base (tenant_id, title, content, file_url, category, source) VALUES
    (1, 'Shipping Policy', 'Our standard shipping time is 3-5 business days.', NULL, 'Shipping', 'manual'),
    (1, 'Return Policy', 'You can return products within 30 days.', NULL, 'Returns', 'manual'),
    
    (2, 'Tech Support Hours', 'Our support team is available 24/7.', NULL, 'Support', 'manual'),
    (2, 'Common Troubleshooting', 'Try restarting your device.', NULL, 'Technical', 'manual'),
    
    (3, 'Health Guidelines', 'Drink 8 glasses of water daily.', NULL, 'Health', 'manual');

-- Insert Dummy Embeddings in Vector Index
INSERT INTO vector_index (tenant_id, knowledge_id, embedding_vector, model_used) VALUES
    (1, 1, ARRAY[0.1, 0.2, 0.3, ... 0.0]::vector(384), 'OpenAI'),
    (1, 2, ARRAY[0.2, 0.3, 0.4, ... 0.0]::vector(384), 'OpenAI'),
    (2, 3, ARRAY[0.4, 0.5, 0.6, ... 0.0]::vector(384), 'Mistral');


-- Insert Dummy Chatbot Settings
INSERT INTO chatbot_settings (tenant_id, setting_key, setting_value) VALUES
    (1, 'greeting_message', 'Welcome to our store! How can I assist you?'),
    (2, 'greeting_message', 'Hello! How can we help you today?'),
    (3, 'greeting_message', 'Welcome to the healthcare chatbot. How can I assist?');

-- Insert Dummy API Keys
INSERT INTO api_keys (tenant_id, user_id, api_key, status) VALUES
    (1, 1, 'api_key_store_123', 'active'),
    (2, 4, 'api_key_support_456', 'active'),
    (3, 6, 'api_key_health_789', 'active');

-- Insert Dummy Chat Logs
INSERT INTO chat_logs (tenant_id, user_id, message, response, source, user_feedback, intent_detected) VALUES
    (1, 3, 'What is your return policy?', 'You can return products within 30 days.', 'knowledge_base', 'positive', 'faq_return_policy'),
    (2, 5, 'How do I reset my password?', 'Try resetting from the settings page.', 'ai_model', 'neutral', 'support_request'),
    (3, 7, 'How many glasses of water should I drink?', 'Doctors recommend 8 glasses per day.', 'knowledge_base', 'positive', 'health_tips');
