import numpy as np

from pydantic import BaseModel
from dataclasses import dataclass


@dataclass
class State(BaseModel):
    """State vector.

    Args:
        consumption [kWh/h]
        wind_production [kWh/h]
        photovoltaic_production [kWh/h]
        battery_storage [kWh]
        hydrogen_storage [kWh]
        grid_import [kWh/h]
        grid_import_peak [kWh/h]
        spot_market_proce [NOK/kWh]
    """

    consumption: float
    wind_production: float
    photovoltaic_production: float
    battery_storage: float
    hydrogen_storage: float
    grid_import: float
    grid_import_peak: float
    spot_market_proce: float

    @property
    def vector(self) -> np.ndarray:
        return np.array(
            [
                self.consumption,
                self.wind_production,
                self.photovoltaic_production,
                self.battery_storage,
                self.hydrogen_storage,
                self.grid_import,
                self.grid_import_peak,
                self.spot_market_proce,
            ],
            dtype=np.float64,
        )

    @classmethod
    def from_vector(cls, state: np.ndarray) -> "State":
        return cls(
            consumption=state.item(0),
            wind_production=state.item(1),
            photovoltaic_production=state.item(2),
            battery_storage=state.item(3),
            hydrogen_storage=state.item(4),
            grid_import=state.item(5),
            grid_import_peak=state.item(6),
            spot_market_proce=state.item(7),
        )
