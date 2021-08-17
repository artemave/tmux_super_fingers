import pytest
from _pytest._code.code import ExceptionInfo

from .target_payload import TargetPaylod
from ..actions.action import Action
from ..test_utils import MockTarget


def teardown_function():
    if hasattr(MockTarget, 'primary_action'):
        delattr(MockTarget, 'primary_action')

    if hasattr(MockTarget, 'secondary_action'):
        delattr(MockTarget, 'secondary_action')


class Performed(Exception):
    def __init__(self, payload: TargetPaylod):
        self.payload = payload


class RaisingAction(Action):
    def perform(self) -> None:
        raise Performed(self.target_payload)


def test_custom_primary_action():
    MockTarget.primary_action = RaisingAction

    target = MockTarget()

    ex_info: ExceptionInfo[Performed]
    with pytest.raises(Performed) as ex_info:
        target.perform_primary_action()

    assert ex_info.value.payload == target.payload


def test_custom_secondary_action():
    MockTarget.secondary_action = RaisingAction

    target = MockTarget()

    ex_info: ExceptionInfo[Performed]
    with pytest.raises(Performed) as ex_info:
        target.perform_secondary_action()

    assert ex_info.value.payload == target.payload
