from abc import ABCMeta, abstractmethod
from ..targets.target_payload import TargetPaylod


class Action(metaclass=ABCMeta):  # pragma: no cover
    def __init__(self, target_payload: TargetPaylod):
        self.target_payload = target_payload

    @abstractmethod
    def perform(self) -> None:
        ...
