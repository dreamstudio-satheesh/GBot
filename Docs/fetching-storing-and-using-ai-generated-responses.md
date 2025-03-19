# **Fetching, Storing, and Using AI-Generated Responses**

## **1. Fetching AI-Generated Responses**

### **Process Flow:**
1. **Check the Knowledge Base (PostgreSQL)**
   - The chatbot first searches the PostgreSQL database for a predefined response.
   - If a **match is found**, the stored response is returned.
   - If no match is found, the query is sent to the AI model.

2. **Send Query to OpenRouter API**
   - If the knowledge base does not have an answer, the system forwards the query to **Mistralai/mistral-small-3.1-24b-instruct** via OpenRouter API.
   - The **retrieval-augmented generation (RAG) system** fetches relevant context from PostgreSQL before sending the query to the AI model.
   - The AI model generates a response based on both the query and retrieved knowledge.

3. **Return AI Response**
   - The AI-generated response is sent back to the chatbot and displayed to the user.

---

## **2. Storing AI-Generated Responses**

### **Logging AI Responses**
- Every chatbot interaction is logged in PostgreSQL with:
  - **Timestamp**
  - **User ID**
  - **Response Source** (Knowledge Base or AI Model)
  - **Confidence Score** (if applicable)

### **Manual Review & Knowledge Base Update**
- SaaS Users can **review past chat history** via the Streamlit dashboard.
- If an AI-generated response is useful, it can be **stored in the knowledge base** for future retrieval.
- This ensures that frequently asked questions get stored responses instead of making repeated AI calls.

### **Enhancing RAG System**
- Frequently used AI responses are **indexed and stored in RAG**.
- RAG improves response accuracy and speed by retrieving **previously generated responses** before sending queries to the AI model.

---

## **3. Using AI-Generated Responses in Real-Time**

### **Priority Order:**
1. **Check the PostgreSQL Knowledge Base**
   - If a matching response exists, return it immediately.
   
2. **Use RAG for Context Retrieval**
   - If a partial match is found, retrieve relevant past responses to improve context.
   
3. **Send Query to OpenRouter API (if necessary)**
   - If no stored response is available, send the query to the AI model.
   
4. **Allow SaaS Admins to Modify Responses**
   - Users can **update or correct AI-generated responses**, storing improved versions for future queries.

---

## **4. Optimization & Cost Control**

### **Reducing API Costs & Improving Efficiency**
- **Cache Frequent Queries:** Store AI responses for repeated user queries to avoid redundant API calls.
- **Hybrid Approach (Knowledge Base + RAG + AI):** Prioritize PostgreSQL responses, using AI only for new or uncommon queries.
- **Monitor API Usage:** Log API calls to track usage trends and set rate limits per SaaS user to control costs.

---

## **5. Summary of the Process**

| Step | Action |
|------|--------|
| **1. User sends a query** | Chatbot receives input. |
| **2. Check knowledge base** | If a matching response exists, return it. |
| **3. Use RAG if needed** | Retrieve similar past interactions to improve context. |
| **4. Query OpenRouter API (if needed)** | If no stored response, generate a new one via AI. |
| **5. Return AI response** | Display response to the user. |
| **6. Store interaction log** | Save query and response for future training. |
| **7. Admin review & update** | SaaS user can modify/store responses in the knowledge base. |

---


