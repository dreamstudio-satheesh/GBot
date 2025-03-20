import streamlit as st
import requests
import os

# Load API Base URL from Environment
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

# Streamlit App Title
st.set_page_config(page_title="AI Chatbot Admin Dashboard", layout="wide")

# User Authentication
st.sidebar.title("Admin Login")
username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")
login_button = st.sidebar.button("Login")

if login_button:
    auth_data = {"username": username, "password": password}
    try:
        response = requests.post(f"{API_BASE_URL}/auth/login", json=auth_data)
        response.raise_for_status()
        token = response.json().get("access_token")
        
        if token:
            st.sidebar.success(f"Welcome, {username}!")
            headers = {"Authorization": f"Bearer {token}"}
        else:
            st.sidebar.error("Invalid credentials")
            st.stop()
    except requests.exceptions.RequestException:
        st.sidebar.error("Login failed. Check your username/password.")
        st.stop()
else:
    st.sidebar.warning("Enter your credentials to access the dashboard")
    st.stop()

# Dashboard Layout
st.title("📊 AI Chatbot Admin Dashboard")

# Sections
menu = st.selectbox("Select a section:", ["Dashboard", "Knowledge Base", "Chatbot Settings", "Chat Logs", "API Keys", "Admin Panel"])

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

elif menu == "Admin Panel":
    st.subheader("👨‍💼 Admin Management")

    # Fetch and List Users
    st.subheader("🧑‍💻 User Management")
    try:
        users_response = requests.get(f"{API_BASE_URL}/admin/users", headers=headers)
        users_response.raise_for_status()
        users = users_response.json()
        
        for user in users:
            st.write(f"**Username:** {user['username']} | **Role:** {user['role']}")
            new_role = st.selectbox(f"Update Role for {user['username']}", ["admin", "user", "support"], index=["admin", "user", "support"].index(user["role"]))
            if st.button(f"Update {user['username']}"):
                update_response = requests.put(f"{API_BASE_URL}/admin/users/update/{user['id']}", json={"role": new_role}, headers=headers)
                if update_response.status_code == 200:
                    st.success(f"Updated {user['username']} to {new_role}")
                else:
                    st.error(f"Failed to update {user['username']}")

            if st.button(f"❌ Delete {user['username']}"):
                delete_response = requests.delete(f"{API_BASE_URL}/admin/users/delete/{user['id']}", headers=headers)
                if delete_response.status_code == 200:
                    st.success(f"Deleted {user['username']}")
                else:
                    st.error(f"Failed to delete {user['username']}")

    except requests.exceptions.RequestException:
        st.error("Failed to load users")

    # Fetch and List Tenants
    st.subheader("🏢 Tenant Management")
    try:
        tenants_response = requests.get(f"{API_BASE_URL}/admin/tenants", headers=headers)
        tenants_response.raise_for_status()
        tenants = tenants_response.json()

        for tenant in tenants:
            st.write(f"**Tenant:** {tenant['name']} | **Domain:** {tenant['domain']}")

        new_tenant_name = st.text_input("New Tenant Name")
        new_tenant_domain = st.text_input("New Tenant Domain")
        if st.button("Create Tenant"):
            create_tenant_response = requests.post(
                f"{API_BASE_URL}/admin/tenants/create", 
                json={"name": new_tenant_name, "domain": new_tenant_domain},
                headers=headers
            )
            if create_tenant_response.status_code == 200:
                st.success(f"Created tenant {new_tenant_name}")
            else:
                st.error("Failed to create tenant")

    except requests.exceptions.RequestException:
        st.error("Failed to load tenants")
