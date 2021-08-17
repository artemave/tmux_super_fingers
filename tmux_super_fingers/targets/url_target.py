from typing import Type
from dataclasses import dataclass
from .target import Target
from .os_openable import OsOpenable
from tmux_super_fingers.actions.os_open_action import OsOpenAction
from ..actions.copy_to_clipboard_action import CopyToClipboardAction
from ..actions.action import Action

# @dataclass doesn't play well with @abstractmethod, hence workaraound.
# Copied from: https://github.com/python/mypy/issues/5374#issuecomment-650656381


class UrlTargetPayload(OsOpenable):
    def __init__(self, file_or_url: str):
        self._file_or_url = file_or_url

    @property
    def file_or_url(self) -> str:
        return self._file_or_url


@dataclass
class UrlTarget(Target):
    url: str

    @property
    def payload(self) -> UrlTargetPayload:
        return UrlTargetPayload(self.url)

    def default_primary_action(self) -> Type[Action]:
        return OsOpenAction

    def default_secondary_action(self) -> Type[Action]:
        return CopyToClipboardAction
