class HydraulicsCalculator:
    GRAVITY = 9.81  # m/s^2

    @staticmethod
    def hydrostatic_pressure(mud_density_kgm3: float, tvd_m: float) -> float:
        """Calculates hydrostatic pressure (Pa) = rho * g * h"""
        if tvd_m <= 0:
            raise ValueError("TVD must be greater than zero.")
        return mud_density_kgm3 * HydraulicsCalculator.GRAVITY * tvd_m

    @staticmethod
    def pressure_gradient(mud_density_kgm3: float) -> float:
        """Calculates pressure gradient (Pa/m) = rho * g"""
        return mud_density_kgm3 * HydraulicsCalculator.GRAVITY

    @staticmethod
    def minimum_mud_density(formation_pressure_pa: float, tvd_m: float) -> float:
        """Calculates minimum mud density (kg/m^3) required to balance pore pressure."""
        if tvd_m <= 0:
            raise ValueError("TVD must be greater than zero.")
        return formation_pressure_pa / (HydraulicsCalculator.GRAVITY * tvd_m)
