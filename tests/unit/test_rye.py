from typing import Tuple, Dict, Union
import numpy as np
import pytest
import pandas as pd

from datetime import datetime, timedelta

from rldiff.env import RyeEnv


@pytest.fixture
def context() -> Dict[str, Union[pd.DataFrame, RyeEnv]]:
    train = pd.read_csv("data/rye/train.csv", index_col=0, parse_dates=True)

    test = pd.DataFrame(
        data={
            "consumption": [1, 2, 1, 3],
            "photovoltaic_production": [1, 2, 3, 4],
            "wind_production": [1, 2, 3, 4],
            "spot_market_price": [1, 2, 3, 4],
        },
        index=pd.date_range("2020-1-1T12:00", periods=4, freq="h"),
    )
    return {
        "train_data": train,
        "test_data": test,
        "train_env": RyeEnv(train, timedelta(days=30)),
        "test_env": RyeEnv(test, timedelta(hours=2)),
    }


class TestRye:
    """
    Class testing gymnasium environment for the Rye Case Study
    """

    def test_episode_length(
        self, context: Dict[str, Union[pd.DataFrame, RyeEnv]]
    ) -> None:
        assert context["train_env"]._episode_length == timedelta(days=30)

    def test_time_delta(self, context: Dict[str, Union[pd.DataFrame, RyeEnv]]) -> None:
        assert (
            context["train_env"]._time + timedelta(days=30)
            == context["train_env"]._episode_end_time
        )

    def test_start_time(self, context: Dict[str, Union[pd.DataFrame, RyeEnv]]) -> None:
        assert context["train_env"]._start_time_data <= context["train_env"]._time

    def test_end_time(self, context: Dict[str, Union[pd.DataFrame, RyeEnv]]) -> None:
        assert context["train_env"]._time <= context["train_env"]._end_time_data

    def test_rye_specific_end_time(
        self, context: Dict[str, Union[pd.DataFrame, RyeEnv]]
    ) -> None:
        context["train_env"].reset(start_time=datetime(2020, 10, 1))

        assert (
            datetime(2020, 10, 31)
            == context["train_env"]._episode_length + context["train_env"]._time
        )

    def test_step(self, context: Dict[str, Union[pd.DataFrame, RyeEnv]]) -> None:
        context["train_env"].reset(start_time=datetime(2020, 10, 1))
        info = context["train_env"].step(action=np.array([1, 1]))[3]

        assert context["train_env"]._time == context[
            "train_env"
        ]._time_resolution + datetime(2020, 10, 1)

    def test_info(self, context: Dict[str, Union[pd.DataFrame, RyeEnv]]) -> None:
        context["train_env"].reset(start_time=datetime(2020, 10, 1))
        info = context["train_env"].step(action=np.array([1, 1]))[3]

        assert info.info["time"] == context["train_env"]._time

    def test_battery_charge_loss(
        self, context: Dict[str, Union[pd.DataFrame, RyeEnv]]
    ) -> None:
        assert context["train_env"]._charge_loss_battery_storage == 0.85

    def test_hydrogen_charge_loss(
        self, context: Dict[str, Union[pd.DataFrame, RyeEnv]]
    ) -> None:
        assert context["train_env"]._change_loss_hydrogen_storage == 0.325

    # TODO: Finish lol
