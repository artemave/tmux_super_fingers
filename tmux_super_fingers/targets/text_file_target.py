import os
import re
from dataclasses import dataclass
from typing import Type, Optional
from .target_payload import OsOpenable
from .target_payload import EditorOpenable
from ..actions.action import Action
from ..actions.send_to_vim_in_tmux_pane_action import SendToVimInTmuxPaneAction
from ..actions.os_open_action import OsOpenAction
from ..actions.copy_to_clipboard_action import CopyToClipboardAction
from .target import Target


@dataclass
class TextFileTargetPayload(OsOpenable, EditorOpenable):
    @property
    def file_or_url(self) -> str:
        return self.file_path


@dataclass
class TextFileTarget(Target):
    file_path: str
    line_number: Optional[int] = None

    @property
    def payload(self) -> TextFileTargetPayload:
        return TextFileTargetPayload(
            file_path=self.file_path,
            line_number=self.line_number
        )

    # TODO: make @property
    def default_primary_action(self) -> Type[Action]:
        if re.search('^n?vim', os.environ['EDITOR']):
            return SendToVimInTmuxPaneAction
        else:
            return OsOpenAction

    def default_secondary_action(self) -> Type[Action]:
        return CopyToClipboardAction
