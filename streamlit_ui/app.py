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
    headers = {"X-API-Key": api_key}  # Correct API Key header format
    try:
        response = requests.get(f"{API_BASE_URL}/auth/me", headers=headers)
        response.raise_for_status()  # Raise an error for failed requests
        user_data = response.json()
        st.sidebar.success(f"Welcome, {user_data.get('username', 'Admin')}!")
    except requests.exceptions.RequestException:
        st.sidebar.error("Invalid API Key or Connection Error")
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
    try:
        stats_response = requests.get(f"{API_BASE_URL}/system/stats", headers=headers)
        stats_response.raise_for_status()
        stats = stats_response.json()
        st.metric(label="Total API Keys", value=stats.get("total_api_keys", "N/A"))
        st.metric(label="CPU Usage (%)", value=stats.get("cpu_usage", "N/A"))
        st.metric(label="Memory Usage (%)", value=stats.get("memory_usage", "N/A"))
    except requests.exceptions.RequestException:
        st.error("Failed to load system stats")

elif menu == "Knowledge Base":
    st.subheader("📚 Manage Knowledge Base")
    try:
        knowledge_response = requests.get(f"{API_BASE_URL}/knowledge-base/entries", headers=headers)
        knowledge_response.raise_for_status()
        knowledge_entries = knowledge_response.json()
        for entry in knowledge_entries:
            st.write(f"**{entry['title']}**: {entry['content']}")
    except requests.exceptions.RequestException:
        st.error("Failed to load knowledge base")

elif menu == "Chatbot Settings":
    st.subheader("⚙️ Chatbot Settings")
    try:
        settings_response = requests.get(f"{API_BASE_URL}/chatbot/settings", headers=headers)
        settings_response.raise_for_status()
        settings = settings_response.json()
        for setting in settings:
            st.text_input(setting['setting_key'], setting['setting_value'])
    except requests.exceptions.RequestException:
        st.error("Failed to load chatbot settings")

elif menu == "Chat Logs":
    st.subheader("🗂 Chat Logs")
    try:
        logs_response = requests.get(f"{API_BASE_URL}/logs/conversations", headers=headers)
        logs_response.raise_for_status()
        logs = logs_response.json()
        for log in logs:
            st.write(f"**User:** {log['message']} → **Bot:** {log['response']}")
    except requests.exceptions.RequestException:
        st.error("Failed to load chat logs")

elif menu == "API Keys":
    st.subheader("🔑 API Key Management")
    try:
        api_keys_response = requests.get(f"{API_BASE_URL}/auth/api-key/list", headers=headers)
        api_keys_response.raise_for_status()
        api_keys = api_keys_response.json()
        for key in api_keys:
            st.write(f"**API Key:** {key['api_key']} (Status: {key['status']})")
    except requests.exceptions.RequestException:
        st.error("Failed to load API keys")
