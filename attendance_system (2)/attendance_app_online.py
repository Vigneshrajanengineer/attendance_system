
# attendance_app_online.py
import streamlit as st
import pandas as pd
from datetime import datetime
import requests
from msal import ConfidentialClientApplication

st.title("Online Excel Attendance System")

# MS Graph credentials (you should store these securely)
client_id = st.secrets["client_id"]
client_secret = st.secrets["client_secret"]
tenant_id = st.secrets["tenant_id"]

authority = f"https://login.microsoftonline.com/{tenant_id}"
scopes = ["https://graph.microsoft.com/.default"]

# Auth function
def authenticate_graph():
    app = ConfidentialClientApplication(
        client_id=client_id,
        authority=authority,
        client_credential=client_secret
    )
    token = app.acquire_token_for_client(scopes)
    return token.get("access_token")

# Submit attendance to Excel online
def submit_attendance(name, status, login, logout):
    token = authenticate_graph()
    if not token:
        st.error("Could not authenticate with Microsoft Graph.")
        return

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    file_path = "/Apps/Attendance/attendance_online.xlsx"
    new_row = {
        "values": [[
            name,
            datetime.now().date().isoformat(),
            status,
            login.strftime("%H:%M:%S"),
            logout.strftime("%H:%M:%S")
        ]]
    }

    # Submit row
    res = requests.post(
        f"https://graph.microsoft.com/v1.0/me/drive/root:{file_path}:/workbook/tables/Table1/rows/add",
        headers=headers,
        json=new_row
    )

    if res.status_code == 201:
        st.success("Attendance recorded online successfully.")
    else:
        st.error("Failed to submit to Excel Online.")
        st.json(res.json())

# UI
with st.form("attendance_form"):
    name = st.text_input("Enter your Name")
    status = st.selectbox("Status", ["Present", "Absent"])
    login_time = st.time_input("Login Time", datetime.now().time())
    logout_time = st.time_input("Logout Time", datetime.now().time())
    submitted = st.form_submit_button("Submit")

    if submitted and name:
        submit_attendance(name, status, login_time, logout_time)
