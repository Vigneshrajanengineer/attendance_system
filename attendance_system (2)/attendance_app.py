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

st.title("Employee Attendance System")

with st.form("attendance_form"):
    name = st.text_input("Enter your Name")
    status = st.selectbox("Status", ["Present", "Absent"])
    login_time = st.time_input("Login Time", datetime.now().time())
    logout_time = st.time_input("Logout Time", datetime.now().time())
    date = datetime.now().date()

    submitted = st.form_submit_button("Submit")

    if submitted:
        if name.strip() == "":
            st.warning("Name cannot be empty.")
        else:
            new_entry = {
                "Name": name,
                "Date": date,
                "Status": status,
                "Login Time": login_time.strftime("%H:%M:%S"),
                "Logout Time": logout_time.strftime("%H:%M:%S")
            }
            save_data(new_entry)
            st.success("Attendance recorded successfully.")

if st.checkbox("Show Attendance Records"):
    df = load_data()
    st.dataframe(df)
