from .action import Action
from ..targets.target_payload import OsOpenable
from ..tmux_adapter import RealTmuxAdapter, TmuxAdapter


class OsOpenAction(Action):
    def __init__(self, target_payload: OsOpenable, tmux_adapter: TmuxAdapter = RealTmuxAdapter()):
        self.target_payload = target_payload
        self.tmux_adapter = tmux_adapter

    def perform(self) -> None:
        self.tmux_adapter.os_open(self.target_payload.file_or_url)
