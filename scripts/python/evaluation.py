import numpy as np
import pandas as pd
import gymnasium as gym

from datetime import datetime
from os.path import abspath, dirname, join

from rldiff.env import RyeEnv
from rldiff.plotter import RyeEnvironmentEpisodePlotter
from rldiff.type_models import InfoDictionary
from scripts.python.random_action import RandomActionAgent


def main() -> None:
    data = pd.read_csv(
        join(dirname(abspath(join(__file__, "../../"))), "data/rye/test.csv")
    )  # TODO: Convert to ray

    env = RyeEnv(data)
    agent = RandomActionAgent(action_space=env.action_space)
    state = env.reset(start_time=datetime(2021, 2, 1, 0, 0))

    plotter = RyeEnvironmentEpisodePlotter()

    info = InfoDictionary(info={})
    done = False

    while not done:
        action = agent.get_action(state)

        state, reward, done, info = env.step(action)

        plotter.update(info)

    print(f"Cumulative reward on test data is: {info.info['cumulative_reward']}")

    plotter.plot_episode()


if __name__ == "__main__":
    main()
