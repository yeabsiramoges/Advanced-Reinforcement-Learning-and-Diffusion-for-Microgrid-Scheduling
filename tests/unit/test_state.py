from typing import Dict, Any
import pytest

from rldiff.state import State


@pytest.fixture
def context() -> Dict[str, Any]:
    return {
        "consumption": 11,
        "wind_production": 6,
        "photovoltaic_production": 6,
        "battery_storage": 500,
        "hydrogen_storage": 1670,
        "grid_import": 1000000,
        "grid_import_peak": 100000,
        "spot_market_price": 100000,
        "resulting_state": State(11, 6, 6, 500, 1670, 1000000, 100000, 100000),
    }


class TestState:
    """
    Class testing all state actions in model run.
    """

    def test_consumption(self, context: Dict[str, Any]) -> None:
        assert context["resulting_state"].consumption == context["consumption"]

    def test_wind_production(self, context: Dict[str, Any]) -> None:
        assert context["resulting_state"].wind_production == context["wind_production"]

    def test_pv_production(self, context: Dict[str, Any]) -> None:
        assert (
            context["resulting_state"].photovoltaic_production
            == context["photovoltaic_production"]
        )

    def test_battery_storage(self, context: Dict[str, Any]) -> None:
        assert context["resulting_state"].battery_storage == context["battery_storage"]

    def test_hydrogen_storage(self, context: Dict[str, Any]) -> None:
        assert (
            context["resulting_state"].hydrogen_storage == context["hydrogen_storage"]
        )

    def test_grid_import(self, context: Dict[str, Any]) -> None:
        assert context["resulting_state"].grid_import == context["grid_import"]

    def test_grid_import_peak(self, context: Dict[str, Any]) -> None:
        assert (
            context["resulting_state"].grid_import_peak == context["grid_import_peak"]
        )

    def test_spot_market_price(self, context: Dict[str, Any]) -> None:
        assert (
            context["resulting_state"].spot_market_price == context["spot_market_price"]
        )

    def test_state(self, context: Dict[str, any]) -> None:
        (
            State.from_vector(context["resulting_state"].vector).vector
            == context["resulting_state"].vector
        ).all()
