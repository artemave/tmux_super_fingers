from dataclasses import dataclass

from .action import Action
from ..targets.os_openable import OsOpenable
from ..tmux_adapter import RealTmuxAdapter, TmuxAdapter


@dataclass
class CopyToClipboardAction(Action):
    target: OsOpenable
    tmux_adapter: TmuxAdapter = RealTmuxAdapter()

    def perform(self) -> None:
        self.tmux_adapter.copy_to_clipboard(self.target.file_or_url)
