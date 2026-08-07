import streamlit as st
from _drilling.mud_density import Mud
from _drilling.rheology import BinghamPlastic
from _drilling.hydraulics import HydraulicsCalculator
from _drilling.hole_cleaning import HoleCleaning
from _drilling.ecd import ECDCalculator


def show_page():
    st.title("💧 Drilling Fluids & Hydraulics Engine")
    st.write("---")

    tab1, tab2, tab3 = st.tabs(
        ["Hydrostatics & Safety", "Bingham-Plastic Rheology", "ECD & Hole Cleaning"])

    # TAB 1: HYDROSTATICS
    with tab1:
        st.subheader("Hydrostatic Pressure Balance")
        col1, col2 = st.columns(2)
        with col1:
            density = st.number_input(
                "Mud Density Input", value=10.5, step=0.1, key="d_input")
            unit = st.selectbox("Select Density Unit", [
                                "ppg", "SG", "kg/m3"], key="u_input")
        with col2:
            tvd = st.number_input(
                "True Vertical Depth, TVD (meters)", value=3000.0, step=100.0, key="tvd_input")
            formation_p = st.number_input(
                "Target Formation Pressure (Pascals)", value=32000000.0, step=500000.0, key="form_p_input")

        if st.button("Run Pressure Balance Analysis", type="primary"):
            try:
                mud = Mud(density, unit)
                density_kgm3 = mud.density_kgm3()

                hydrostatic = HydraulicsCalculator.hydrostatic_pressure(
                    density_kgm3, tvd)
                grad = HydraulicsCalculator.pressure_gradient(density_kgm3)
                min_density = HydraulicsCalculator.minimum_mud_density(
                    formation_p, tvd)

                st.write("#### Calculations Output")
                col_a, col_b = st.columns(2)
                col_a.metric("Equivalent Density (SI)",
                             f"{density_kgm3:.2f} kg/m³")
                col_b.metric("Pressure Gradient", f"{grad:.2f} Pa/m")

                st.metric("Computed Hydrostatic Pressure",
                          f"{hydrostatic / 1e6:.3f} MPa")
                st.metric("Minimum Safe Mud Density Required",
                          f"{min_density:.2f} kg/m³")

                if hydrostatic >= formation_p:
                    margin = (hydrostatic - formation_p) / 1e6
                    st.success(
                        f"✅ Safe! System is Overbalanced by {margin:.3f} MPa.")
                else:
                    deficit = (formation_p - hydrostatic) / 1e6
                    st.error(
                        f"❌ Warning! Underbalanced by {deficit:.3f} MPa. Risk of fluid influx (Kick).")
            except Exception as e:
                st.error(f"Error: {e}")

    # TAB 2: RHEOLOGY
    with tab2:
        st.subheader("Bingham-Plastic Non-Newtonian Flow Rheology Profile")
        col1, col2 = st.columns(2)
        with col1:
            pv = st.number_input("Plastic Viscosity, PV (cP)",
                                 min_value=1.0, value=15.0, step=1.0)
            yp = st.number_input("Yield Point, YP (lb/100ft²)",
                                 min_value=0.0, value=12.0, step=1.0)
        with col2:
            shear_rate = st.number_input(
                "Input Operating Shear Rate (s⁻¹)", value=511.0, step=10.0)

        if st.button("Calculate Flow Stress"):
            try:
                model = BinghamPlastic(pv, yp)
                stress = model.get_shear_stress(shear_rate)

                st.info(
                    f"Mathematical Model Model: τ = {yp:.1f} + ({pv:.3f} * 10⁻³) * γ")
                st.metric("Calculated Shear Stress (τ)", f"{stress:.3f} Pa")
            except Exception as e:
                st.error(f"Error: {e}")

    # TAB 3: ECD & HOLE CLEANING
    with tab3:
        st.subheader("Cuttings Cleanout & Dynamic ECD Controls")
        col1, col2 = st.columns(2)
        with col1:
            static_rho = st.number_input(
                "Static Mud Density (kg/m³)", value=1200.0, step=50.0)
            ann_p_loss = st.number_input(
                "Annular Frictional Pressure Loss (Pa)", value=1500000.0, step=100000.0)
            clean_tvd = st.number_input(
                "Hole Deepest Vertical Point (m)", value=3000.0, step=100.0)
        with col2:
            cutting_rho = st.number_input(
                "Drilled Cuttings Density (kg/m³)", value=2650.0, step=50.0)
            cutting_size = st.number_input(
                "Average Cutting Size (meters, e.g. 5mm = 0.005)", value=0.005, format="%.4f")

        if st.button("Evaluate ECD & Cuttings Transport"):
            try:
                ecd = ECDCalculator.calculate_ecd(
                    static_rho, ann_p_loss, clean_tvd)
                slip = HoleCleaning.slip_velocity_empirical(
                    static_rho, cutting_rho, cutting_size)

                st.write("#### Results")
                st.metric("Equivalent Circulating Density (ECD)",
                          f"{ecd:.2f} kg/m³")
                st.metric("Cuttings Static Settling/Slip Velocity",
                          f"{slip:.3f} m/s")

                if ecd > static_rho * 1.15:
                    st.warning(
                        "⚠️ High ECD detected! Monitor closely to prevent formation fracturing.")
            except Exception as e:
                st.error(f"Error: {e}")
