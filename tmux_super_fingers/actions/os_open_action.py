from .action import Action
from ..targets.target_payload import OsOpenable
from ..cli_adapter import RealCliAdapter, CliAdapter


class OsOpenAction(Action):
    def __init__(self, target_payload: OsOpenable, cli_adapter: CliAdapter = RealCliAdapter()):
        self.target_payload = target_payload
        self.cli_adapter = cli_adapter

    def perform(self) -> None:
        self.cli_adapter.os_open(self.target_payload.file_or_url)
