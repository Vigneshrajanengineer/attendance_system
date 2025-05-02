
# attendance_app_punch.py
import streamlit as st
import pandas as pd
from datetime import datetime
import os

EXCEL_FILE = "attendance.xlsx"

# Initialize Excel
if not os.path.exists(EXCEL_FILE):
    df_init = pd.DataFrame(columns=["Name", "Date", "Status", "Login Time", "Logout Time"])
    df_init.to_excel(EXCEL_FILE, index=False)

def load_data():
    return pd.read_excel(EXCEL_FILE)

def save_data(new_row):
    df = load_data()
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_excel(EXCEL_FILE, index=False)

# In-memory session state
if "login_time" not in st.session_state:
    st.session_state.login_time = None

if "logout_time" not in st.session_state:
    st.session_state.logout_time = None

st.title("Punch In/Out Attendance System")

name = st.text_input("Enter your Name")
status = st.selectbox("Status", ["Present", "Absent"])

if st.button("Punch In"):
    st.session_state.login_time = datetime.now().strftime("%H:%M:%S")
    st.success(f"Punched In at {st.session_state.login_time}")

if st.button("Punch Out"):
    st.session_state.logout_time = datetime.now().strftime("%H:%M:%S")
    st.success(f"Punched Out at {st.session_state.logout_time}")

if st.button("Submit Attendance"):
    if name.strip() == "":
        st.warning("Name cannot be empty.")
    elif not st.session_state.login_time or not st.session_state.logout_time:
        st.warning("Please Punch In and Out before submitting.")
    else:
        new_entry = {
            "Name": name,
            "Date": datetime.now().date(),
            "Status": status,
            "Login Time": st.session_state.login_time,
            "Logout Time": st.session_state.logout_time
        }
        save_data(new_entry)
        st.success("Attendance submitted.")
        st.session_state.login_time = None
        st.session_state.logout_time = None

if st.checkbox("Show Attendance Records"):
    df = load_data()
    st.dataframe(df)
