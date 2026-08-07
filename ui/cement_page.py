import math
import streamlit as st
import pandas as pd
import os
from cementing.annular_volume import AnnularVolume
from cementing.slurry_design import SlurryDesigner
from cementing.displacement import DisplacementCalculator
from cementing.pump_pressure import PumpPressureCalculator


def show_page():
    st.title("🏗️ Cementing Engineering Module")
    st.write("---")

    tab1, tab2, tab3 = st.tabs(
        ["Annular Volume & Slurry", "Casing Displacement", "Database Reference"])

    # TAB 1: VOLUME & DESIGN
    with tab1:
        st.subheader("Primary Slurry Volumetric Calculations")
        col1, col2 = st.columns(2)
        with col1:
            d_hole = st.number_input(
                "Hole Diameter (inches)", value=12.25, step=0.125)
            d_case = st.number_input(
                "Casing Outer Diameter (inches)", value=9.625, step=0.125)
            length = st.number_input(
                "Cemented Length (feet)", value=1500.0, step=100.0)
            washout = st.slider(
                "Wellbore Washout Excess Factor", 0.0, 1.0, 0.15, step=0.05)
        with col2:
            yield_sk = st.number_input(
                "Slurry Yield (cuft/sack)", value=1.15, step=0.05)
            water_req = st.number_input(
                "Water Requirement (gal/sack)", value=5.0, step=0.1)

        if st.button("Calculate Slurry Requirements", type="primary"):
            try:
                vol = AnnularVolume.calculate_volume(
                    d_hole, d_case, length, washout)
                design = SlurryDesigner.calculate_mix_water_and_sacks(
                    vol, yield_sk, water_req)

                st.write("#### Calculations Output")
                col_a, col_b = st.columns(2)
                col_a.metric("Total Slurry Volume Needed", f"{vol:.2f} ft³")
                col_b.metric("Equivalent Volume in Barrels",
                             f"{vol / 5.615:.2f} bbl")

                col_c, col_d = st.columns(2)
                col_c.metric("Cement Sacks Required",
                             f"{design['sacks_cement']} sacks")
                col_d.metric("Total Mix Water Required",
                             f"{design['water_gallons']:.1f} gal")
            except Exception as e:
                st.error(f"Error: {e}")

    # TAB 2: CASING DISPLACEMENT
    with tab2:
        st.subheader("Casing Displacement Fluids & Bumping Safeties")
        col1, col2 = st.columns(2)
        with col1:
            casing_id = st.number_input(
                "Casing Inner Diameter (inches)", value=8.835, step=0.05)
            disp_length = st.number_input(
                "Total Depth of Displacement Casing (feet)", value=4000.0, step=100.0)
            pump_output = st.number_input(
                "Pump Output Efficiency (bbl/stroke)", value=0.12, step=0.01)
        with col2:
            slurry_rho = st.number_input(
                "Slurry Density (ppg)", value=15.8, step=0.1)
            mud_rho = st.number_input(
                "Well Mud Density (ppg)", value=10.2, step=0.1)
            cement_height = st.number_input(
                "Height of Cement in Annulus (feet)", value=1500.0, step=100.0)

        if st.button("Calculate Displacement Dynamics"):
            try:
                capacity = DisplacementCalculator.internal_capacity_bbl(
                    casing_id, disp_length)
                strokes = DisplacementCalculator.displacement_strokes(
                    capacity, pump_output)
                diff = PumpPressureCalculator.hydrostatic_differential(
                    slurry_rho, mud_rho, cement_height)
                max_pump = PumpPressureCalculator.max_plug_bumping_pressure(
                    diff, 300.0)  # assuming 300 psi friction

                st.write("#### Results")
                col_x, col_y = st.columns(2)
                col_x.metric("Total Casing Capacity Volume",
                             f"{capacity:.2f} bbl")
                col_y.metric("Total Pump Strokes Required",
                             f"{math.ceil(strokes)} strokes")

                col_z, col_w = st.columns(2)
                col_z.metric("Hydrostatic U-tube Differential",
                             f"{diff:.1f} psi")
                col_w.metric("Max Recommended Bump Pressure",
                             f"{max_pump:.1f} psi")
            except Exception as e:
                st.error(f"Error: {e}")

    # TAB 3: DATABASE ACCESS
    with tab3:
        st.subheader("Automated lookup databases")

        # Safe loading path setup
        additives_path = "database/additives.csv"
        props_path = "database/cement_properties.csv"

        if os.path.exists(additives_path):
            st.write("#### 🧪 Cement Specialty Additives Library")
            df_add = pd.read_csv(additives_path)
            st.dataframe(df_add, use_container_width=True)

        if os.path.exists(props_path):
            st.write("#### 🧱 Base Slurry Reference Sheet")
            df_prop = pd.read_csv(props_path)
            st.dataframe(df_prop, use_container_width=True)
