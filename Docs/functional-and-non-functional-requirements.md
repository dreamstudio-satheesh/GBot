# **Functional & Non-Functional Requirements**

## **1. Functional Requirements**

### **Core Features**
1. **Chatbot Responses Based on AI**  
   - AI-driven responses using **Mistralai/mistral-small-3.1-24b-instruct** and **OpenAI/gpt-4o-mini**.
   - Context-aware response generation using **Retrieval-Augmented Generation (RAG)**.
   - Ability to fetch stored FAQs from the PostgreSQL knowledge base.
   
2. **User Authentication (API Key-Based & Username/Password for Admin Dashboard)**  
   - API access via **unique key-based authentication**.
   - Secure key management for users accessing chatbot API.
   - Admin dashboard authentication using **username/password stored in the Users table**.
   - Role-based access control for different user levels (Admin, Standard User, Guest).
   
3. **Web-Based Admin Dashboard**  
   - **Streamlit-based** interactive UI for managing chatbot settings.
   - Dashboard for monitoring chat logs, analytics, and response accuracy.
   - User-friendly interface for configuring chatbot workflows and FAQs.
   
4. **Knowledge Base Storage (PostgreSQL)**  
   - PostgreSQL database for storing chatbot knowledge and FAQs.
   - Indexed search for efficient retrieval of stored responses.
   - Ability to add, update, and delete knowledge base entries dynamically.
   
## **2. Non-Functional Requirements**

### **Performance & Scalability**
- Efficient AI response generation with minimal latency.
- Scalable architecture supporting multiple chatbot instances.
- Optimized database queries to ensure fast response times.

### **Security**
- Encrypted data storage (AES-256 for sensitive data).
- Secure API endpoints with **key-based authentication**.
- HTTPS/TLS encryption for all data in transit.

### **Usability & Reliability**
- Intuitive UI for admin dashboard with minimal learning curve.
- 99.9% uptime reliability for chatbot services.
- Automatic recovery from failures with backup and restore mechanisms.

### **Compliance & Maintenance**
- GDPR-compliant data handling (user data deletion upon request).
- Regular security audits and vulnerability patching.
- Logging and monitoring for error tracking and analytics.

---


