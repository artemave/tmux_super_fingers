from abc import ABCMeta, abstractmethod


class Target(metaclass=ABCMeta):
    @abstractmethod
    def perform_primary_action(self) -> None:
        ...
