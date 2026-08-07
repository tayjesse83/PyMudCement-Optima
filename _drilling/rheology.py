class BinghamPlastic:
    def _init_(self, pv_cp: float, yp_lb_100ft2: float):
        """
        Bingham-Plastic rheology properties in field units:
        PV in centipoise (cP)
        YP in lb/100ft²
        """
        if pv_cp <= 0:
            raise ValueError(
                "Plastic Viscosity (PV) must be greater than zero.")
        if yp_lb_100ft2 < 0:
            raise ValueError("Yield Point (YP) cannot be negative.")

        self.pv = pv_cp
        self.yp = yp_lb_100ft2

    def get_shear_stress(self, shear_rate_s1: float) -> float:
        """
        Calculates shear stress (tau) in Pa for a given shear rate (s^-1).
        Converts field PV/YP to SI Units for calculation.
        """
        # Convert PV from cP to Pa.s (1 cP = 0.001 Pa.s)
        pv_pas = self.pv * 0.001

        # Convert YP from lb/100ft2 to Pa (1 lb/100ft2 = 0.478803 Pa)
        yp_pa = self.yp * 0.478803

        if shear_rate_s1 <= 0:
            return 0.0

        return yp_pa + (pv_pas * shear_rate_s1)
