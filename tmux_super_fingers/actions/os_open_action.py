from dataclasses import dataclass

from .action import Action
from ..targets.os_openable import OsOpenable
from ..tmux_adapter import RealTmuxAdapter, TmuxAdapter


@dataclass
class OsOpenAction(Action):
    target_payload: OsOpenable
    tmux_adapter: TmuxAdapter = RealTmuxAdapter()

    def perform(self) -> None:
        self.tmux_adapter.os_open(self.target_payload.file_or_url)
