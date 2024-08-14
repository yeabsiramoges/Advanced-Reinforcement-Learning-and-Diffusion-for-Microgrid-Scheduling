import logging
import numpy as np
import pandas as pd
import gymnasium as gym

from .state import State
from .action import Action
from pydantic import BaseModel
from random import randrange, seed
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple, cast


class RyeEnv(gym.Env, BaseModel):
    """Simulator for microgrid dynamics in Rye Case Study.

    Attributes:
        _state
        _cumulative_reward
        _time
        _episode_length
        _time_resolution
        _charge_loss_battery_storage
        _change_loss_hydrogen_storage
        _grid_tariff
        _peak_grid_tarrif
        _action_space_min
        _action_space_max
        _state_space_min
        _state_space_max
        action_space
        observation_space
        _measured_consumption_data
        _measured_photovoltaic_production_data
        _measured_wind_production_data
        _spot_market_price_data
        _start_date_data
        _end_date_data
        _episode_end_time
        metadata
    """

    _state: State
    _cumulative_reward: float
    _time: datetime

    _episode_length: timedelta
    _time_resolution: timedelta
    _charge_loss_battery_storage: float
    _change_loss_hydrogen_storage: float
    _grid_tariff: float
    _peak_grid_tarrif: float

    _action_space_min: Action
    _action_space_max: Action
    _state_space_min: State
    _state_space_max: State

    action_space: gym.spaces.Box
    observation_space: gym.spaces.Box

    _measured_consumption_data: pd.DataFrame
    _measured_photovoltaic_production_data: pd.DataFrame
    _measured_wind_production_data: pd.DataFrame
    _spot_market_price_data: pd.DataFrame

    _start_date_data: datetime
    _end_date_data: datetime
    _episode_end_time: datetime

    metadata: Dict[str, List[str]]
