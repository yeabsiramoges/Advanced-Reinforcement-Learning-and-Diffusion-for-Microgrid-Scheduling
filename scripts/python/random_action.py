import ray
import logging

logger = logging.getLogger(__name__)

import numpy as np
import pandas as pd
import gymnasium as gym

from rldiff.env import RyeEnv
from os.path import abspath, dirname, join
from rldiff.plotter import RyeEnvironmentEpisodePlotter


class RandomActionAgent:
    def __init__(self, action_space: gym.spaces.Box):
        self._action_space = action_space

    def get_action(self, state: np.ndarray = None) -> np.ndarray:
        """Pull any action from action space"""
        return (
            self._action_space.sample()
            if state is not None
            else self._action_space.sample(state)
        )


def main() -> None:
    data = pd.read_csv(
        join(dirname(abspath(join(__file__, "../../"))), "data/rye/train.csv")
    )  # TODO: Convert to ray

    env = RyeEnv(data)
    agent = RandomActionAgent(action_space=env.action_space)
    plotter = RyeEnvironmentEpisodePlotter()

    info = None
    done = False

    while not done:
        action = agent.get_action()
        _, _, done, info = env.step(action)
        plotter.update(info)

    print(f"Cumulative Reward for Random Agent is: {info.info['cumulative_reward']}")
    plotter.plot_episode()


if __name__ == "__main__":
    main()
