class HoleCleaning:
    @staticmethod
    def slip_velocity_empirical(mud_density_kgm3: float, cutting_density_kgm3: float, cutting_size_m: float) -> float:
        """
        Estimates the settling/slip velocity (m/s) of cuttings in static mud
        using a simplified terminal settling velocity physics model.
        """
        if cutting_density_kgm3 <= mud_density_kgm3:
            return 0.0  # Cuttings float or stay suspended easily

        g = 9.81
        # Approximate drag coefficient for raw drill cuttings
        drag_coeff = 1.5

        density_diff = cutting_density_kgm3 - mud_density_kgm3
        numerator = 4 * g * cutting_size_m * density_diff
        denominator = 3 * drag_coeff * mud_density_kgm3

        return (numerator / denominator) ** 0.5

    @staticmethod
    def calculate_minimum_flow_rate(annular_velocity_ms: float, slip_velocity_ms: float, annular_area_m2: float) -> float:
        """Calculates minimum required mud flow rate (m^3/s) for effective cuttings transport."""
        net_transport_velocity = annular_velocity_ms - slip_velocity_ms
        if net_transport_velocity <= 0.2:
            # Recommend an annular velocity safety buffer of at least 0.2 m/s over settling velocity
            annular_velocity_ms = slip_velocity_ms + 0.3

        return annular_velocity_ms * annular_area_m2
