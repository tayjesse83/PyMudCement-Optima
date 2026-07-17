
import streamlit as st
from ui import dashboard, drilling_page, cement_page

# Set page structure
st.set_page_config(
    page_title="PyMudCement-Optima",
    page_icon="💧",
    layout="wide"
)

# Sidebar Routing Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go To:",
    ["Main Dashboard", "Drilling Fluids & Hydraulics", "Cementing Module"]
)

# Page Router
if page == "Main Dashboard":
    dashboard.show_page()
elif page == "Drilling Fluids & Hydraulics":
    drilling_page.show_page()
elif page == "Cementing Module":
    cement_page.show_page()
