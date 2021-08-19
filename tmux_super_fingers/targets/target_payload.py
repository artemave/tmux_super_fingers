from dataclasses import dataclass
from abc import ABCMeta, abstractmethod
from typing import Optional


class TargetPaylod:
    """ Some payload that's passed from target to action """


@dataclass
class EditorOpenable(TargetPaylod):
    """ Anything that can be sent to vim """

    file_path: str
    line_number: Optional[int] = None


class OsOpenable(TargetPaylod, metaclass=ABCMeta):  # pragma: no cover
    """ Anything that can be sent to open/xdg-open. """

    @property
    @abstractmethod
    def file_or_url(self) -> str:
        ...
