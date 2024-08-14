from typing import Dict, Any
import pytest

from rldiff.action import Action


@pytest.fixture
def context() -> Dict[str, Any]:
    battery = 400
    hydrogen = 55

    return {
        "input_charge_battery": battery,
        "input_charge_hyrdogen": hydrogen,
        "resulting_action": Action(charge_battery=battery, charge_hydrogen=hydrogen),
    }


class TestAction:
    def test_battery_charge(self, context: Dict[str, Any]) -> None:
        assert context["resulting_action"].charge_battery == 400

    def test_hydrogen_charge(self, context: Dict[str, Any]) -> None:
        assert context["resulting_action"].charge_hydrogen == 55

    def test_action_vector(self, context: Dict[str, Any]) -> None:
        assert (
            Action.from_vector(context["resulting_action"].vector).vector
            == context["resulting_action"].vector
        ).all()
