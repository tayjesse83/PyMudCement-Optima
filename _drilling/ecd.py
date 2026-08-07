class ECDCalculator:
    @staticmethod
    def calculate_ecd(static_mud_density_kgm3: float, annular_pressure_loss_pa: float, tvd_m: float) -> float:
        """
        Calculates Equivalent Circulating Density (ECD) in kg/m^3.
        ECD = Static Density + (Annular Pressure Drop / (g * TVD))
        """
        if tvd_m <= 0:
            raise ValueError("TVD must be greater than zero.")

        g = 9.81
        dynamic_density_increase = annular_pressure_loss_pa / (g * tvd_m)
        return static_mud_density_kgm3 + dynamic_density_increase
