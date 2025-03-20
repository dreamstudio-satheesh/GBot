import streamlit as st
import requests
import os

# Load API Base URL from Environment
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

# Streamlit App Title
st.set_page_config(page_title="AI Chatbot Admin Dashboard", layout="wide")

# User Authentication
st.sidebar.title("Admin Login")
api_key = st.sidebar.text_input("Enter API Key", type="password")
login_button = st.sidebar.button("Login")

if login_button and api_key:
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.get(f"{API_BASE_URL}/auth/me", headers=headers)
    if response.status_code == 200:
        st.sidebar.success("Login successful!")
        user_data = response.json()
    else:
        st.sidebar.error("Invalid API Key")
        st.stop()
else:
    st.sidebar.warning("Enter your API Key to access the dashboard")
    st.stop()

# Dashboard Layout
st.title("📊 AI Chatbot Admin Dashboard")

# Sections
menu = st.selectbox("Select a section:", ["Dashboard", "Knowledge Base", "Chatbot Settings", "Chat Logs", "API Keys"])

if menu == "Dashboard":
    st.subheader("📊 System Overview")
    stats_response = requests.get(f"{API_BASE_URL}/system/stats", headers=headers)
    if stats_response.status_code == 200:
        stats = stats_response.json()
        st.metric(label="Total API Keys", value=stats["total_api_keys"])
        st.metric(label="CPU Usage (%)", value=stats["cpu_usage"])
        st.metric(label="Memory Usage (%)", value=stats["memory_usage"])
    else:
        st.error("Failed to load system stats")

elif menu == "Knowledge Base":
    st.subheader("📚 Manage Knowledge Base")
    knowledge_response = requests.get(f"{API_BASE_URL}/knowledge-base/entries", headers=headers)
    if knowledge_response.status_code == 200:
        knowledge_entries = knowledge_response.json()
        for entry in knowledge_entries:
            st.write(f"**{entry['title']}**: {entry['content']}")
    else:
        st.error("Failed to load knowledge base")

elif menu == "Chatbot Settings":
    st.subheader("⚙️ Chatbot Settings")
    settings_response = requests.get(f"{API_BASE_URL}/chatbot/settings", headers=headers)
    if settings_response.status_code == 200:
        settings = settings_response.json()
        for setting in settings:
            st.text_input(setting['setting_key'], setting['setting_value'])
    else:
        st.error("Failed to load chatbot settings")

elif menu == "Chat Logs":
    st.subheader("🗂 Chat Logs")
    logs_response = requests.get(f"{API_BASE_URL}/logs/conversations", headers=headers)
    if logs_response.status_code == 200:
        logs = logs_response.json()
        for log in logs:
            st.write(f"**User:** {log['message']} → **Bot:** {log['response']}")
    else:
        st.error("Failed to load chat logs")

elif menu == "API Keys":
    st.subheader("🔑 API Key Management")
    api_keys_response = requests.get(f"{API_BASE_URL}/auth/api-key/list", headers=headers)
    if api_keys_response.status_code == 200:
        api_keys = api_keys_response.json()
        for key in api_keys:
            st.write(f"**API Key:** {key['api_key']} (Status: {key['status']})")
    else:
        st.error("Failed to load API keys")
