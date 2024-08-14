import pandas as pd
import matplotlib.pyplot as plt

from datetime import datetime
from pydantic import BaseModel
from dataclasses import dataclass
from typing import Dict, List, cast

from rldiff.type_models import InfoDictionary


@dataclass
class RyeEnvironmentEpisodePlotter(BaseModel):
    """ """

    _actions: List[Dict[str, float]]
    _rewards: List[Dict[str, float]]
    _states: List[Dict[str, float]]
    _times: List[datetime]

    def __init__(self) -> None:
        self.reset()

    def update(self, info_dictionary: InfoDictionary) -> None:
        """
        Update state space variables.

        Args:
            info_dictionary: Info dictionary output from running env.step(action).
        """
        self._actions.append(info_dictionary.info["action"].__dict__)

        self._rewards.append(
            {
                "reward": cast(float, info_dictionary.info["reward"]),
                "cumulative_reward": cast(
                    float, info_dictionary.info["cumulative_reward"]
                ),
            }
        )

        self._states.append(info_dictionary.info["state"].__dict__)

        self._times.append(cast(datetime, info_dictionary.info["time"]))

    def plot_episode(self, show: bool = True) -> None:
        """
        Plot states, rewards, and actions from episode.

        Args:
            show: boolean for if the plot should be shown
        """
        _actions = pd.DataFrame(self._actions, index=self._times)
        _rewards = pd.DataFrame(self._rewards, index=self._times)
        _states = pd.DataFrame(self._states, index=self._times)

        _actions.plot(subplots=True, title="Actions")
        _rewards.plot(subplots=True, title="Rewards")
        _states.plot(subplots=True, title="Rewards")

        if show:
            plt.show()

        self.reset()

    def reset(self) -> None:
        """
        Reset list of states, actions, times, and rewards.
        """
        self._actions = []
        self._rewards = []
        self._states = []
        self._times = []
