from dataclasses import dataclass
from abc import ABCMeta, abstractmethod
from ..targets.target_payload import TargetPaylod


@dataclass
class _ActionData:
    # TODO: force reimplementation
    target_payload: TargetPaylod


class Action(_ActionData, metaclass=ABCMeta):  # pragma: no cover
    @abstractmethod
    def perform(self) -> None:
        ...
