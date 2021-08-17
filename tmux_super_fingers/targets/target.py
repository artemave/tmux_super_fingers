from abc import ABCMeta, abstractmethod
from typing import Type

from ..actions.action import Action
from .target_payload import TargetPaylod


class Target(metaclass=ABCMeta):  # pragma: no cover
    primary_action: Type[Action]
    secondary_action: Type[Action]

    @abstractmethod
    def default_primary_action(self) -> Type[Action]:
        ...

    @abstractmethod
    def default_secondary_action(self) -> Type[Action]:
        ...

    @property
    @abstractmethod
    def payload(self) -> TargetPaylod:
        ...

    def perform_primary_action(self) -> None:
        action_class = getattr(self, 'primary_action', self.default_primary_action())
        action_class(self.payload).perform()

    def perform_secondary_action(self) -> None:
        action_class = getattr(self, 'secondary_action', self.default_secondary_action())
        action_class(self.payload).perform()
