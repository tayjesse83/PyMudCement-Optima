import streamlit as st


def show_page():
    st.title("📊 PyMudCement-Optima Dashboard")
    st.subheader(
        "SPE Drilling & Cementing Engineering Integrated Software Suite")
    st.markdown(
        "Developed under course *PENG 258: Intelligent Mud & Cement Design Suite*")

    st.write("---")

    # Showcase some attractive high-level metrics
    st.write("### Active Project Status Overview")
    col1, col2, col3 = st.columns(3)
    col1.metric("Project Cohort", "BSc Petroleum Eng.")
    col2.metric("Target Well Status", "Active Design Phase")
    col3.metric("Backend Calculations", "Standard SPE Compliant")

    st.info(
        "👈 Use the left sidebar to navigate between *Drilling Fluids & Hydraulics Engine* "
        "and the *Cementing Engineering Module*."
    )

    st.markdown("""
    ### Project Overview
    PyMudCement-Optima automates critical calculations used on active drilling rigs to safely maintain well control and construct top-tier cement barriers. 
    
    ### Key Features
    - *Drilling Fluid Mechanics:* Multi-unit mud density handling, static hydrostatics checks, and non-Newtonian fluid rheology tracking.
    - *Primary Cementing:* Geometric annular volumetric calculations, displacement pump strokes tracking, and plug-bumping safety limits.
    """)
