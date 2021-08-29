from .os_open_action import OsOpenAction


class CopyToClipboardAction(OsOpenAction):
    def perform(self) -> None:
        self.cli_adapter.copy_to_clipboard(self.target_payload.file_or_url)
