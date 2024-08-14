import numpy as np

from pydantic import BaseModel
from dataclasses import dataclass


@dataclass
class Action(BaseModel):
    """Action vector.

    Args:
        charge_battery [kW/h]
        charge_hydrogen [kW/h]
    """

    charge_battery: float
    charge_hydrogen: float

    @property
    def vector(self) -> np.ndarray:
        return np.array([self.charge_battery, self.charge_hydrogen], dtype=np.float64)

    @classmethod
    def from_vector(cls, action: np.ndarray) -> "Action":
        return cls(charge_battery=action.item(0), charge_hydrogen=action.item(1))
