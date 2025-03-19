# **Basic System Architecture & Data Flow**

## **1. System Overview**
The SaaS-based AI chatbot system is designed to automate customer interactions for e-commerce and business websites. The architecture follows a **microservices-based** approach, leveraging **FastAPI, PostgreSQL, and AI-powered LLMs** for intelligent response generation.

---

## **2. High-Level System Components**
### **2.1 Backend (API & Business Logic Layer)**
- **FastAPI-based RESTful API**
- **Authentication & Authorization** (API Key-Based for API Access, Username/Password for Admin Dashboard)
- **PostgreSQL Knowledge Base** for FAQ storage and indexed retrieval
- **AI Model Integration**:
  - **Mistralai/mistral-small-3.1-24b-instruct** (High-performance small model)
  - **OpenAI/gpt-4o-mini** (Cost-efficient, balanced response generation)
- **Retrieval-Augmented Generation (RAG) Engine** for dynamic knowledge retrieval

### **2.2 Frontend (Admin Dashboard & Chatbot Widget)**
- **Admin Dashboard (Streamlit)** for chatbot management, logs, and analytics
- **Embeddable Chatbot Widget (JavaScript SDK)** for website integration
- **Real-time WebSocket Communication** for interactive chat sessions

### **2.3 Infrastructure & Deployment**
- **Dockerized Deployment** on Hetzner Cloud (VM)
- **PostgreSQL as Persistent Storage** (Dockerized local database)
- **Cloud Storage (Hetzner S3-Compatible) for Media & Logs**
- **Git Hooks for Manual CI/CD Pipeline**

---

## **3. Data Flow & System Interaction**
### **3.1 Chatbot Query Handling Workflow**
1. User interacts with the chatbot via the embedded widget.
2. The chatbot widget sends a request to the FastAPI backend.
3. The API verifies authentication (if required) and processes the request.
4. The system searches the PostgreSQL knowledge base for relevant responses.
5. If a response is found, it is returned to the user.
6. If no response is found, the AI model generates an answer using RAG.
7. The chatbot delivers the response to the user in real-time.
8. The user interaction is logged for future analysis and model improvements.

### **3.2 Admin Dashboard Interaction Workflow**
1. Admin logs into the **Streamlit dashboard** (Username/Password authentication).
2. Admin manages chatbot settings, responses, and API keys.
3. Admin reviews past chat logs and chatbot performance analytics.
4. Admin updates the knowledge base (FAQs, custom responses).
5. Updated knowledge is indexed and stored in PostgreSQL for improved future responses.

### **3.3 AI Model & RAG Integration Workflow**
1. The chatbot query is preprocessed and tokenized.
2. The RAG system retrieves contextually relevant data from the PostgreSQL knowledge base.
3. The retrieved data is combined with user input and sent to the AI model.
4. The AI model generates a response based on the combined context.
5. The response is returned to the chatbot for user delivery.

### **3.4 API Request Handling (Authentication & Data Retrieval)**
1. API requests are authenticated using API keys.
2. Role-based access control is applied for different user types (Admin, SaaS User, Guest).
3. API verifies and processes data retrieval or update requests.
4. Secure data handling and logging mechanisms ensure reliability.

---

## **4. Security Considerations**
- **Authentication & Authorization**: API Key-Based Authentication for API Access, Username/Password Authentication for Admin Dashboard
- **Data Encryption**: AES-256 for storage, TLS for transmission
- **Secure API Endpoints**: Rate limiting and API key validation
- **GDPR Compliance**: Data deletion on user request

---

## **5. System Scalability & Performance Optimization**
- **Optimized AI Inference** with caching for frequently asked queries
- **Database Indexing & Query Optimization** for faster retrieval
- **Asynchronous Processing** for non-blocking API requests
- **Load Balancing & Auto-Scaling** (Future consideration for growth)

---

## **6. Updated Features & Future Expansion**
- **Multi-Channel Expansion** (WhatsApp, Messenger, Email, SMS)
- **CRM and ERP Integrations**
- **Advanced AI-based Product Recommendations**
- **More Fine-Tuned AI Model Support for Specific Business Domains**

---

## **7. Conclusion**
This architecture ensures a **scalable, secure, and AI-powered chatbot** solution for SaaS users. The system leverages **LLMs, RAG, and PostgreSQL** to enhance response accuracy while maintaining **efficient performance and security**. Future enhancements will focus on **multi-channel expansion, AI model fine-tuning, and workflow automation**.

