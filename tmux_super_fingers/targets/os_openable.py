from abc import ABCMeta, abstractmethod
from .target_payload import TargetPaylod


class OsOpenable(TargetPaylod, metaclass=ABCMeta):  # pragma: no cover
    """ Anything that can be sent to open/xdg-open. """

    @property
    @abstractmethod
    def file_or_url(self) -> str:
        ...
