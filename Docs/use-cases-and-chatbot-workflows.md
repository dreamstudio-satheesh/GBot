# **Use Cases & Chatbot Workflows**

## **1. User Roles & Capabilities**

### **1.1 SaaS Admin**
- **Manages platform-wide settings** (e.g., global chatbot configurations, subscription plans).
- **Oversees all SaaS users** and their chatbot instances.
- **Has full access** to the admin dashboard.
- **Manages billing & user accounts**.
- **Monitors platform analytics & chatbot usage reports**.
- **Manages AI model configurations** and updates.
- **Controls security policies and API rate limits**.

### **1.2 SaaS User (E-commerce Admin)**
- **Manages a single chatbot instance** for their e-commerce store.
- **Customizes chatbot responses** and uploads business-specific FAQs.
- **Integrates chatbot with their website** (via embeddable JavaScript SDK).
- **Manages API keys** for chatbot access.
- **Tracks chatbot performance** through analytics.
- **Handles customer interactions** and leads collected by the chatbot.
- **Tests chatbot responses** via a test chat interface.
- **Reviews past chat history** to identify incorrect or unhelpful responses.
- **Modifies chatbot answers** and stores them in the knowledge base.
- **Updates stored responses into RAG** to improve chatbot learning.
- **Flags uncertain responses** for manual correction.

---

## **2. Use Cases**

### **2.1 Customer Support Automation**
- Users ask questions about products, services, or policies.
- Chatbot retrieves answers from the knowledge base or AI model.
- If no answer is found, chatbot suggests contacting support.

### **2.2 Lead Generation & Sales Assistance**
- Chatbot collects user inquiries and asks qualifying questions.
- Based on responses, chatbot recommends products/services.
- Captures user contact details for follow-ups.

### **2.3 FAQ Handling**
- Users ask frequently asked questions (e.g., refund policy, shipping details).
- Chatbot searches the knowledge base and provides responses.
- AI model enhances answers when needed.

### **2.4 Appointment Scheduling**
- Users request to schedule meetings or demos.
- Chatbot integrates with a calendar API to check availability.
- Confirms and records the appointment.

### **2.5 User Authentication & API Access**
- Users access chatbot API via key-based authentication.
- Admins log in to the Streamlit dashboard with username/password.
- Role-based access ensures security.

---

## **3. Chatbot Workflows**

### **3.1 Standard Response Workflow**
1. User sends a query via chatbot.
2. Chatbot searches the knowledge base.
3. If found, chatbot responds with a stored answer.
4. If not found, chatbot uses AI model for response generation.
5. If the AI model is uncertain, chatbot suggests human support.

### **3.2 Sales & Lead Generation Workflow**
1. User interacts with chatbot for product recommendations.
2. Chatbot asks qualifying questions to understand user needs.
3. Based on responses, chatbot suggests products/services.
4. If needed, chatbot forwards the lead to human sales.

### **3.3 API Access Workflow**
1. User sends a request to the chatbot API.
2. API verifies the request using key-based authentication.
3. If valid, API processes the request and responds.
4. If invalid, API returns an authentication error.

### **3.4 Admin Dashboard Login Workflow**
1. Admin enters username and password in Streamlit dashboard.
2. System validates credentials against the Users table.
3. If valid, admin gains access.
4. If invalid, system denies login and logs the attempt.

### **3.5 Chatbot Learning & Knowledge Base Update Workflow**
1. SaaS User tests chatbot responses using a test chat interface.
2. Reviews past chat history for incorrect responses.
3. Modifies and updates chatbot responses in the knowledge base.
4. Stores improved responses in RAG for future retrieval.
5. Flags uncertain responses for manual correction.
6. Chatbot syncs updated knowledge for future queries.
7. AI model improves responses based on updated data.

---
