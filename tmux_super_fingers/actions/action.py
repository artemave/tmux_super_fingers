from dataclasses import dataclass
from abc import ABCMeta, abstractmethod
from ..targets.target import Target


@dataclass
class _ActionData:
    target: Target


class Action(_ActionData, metaclass=ABCMeta):  # pragma: no cover
    @abstractmethod
    def perform(self) -> None:
        ...
