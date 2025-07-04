# -*- coding: utf-8 -*-
"""TASK 3 HACKATHON

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1dIytw_k_rqyGWeH1qE8b-Pju1jaYSwGB
"""

import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("firebase-admin.json")  # Not the web config!
firebase_admin.initialize_app(cred)

from firebase_admin import auth, firestore

db = firestore.client()  # Initialize Firestore

def register_user(email: str, password: str, name: str, company_id: str = None):
    try:
        # 1. Create user in Firebase Authentication
        user = auth.create_user(
            email=email,
            password=password,
            display_name=name
        )

        # 2. Save additional user data to Firestore
        user_data = {
            "email": email,
            "name": name,
            "company_id": company_id  # Optional (links user to a company)
        }
        db.collection("users").document(user.uid).set(user_data)

        print(f"✅ User registered successfully! UID: {user.uid}")
        return user.uid
    except Exception as e:
        print(f"❌ Failed to register user: {e}")
        return None

def register_company(company_name: str, admin_email: str, industry: str):
    try:
        # Save company data to Firestore
        company_ref = db.collection("companies").document()
        company_data = {
            "name": company_name,
            "admin_email": admin_email,
            "industry": industry,
            "created_at": firestore.SERVER_TIMESTAMP  # Auto-adds timestamp
        }
        company_ref.set(company_data)

        print(f"✅ Company registered! ID: {company_ref.id}")
        return company_ref.id
    except Exception as e:
        print(f"❌ Failed to register company: {e}")
        return None

if __name__ == "__main__":
    # Test user registration
    user_id = register_user(
        email="test@example.com",
        password="SecurePass123!",
        name="Test User",
        company_id=None  # Optional
    )

    # Test company registration
    company_id = register_company(
        company_name="Tech Solutions Inc",
        admin_email="admin@techsolutions.com",
        industry="IT Services"
    )

def login_user(email: str, password: str):
    from firebase_admin import auth
    try:
        user = auth.get_user_by_email(email)
        print(f"✅ User {email} exists! UID: {user.uid}")
        return user.uid
    except auth.UserNotFoundError:
        print("❌ User not found")
    except Exception as e:
        print(f"❌ Login failed: {e}")

pip install streamlit streamlit-elements pillow

import streamlit as st
from streamlit_elements import elements, mui, html
from PIL import Image
import time

# Custom CSS for animations
st.markdown("""
<style>
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes pulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.05); }
    100% { transform: scale(1); }
}

.animated-card {
    animation: fadeIn 0.6s ease-out;
    border-radius: 15px !important;
    box-shadow: 0 10px 20px rgba(0,0,0,0.1) !important;
    transition: all 0.3s ease !important;
}

.animated-card:hover {
    transform: translateY(-5px) !important;
    box-shadow: 0 15px 30px rgba(0,0,0,0.2) !important;
}

.pulse-button {
    animation: pulse 2s infinite;
}
</style>
""", unsafe_allow_html=True)

# App Header with Animation
with elements("header"):
    mui.Box(
        mui.Typography("✨ SupportGenius AI", variant="h3", sx={
            "background": "linear-gradient(45deg, #6e48aa 30%, #9d50bb 90%)",
            "-webkit-background-clip": "text",
            "-webkit-text-fill-color": "transparent",
            "fontWeight": "bold",
            "textAlign": "center",
            "mb": 4,
            "animation": "fadeIn 1s ease-out"
        })
    )

# Animated Cards Layout
col1, col2 = st.columns(2)

with col1:
    with elements("register_card"):
        with mui.Card(className="animated-card", sx={"p": 3}):
            mui.Typography("New User?", variant="h5", gutterBottom=True)

            email = mui.TextField(label="Email", fullWidth=True, sx={"mb": 2})
            password = mui.TextField(label="Password", type="password", fullWidth=True)

            with mui.Button(
                variant="contained",
                color="primary",
                className="pulse-button",
                sx={"mt": 2, "py": 1.5},
                onClick=lambda: register_user(email.value, password.value, "New User")
            ):
                html.Div("Create Account", style={"fontWeight": "bold"})

with col2:
    with elements("login_card"):
        with mui.Card(className="animated-card", sx={"p": 3}):
            mui.Typography("Existing User?", variant="h5", gutterBottom=True)

            login_email = mui.TextField(label="Email", fullWidth=True, sx={"mb": 2})
            login_pass = mui.TextField(label="Password", type="password", fullWidth=True)

            with mui.Button(
                variant="outlined",
                color="secondary",
                sx={"mt": 2, "py": 1.5},
                onClick=lambda: login_user(login_email.value, login_pass.value)
            ):
                "Sign In"

# Animated Success Message
if st.session_state.get("success"):
    with elements("success_alert"):
        mui.Alert(
            "🎉 Registration successful!",
            severity="success",
            sx={"animation": "fadeIn 0.5s", "mt": 3}
        )
        time.sleep(3)
        del st.session_state["success"]

from streamlit.components.v1 import html

def loading_animation():
    html("""
    <div id="loader" style="display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(255,255,255,0.7);z-index:9999">
        <div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%)">
            <div class="spinner"></div>
        </div>
    </div>
    <style>
    .spinner {
        width: 40px;
        height: 40px;
        border: 4px solid #f3f3f3;
        border-top: 4px solid #6e48aa;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    </style>
    <script>
    function showLoader() {
        document.getElementById("loader").style.display = "block";
    }
    </script>
    """)

# Call this before auth operations
loading_animation()

# auth_operations.py
import firebase_admin
from firebase_admin import credentials, auth

def register_user(email, password, name):
    try:
        user = auth.create_user(email=email, password=password, display_name=name)
        st.session_state["success"] = True
        return True
    except Exception as e:
        st.error(f"Error: {e}")
        return False

def login_user(email, password):
    # Implement your login logic
    pass

# Commented out IPython magic to ensure Python compatibility.
# %%writefile app.py
# import streamlit as st
# import firebase_admin
# from firebase_admin import credentials, auth, firestore
# from datetime import datetime
# import numpy as np
# 
# # ===== 1. CUSTOM CURSOR TRAIL =====
# cursor_js = """
# <script>
# document.addEventListener('DOMContentLoaded', () => {
#     const cursor = document.createElement('div');
#     cursor.style.position = 'fixed';
#     cursor.style.width = '20px';
#     cursor.style.height = '20px';
#     cursor.style.borderRadius = '50%';
#     cursor.style.backgroundColor = 'rgba(110, 72, 170, 0.5)';
#     cursor.style.pointerEvents = 'none';
#     cursor.style.zIndex = '9999';
#     cursor.style.transform = 'translate(-50%, -50%)';
#     cursor.style.transition = 'transform 0.1s ease, opacity 0.5s ease';
#     document.body.appendChild(cursor);
# 
#     const particles = [];
#     document.addEventListener('mousemove', (e) => {
#         cursor.style.left = e.clientX + 'px';
#         cursor.style.top = e.clientY + 'px';
# 
#         // Create trailing particle
#         const particle = document.createElement('div');
#         particle.style.position = 'fixed';
#         particle.style.width = '8px';
#         particle.style.height = '8px';
#         particle.style.borderRadius = '50%';
#         particle.style.backgroundColor = 'rgba(110, 72, 170, 0.3)';
#         particle.style.left = e.clientX + 'px';
#         particle.style.top = e.clientY + 'px';
#         particle.style.zIndex = '9998';
#         document.body.appendChild(particle);
# 
#         // Animate and remove particle
#         setTimeout(() => {
#             particle.style.transform = 'scale(2)';
#             particle.style.opacity = '0';
#             setTimeout(() => particle.remove(), 500);
#         }, 50);
#     });
# });
# </script>
# """
# 
# # ===== 2. MODERN STYLING =====
# custom_css = """
# <style>
# /* Google Fonts */
# @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
# 
# /* Global Styles */
# html, body, [class*="css"] {
#     font-family: 'Poppins', sans-serif;
# }
# 
# /* Animated Gradient Header */
# @keyframes gradientBG {
#     0% {background-position: 0% 50%}
#     50% {background-position: 100% 50%}
#     100% {background-position: 0% 50%}
# }
# 
# .header {
#     background: linear-gradient(-45deg, #6e48aa, #9d50bb, #4776E6, #8E54E9);
#     background-size: 400% 400%;
#     animation: gradientBG 15s ease infinite;
#     color: white;
#     padding: 2rem;
#     border-radius: 15px;
#     margin-bottom: 2rem;
#     box-shadow: 0 4px 15px rgba(0,0,0,0.1);
# }
# 
# /* Floating Card Animation */
# @keyframes float {
#     0% {transform: translateY(0px)}
#     50% {transform: translateY(-10px)}
#     100% {transform: translateY(0px)}
# }
# 
# .card {
#     animation: float 4s ease-in-out infinite;
#     border-radius: 15px !important;
#     box-shadow: 0 10px 20px rgba(0,0,0,0.1) !important;
#     transition: all 0.3s ease !important;
#     padding: 1.5rem;
#     margin-bottom: 1.5rem;
# }
# 
# .card:hover {
#     transform: translateY(-5px) scale(1.02);
#     box-shadow: 0 15px 30px rgba(0,0,0,0.2) !important;
# }
# 
# /* Button Glow Effect */
# .stButton>button {
#     border: none;
#     background: linear-gradient(45deg, #6e48aa, #9d50bb);
#     color: white;
#     font-weight: 600;
#     transition: all 0.3s;
# }
# 
# .stButton>button:hover {
#     transform: translateY(-2px);
#     box-shadow: 0 5px 15px rgba(110, 72, 170, 0.4);
# }
# 
# /* Input Field Styling */
# .stTextInput>div>div>input {
#     border-radius: 10px !important;
#     padding: 10px !important;
# }
# </style>
# """
# 
# # ===== 3. FIREBASE INITIALIZATION =====
# if not firebase_admin._apps:
#     try:
#         cred = credentials.Certificate("firebase-admin.json")
#         firebase_admin.initialize_app(cred)
#         db = firestore.client()
#         firebase_status = "✅ Connected"
#     except Exception as e:
#         db = None
#         auth = None
#         firebase_status = f"❌ Error: {str(e)}"
# else:
#     db = firestore.client()
#     firebase_status = "✅ Already connected"
# 
# # ===== 4. STREAMLIT APP =====
# st.set_page_config(
#     page_title="SupportGenius AI",
#     page_icon="✨",
#     layout="wide"
# )
# 
# # Inject custom CSS and cursor JS
# st.markdown(custom_css, unsafe_allow_html=True)
# st.components.v1.html(cursor_js, height=0, width=0)
# 
# # Animated Header
# st.markdown("""
# <div class="header">
#     <h1 style="margin:0;font-weight:700;">✨ SupportGenius AI</h1>
#     <p style="margin:0;opacity:0.8;">Revolutionizing Customer Support</p>
# </div>
# """, unsafe_allow_html=True)
# 
# # Dashboard Layout
# col1, col2 = st.columns(2)
# 
# with col1:
#     st.markdown("""
#     <div class="card">
#         <h3 style="color:#6e48aa;">System Status</h3>
#         <p><b>Firebase:</b> {firebase_status}</p>
#         <p><b>Last refresh:</b> {timestamp}</p>
#     </div>
#     """.format(
#         firebase_status=firebase_status,
#         timestamp=datetime.now().strftime("%H:%M:%S")
#     ), unsafe_allow_html=True)
# 
# with col2:
#     st.markdown("""
#     <div class="card">
#         <h3 style="color:#6e48aa;">Quick Actions</h3>
#         <button onclick="window.location.reload()" style="
#             background: linear-gradient(45deg, #6e48aa, #9d50bb);
#             color: white;
#             border: none;
#             padding: 10px 20px;
#             border-radius: 8px;
#             cursor: pointer;
#             font-weight: 600;
#         ">Refresh App</button>
#     </div>
#     """, unsafe_allow_html=True)
# 
# # Firebase Features
# if db and auth:
#     tab1, tab2 = st.tabs(["👥 User Management", "🏢 Company Portal"])
# 
#     with tab1:
#         st.markdown("""
#         <div class="card">
#             <h3 style="color:#6e48aa;">Register New User</h3>
#         """, unsafe_allow_html=True)
# 
#         email = st.text_input("Email Address")
#         if st.button("Create User Account"):
#             try:
#                 user = auth.create_user(email=email)
#                 st.success(f"🎉 User {email} created successfully!")
#                 st.balloons()
#             except Exception as e:
#                 st.error(f"❌ Error: {str(e)}")
# 
#         st.markdown("</div>", unsafe_allow_html=True)
# 
#     with tab2:
#         st.markdown("""
#         <div class="card">
#             <h3 style="color:#6e48aa;">Register New Company</h3>
#         """, unsafe_allow_html=True)
# 
#         company_name = st.text_input("Company Name")
#         if st.button("Register Company"):
#             try:
#                 company_ref = db.collection("companies").document()
#                 company_ref.set({
#                     "name": company_name,
#                     "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#                 })
#                 st.success(f"🏢 Company {company_name} registered successfully!")
#             except Exception as e:
#                 st.error(f"❌ Error: {str(e)}")
# 
#         st.markdown("</div>", unsafe_allow_html=True)

from google.colab import files
files.upload()  # Select your Firebase service account file

!pkill -f streamlit
!streamlit run app.py --server.port=8501 --server.enableCORS=false &> /content/streamlit.log &

from google.colab.output import eval_js
print("Access your professional app at:", eval_js("google.colab.kernel.proxyPort(8501)"))

