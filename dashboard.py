import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# 1. Page Setting
st.set_page_config(page_title="Hospital Management System", layout="wide")
st.title("🏥 Hospital Patient Management System")

CSV_FILE = "hospital_patients.csv"

# 2. Data Load karne ka function
def load_data():
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    else:
        # Agar file nahi hai to sample data bana do
        data = {
            'Patient_ID': [101, 102, 103, 104, 105],
            'Name': ['Ali Khan', 'Sara Ahmed', 'Usman Malik', 'Fatima Noor', 'Ahmad Raza'],
            'Age': [25, 34, 45, 29, 52],
            'Disease': ['Fever', 'Diabetes', 'BP', 'Fever', 'Sugar'],
            'Days_Admitted': [3, 7, 5, 2, 10],
            'Bill_Amount': [5000, 15000, 12000, 4000, 25000]
        }
        df = pd.DataFrame(data)
        df.to_csv(CSV_FILE, index=False)
        return df

# 3. Data Save karne ka function
def save_data(dataframe):
    dataframe.to_csv(CSV_FILE, index=False)

# Session state me data save karo taake refresh par na uday
if 'df' not in st.session_state:
    st.session_state.df = load_data()

df = st.session_state.df

# --- SIDEBAR ---
st.sidebar.header("➕ Naya Patient Add Karein")

with st.sidebar.form(key="patient_form", clear_on_submit=True):
    new_name = st.text_input("Patient ka Naam")
    new_age = st.number_input("Age", min_value=1, max_value=120, step=1)
    new_disease = st.text_input("Bimari")
    new_days = st.number_input("Kitne Din Admit", min_value=0, step=1)
    new_bill = st.number_input("Bill Amount Rs", min_value=0.0, step=500.0)
    
    submit_button = st.form_submit_button(label="Patient Add Karein")

if submit_button:
    if new_name and new_disease:
        new_id = int(df["Patient_ID"].max()) + 1 if not df.empty else 101
        
        new_row = pd.DataFrame([{
            "Patient_ID": new_id,
            "Name": new_name,
            "Age": int(new_age),
            "Disease": new_disease,
            "Days_Admitted": int(new_days),
            "Bill_Amount": float(new_bill)
        }])
        
        df = pd.concat([df, new_row], ignore_index=True)
        save_data(df)
        st.session_state.df = df
        st.sidebar.success(f"✅ {new_name} ko add kar diya gaya!")
        st.rerun()
    else:
        st.sidebar.error("Naam aur Bimari likhna zaroori hai!")

st.sidebar.markdown("---")

# Search
st.sidebar.header("🔍 Patient Search")
search_query = st.sidebar.text_input("Naam likh kar search karein:")

if search_query:
    filtered_df = df[df["Name"].str.contains(search_query, case=False, na=False)]
else:
    filtered_df = df

# --- MAIN SCREEN ---
col1, col2 = st.columns([3, 2])

with col1:
    st.subheader("📋 Patient Records")
    st.metric("Total Patients", len(df))
    
    if not filtered_df.empty:
        st.dataframe(filtered_df, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        st.subheader("🗑️ Patient Delete Karein")
        delete_id = st.number_input("Delete karne ke liye Patient ID likhein:", min_value=0, step=1)
        if st.button("Delete Patient", type="primary"):
            if delete_id in df["Patient_ID"].values:
                df = df[df["Patient_ID"] != delete_id]
                save_data(df)
                st.session_state.df = df
                st.success(f"Patient ID {delete_id} delete ho gaya.")
                st.rerun()
            else:
                st.error("Ye Patient ID nahi mili.")
    else:
        st.info("Koi records nahi mile.")

with col2:
    st.subheader("📊 Analytics & Reports")
    if not df.empty:
        st.write("**Sab se Zyada Bimariyan**")
        fig, ax = plt.subplots(figsize=(5, 3))
        df["Disease"].value_counts().plot(kind="bar", ax=ax, color="#2E7D32")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        st.pyplot(fig)
        
        st.markdown("---")
        
        st.write("**Age vs Bill Amount Graph**")
        fig2, ax2 = plt.subplots(figsize=(5, 3))
        ax2.scatter(df["Age"], df["Bill_Amount"], color="#D32F2F", alpha=0.7) # Error theek hai
        ax2.set_xlabel("Age")
        ax2.set_ylabel("Bill Amount Rs")
        plt.tight_layout()
        st.pyplot(fig2)
        
        st.markdown("---")
        st.write("**Total Hospital Revenue**")
        st.metric("💰", f"Rs {df['Bill_Amount'].sum():,.0f}")
    else:
        st.info("Graph ke liye pehle data add karein.")

st.markdown("---")
st.caption("Made with ❤️ using Streamlit")