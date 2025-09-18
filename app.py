import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import streamlit as st
from streamlit_lottie import st_lottie
import requests
import pandas as pd
import os

scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/drive"]
service_account_info = st.secrets["google_service_account"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(service_account_info, scope)
client = gspread.authorize(creds)
sheet = client.open("StudyMatchRegistrations").sheet1


st.set_page_config(
    page_title="Study Match",  # This is the title that appears on the browser tab
    page_icon="🎓",            # Optional: an emoji or icon
    layout="wide",         # Optional: 'wide' or 'centered'
)
# Function to load Lottie animation from URL
def load_lottie_url(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Initialize session state for page
if "page" not in st.session_state:
    st.session_state.page = "home"

# HOME PAGE
if st.session_state.page == "home":
    st.title("🎓 Welcome to Study Match")
    st.subheader("Find Your Perfect Study Partner!")

    # Load Lottie animation
    lottie_animation = load_lottie_url("https://assets5.lottiefiles.com/packages/lf20_tfb3estd.json")
    
    # Layout with columns
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        **Why join Study Match?**  
        - 🚀 Boost your learning efficiency  
        - 📚 Collaborate with like-minded peers  
        - 💡 Build meaningful academic & personal connections  
        - ⚡ Stay motivated and accountable  
        """)

        st.success("✅ Smart Matching Algorithm")
        st.info("💬 Connect with like-minded learners")
        st.warning("⚡ Enhance your study productivity")

    with col2:
        if lottie_animation:
            st_lottie(lottie_animation, height=300)
        else:
            st.image("study_image.png", caption="Collaborate & Learn", use_column_width=True)

    st.markdown("<h3 style='text-align:center; color:#1f77b4;'>Ready to start your study journey?</h3>", unsafe_allow_html=True)
    if st.button("Let's Go"):
    
        st.session_state.page="registration"
       
    


elif st.session_state.page=="registration":
    st.title("Register Yourself With Us")
    
    
    with st.form("registration form",clear_on_submit=True,enter_to_submit=True):
        col1,col2=st.columns(2)
        with col1:
            first_name=st.text_input("Enter your first name")
        with col2:
            last_name=st.text_input("Enter your last name")
    
        email=st.text_input("Enter your email",placeholder="you@example.com")
    
        profession= st.selectbox("Profession",["School Student","College Student","Job"])
        extra=st.text_input("Details",placeholder="Class/Course and year/Job designation")

        Gender=st.selectbox("Gender",["Male","Female"])    

        instagram=st.text_input("Instagram Username")
        age=st.number_input('Enter your age')
        goals=st.text_area("Goals in future")

        submit=st.form_submit_button("Submit")
        if submit:
            st.success(f"Thanks {first_name} We'll find you your match soon 💖")


            new_data={
                "First name":first_name,
                "Last name":last_name,
                "Email":email,
                "Profession":profession,
                "Detail":extra,
                "Gender":Gender,
                "Instagram":instagram,
                "Age":age,
                "Goals":goals

            }
                # Convert to list in correct order
            row = [new_data[col] for col in ["First name","Last name","Email","Profession","Detail",
                                            "Gender","Instagram","Age","Goals"]]
            try:
                sheet.append_row(row)
            except Exception as e:
                st.error(f"An error occurred while saving your data: {e}")
                st.session_state.page = "home"

            


    
