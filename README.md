# 🧠 AI Chatbot - SaaS Based Solution

A **FastAPI-powered AI Chatbot** designed for **e-commerce, tech support, and healthcare industries**.  
This chatbot uses **PostgreSQL with pgvector**, **Retrieval-Augmented Generation (RAG)**, and **Mistral/OpenAI LLMs** for intelligent responses.

---

## 🚀 Features
✅ **Multi-Tenant Support** - Separate data per business  
✅ **AI-Powered Responses** - Uses OpenAI/Mistral models  
✅ **Retrieval-Augmented Generation (RAG)** - Improves knowledge retrieval  
✅ **Streamlit Admin Dashboard** - Manage chatbot settings  
✅ **Embeddable JavaScript Widget** - For website integration  
✅ **Secure API Access** - API key-based authentication  
✅ **Dockerized Deployment** - Runs seamlessly with Docker  

---

## 📂 Project Structure

```
/ai-chatbot
│── /app
│   ├── /api       # API Endpoints
│   ├── /models    # Database Models
│   ├── /services  # Business Logic
│   ├── /utils     # Utility Functions
│   ├── config.py  # Configuration Settings
│   ├── main.py    # FastAPI Entry Point
│── /db
│   ├── init.sql   # Database Schema & Dummy Data
│── /data          # Local Storage for Files
│── .gitignore     # Ignore unnecessary files
│── docker-compose.yml
│── Dockerfile
│── requirements.txt
│── .env
│── README.md
```

Thanks