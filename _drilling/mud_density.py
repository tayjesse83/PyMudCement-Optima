from dataclasses import dataclass


@dataclass
class Mud:
    density: float
    unit: str = "kg/m3"

    def _post_init_(self):
        if self.density <= 0:
            raise ValueError("Mud density must be greater than zero.")

        valid_units = {"kg/m3", "sg", "ppg"}
        if self.unit.lower() not in valid_units:
            raise ValueError(
                f"Unit '{self.unit}' not supported. Choose from {valid_units}")

    def density_kgm3(self) -> float:
        """Converts mud density to SI (kg/m^3)."""
        unit_lower = self.unit.lower()
        if unit_lower == "kg/m3":
            return self.density
        elif unit_lower == "sg":
            return self.density * 1000.0
        elif unit_lower == "ppg":
            return self.density * 119.826
        return self.density
