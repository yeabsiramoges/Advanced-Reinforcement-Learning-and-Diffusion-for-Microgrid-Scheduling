import numpy as np
import pandas as pd
import gymnasium as gym

from rldiff.state import State
from rldiff.action import Action
from random import randrange, seed
from datetime import datetime, timedelta
from rldiff.type_models import InfoDictionary
from rldiff.util import get_hour_resolution, preprocess
from rldiff.exception import InvalidRenderModeException
from typing import Any, Dict, List, Optional, Tuple, cast


class RyeEnv(gym.Env):
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

    _start_time_data: datetime
    _end_time_data: datetime
    _episode_end_time: datetime

    metadata: Dict[str, List[str]]

    def __init__(
        self,
        data: pd.DataFrame,
        episode_length: timedelta = timedelta(days=30),
        random_seed: Optional[int] = None,
        charge_loss_battery: float = 0.85,
        charge_loss_hydrogen: float = 0.325,
        grid_tarrif: float = 0.05,
        peak_grid_tarrif: float = 49.0,
    ) -> None:
        """Initializing the rye environment.

        Args:
            data
            episode_length
            random_seed
            charge_loss_battery
            charge_loss_hydrogen
            grid_tarrif
            peak_grid_tarrif
        """

        self.seed(random_seed)

        # Preprocess data
        data = preprocess(data)

        # Metadata for Gymnasium render-function
        self.metadata = {"render.modes": ["ansi"]}

        # Length of episode and resolutions
        self._episode_length = episode_length
        self._time_resolution = timedelta(hours=1)

        # Loss and reward function constants
        self._charge_loss_battery_storage = charge_loss_battery
        self._change_loss_hydrogen_storage = charge_loss_hydrogen

        self._grid_tariff = grid_tarrif
        self._peak_grid_tarrif = peak_grid_tarrif

        # Measured Data
        self._measured_consumption_data = data.consumption
        self._measured_wind_production_data = data.wind_production
        self._measured_photovoltaic_production_data = data.photovoltaic_production

        # Market Data
        self._spot_market_price_data = data.spot_market_price

        # Action Space: (Using constraints from Rye infra.)
        self._action_space_min = Action(charge_battery=-400, charge_hydrogen=-100)

        self._action_space_max = Action(charge_battery=400, charge_hydrogen=55)

        self.action_space = gym.spaces.Box(
            low=self._action_space_min.vector,
            high=self._action_space_max.vector,
            dtype=np.float64,
        )

        # State Space
        self._state_space_min = State(
            consumption=self._measured_consumption_data.min(),
            wind_production=self._measured_wind_production_data.min(),
            photovoltaic_production=self._measured_photovoltaic_production_data.min(),
            spot_market_price=self._spot_market_price_data.min(),
            battery_storage=0,
            hydrogen_storage=0,
            grid_import=0,
            grid_import_peak=0,
        )

        self._state_space_max = State(
            consumption=self._measured_consumption_data.max(),
            wind_production=self._measured_wind_production_data.max(),
            photovoltaic_production=self._measured_photovoltaic_production_data.max(),
            spot_market_price=self._spot_market_price_data.max(),
            battery_storage=500,
            hydrogen_storage=1670,
            grid_import=np.inf,
            grid_import_peak=np.inf,
        )

        # Observation / state space
        self.observation_space = gym.spaces.Box(
            low=self._state_space_min.vector,
            high=self._state_space_max.vector,
            dtype=np.float64,
        )

        # Start and end dates: format example -> 2020-01-01 13:00:00
        datetime_format = "%Y-%m-%d %H:%M:%S"
        self._start_time_data = datetime.strptime(data.time.min(), datetime_format)
        self._end_time_data = datetime.strptime(data.time.max(), datetime_format)

        self.reset()

    def get_possible_start_times(self) -> List[datetime]:
        """
        Returns a list of possible start times based on input data
        """
        return list(
            self._measured_photovoltaic_production_data.loc[
                : self._end_time_data - self._episode_length
            ].index
        )

    def get_state_vector(self) -> np.ndarray:
        """Returns state vector."""
        return self._state.vector

    def seed(self, random_seed: Optional[int] = None) -> None:
        """
        Setting random number generator seed for reproducibility.
        """
        if random_seed is not None:
            seed(random_seed)

    def reset(
        self,
        start_time: Optional[datetime] = None,
        battery_storage: float = 0.0,
        hydrogen_storage: float = 0.0,
        grid_import: float = 0.0,
    ) -> np.ndarray:
        """Resets environment to intial state.

        Args:
            start_time
            battery_storage
            hydrogen_storage
            grid_import

        Returns:
            state: initial state object
        """

        # Cumulative reward for episode
        self._cumulative_reward = 0

        # Setting time attributes
        if start_time is None:
            delta = (self._end_time_data - self._episode_length) - self._start_time_data
            random_seconds = randrange(delta.days * 24 * 30 * 30 + delta.seconds)
            random_hours = int(random_seconds / 3600)
            self._time = self._start_time_data + timedelta(hours=random_hours)
        else:
            self._time = get_hour_resolution(start_time)

        self._episode_end_time = self._time + self._episode_length

        # Initial State

        state = State(
            consumption=self._measured_consumption_data.loc[self._time],
            wind_production=self._measured_wind_production_data.loc[self._time],
            photovoltaic_production=self._measured_photovoltaic_production_data.loc[
                self._time
            ],
            spot_market_price=self._spot_market_price_data.loc[self._time],
            battery_storage=battery_storage,
            hydrogen_storage=hydrogen_storage,
            grid_import=grid_import,
            grid_import_peak=grid_import,
        )

        # Aligning initial state with state space
        state_vector = np.clip(
            state.vector,
            a_min=self.observation_space.low,
            a_max=self.observation_space.high,
        )

        self._state = State.from_vector(cast(np.ndarray, state_vector))

        return self._state.vector

    def _perform_action_on_env(
        self,
        action_array: np.ndarray,
        state_current: State,
    ) -> Tuple[State, Action]:
        """Calculate the new states by performing action on environment.

        Args:
            action
            state_current
        Returns:
            state_new: New state based on current state and action.
            action: Action actually performed in environment.
        """

        # Saturated action vector
        action = Action.from_vector(
            cast(
                np.ndarray,
                np.clip(
                    action_array,
                    a_min=self._action_space_min.vector,
                    a_max=self._action_space_max.vector,
                ),
            )
        )

        # Data for current timestep
        consumption_new = self._measured_consumption_data.loc[self._time]
        wind_production_new = self._measured_wind_production_data.loc[self._time]
        photovoltaic_production_new = self._measured_photovoltaic_production_data.loc[
            self._time
        ]
        spot_market_price = self._spot_market_price_data.loc[self._time]

        # Compute loss from electrical to chemical energy conversion
        if action.charge_battery > 0:
            charge_battery = self._charge_loss_battery_storage * action.charge_battery
        else:
            charge_battery = action.charge_battery

        if action.charge_battery > 0:
            charge_hydrogen = (
                self._change_loss_hydrogen_storage * action.charge_hydrogen
            )
        else:
            charge_hydrogen = action.charge_hydrogen

        # Energy storage constraints
        battery_storage_new = np.clip(
            state_current.battery_storage + charge_battery,
            a_min=self._state_space_min.battery_storage,
            a_max=self._state_space_max.battery_storage,
        )

        hydrogen_storage_new = np.clip(
            state_current.hydrogen_storage + charge_hydrogen,
            a_min=self._state_space_min.hydrogen_storage,
            a_max=self._state_space_max.hydrogen_storage,
        )

        # Lower bound for energy storage
        if action.charge_battery < 0:
            discharge_battery = float(
                battery_storage_new - state_current.battery_storage
            )
            action.charge_battery = max(discharge_battery, action.charge_battery)

        if action.charge_hydrogen < 0:
            discharge_hyrdogen = float(
                hydrogen_storage_new - state_current.hydrogen_storage
            )
            action.charge_hydrogen = max(discharge_hyrdogen, action.charge_hydrogen)

        # Compute power consumption in grid
        power_in_microgrid_new = (
            wind_production_new
            + photovoltaic_production_new
            - action.charge_hydrogen
            - action.charge_battery
        )

        # Compute additional power needed from grid if negative, as well as the peak
        # TODO: Add the option to compute in the case of exporting power to grid
        grid_import_new = np.clip(
            consumption_new - power_in_microgrid_new, a_min=0, a_max=None
        )

        grid_import_peak_new = max(state_current.grid_import_peak, grid_import_new)

        # Define new states
        states = State(
            consumption=consumption_new,
            wind_production=wind_production_new,
            photovoltaic_production=photovoltaic_production_new,
            hydrogen_storage=float(hydrogen_storage_new),
            battery_storage=float(battery_storage_new),
            grid_import=grid_import_new,
            spot_market_price=spot_market_price,
            grid_import_peak=grid_import_peak_new,
        )

        return states, action

    def _reward(self, state: State, done: bool) -> float:
        """Return reward of a given state.

        Args:
            state

        Returns:
            reward: reward of current state
        """

        power = (state.spot_market_price + self._grid_tariff) * state.grid_import
        peak = self._peak_grid_tarrif * state.grid_import_peak if done else 0

        return power + peak

    def step(
        self, action: np.ndarray
    ) -> Tuple[np.ndarray, float, bool, Dict[str, Any]]:
        """
        Run one-time step of the environment's dynamics.
        Environment resets when the end of the episode is reached.

        Args:
            action

        Returns:
            observation: agent observation of current environment state
            reward: amount of returned reward after taken action
            done: has the current episode ended or not
            info_dictionary: contains auxiliary state information
        """
        self._time += self._time_resolution

        new_state, new_action = self._perform_action_on_env(
            action_array=action, state_current=self._state
        )

        # Check if episode is finished
        done = self._time >= self._episode_end_time

        # Calculate reward
        reward = self._reward(new_state, done)
        self._cumulative_reward += reward

        # Update state variables
        self._state = new_state

        # Update info
        info = InfoDictionary(
            info={
                "state": new_state,
                "action": new_action,
                "time": self._time,
                "reward": reward,
                "cumulative_reward": self._cumulative_reward,
            }
        )

        if done:
            self.reset()

        return new_state.vector, reward, done, info

    def render(self, mode: str = "ansi") -> str:
        """Render environment

        Args:
            mode

        Returns:
            ansi: String contaning terminal-style text representation
        """

        match mode:
            case "ansi":
                return (
                    f"Step {self._time}/{self._episode_end_time}"
                    f"have state {self._state}"
                )
            case _:
                raise InvalidRenderModeException(f"Mode {mode} is not available.")
