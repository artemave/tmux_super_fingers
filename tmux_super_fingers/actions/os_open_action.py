from dataclasses import dataclass

from .action import Action
from ..targets.os_openable import OsOpenable
from ..tmux_adapter import RealTmuxAdapter, TmuxAdapter


@dataclass
class OsOpenAction(Action):
    target: OsOpenable
    tmux_adapter: TmuxAdapter = RealTmuxAdapter()

    def perform(self) -> None:
        self.tmux_adapter.os_open(self.target.file_or_url)
