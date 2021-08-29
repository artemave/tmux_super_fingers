from abc import ABCMeta, abstractmethod
from typing import Type

from ..actions.action import Action
from .target_payload import TargetPaylod


# I would really like to be able to encode payload type in a Generic argument and then
# match that payload type with the Action Generic payload type argument.
# However, I wasn't able to express "action payload type is a subset of target payload type"
# constraint and so I had to bail out of the whole idea.
class Target(metaclass=ABCMeta):
    primary_action: Type[Action]
    secondary_action: Type[Action]

    @property
    @abstractmethod
    def default_primary_action(self) -> Type[Action]:  # pragma: no cover
        ...

    @property
    @abstractmethod
    def default_secondary_action(self) -> Type[Action]:  # pragma: no cover
        ...

    @property
    @abstractmethod
    def payload(self) -> TargetPaylod:  # pragma: no cover
        ...

    def perform_primary_action(self) -> None:
        action_class = getattr(self, 'primary_action', self.default_primary_action)
        action_class(self.payload).perform()

    def perform_secondary_action(self) -> None:
        action_class = getattr(self, 'secondary_action', self.default_secondary_action)
        action_class(self.payload).perform()
