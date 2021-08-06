import os
import re
from .os_openable import OsOpenable
from .editor_openable import EditorOpenable
from ..actions.send_to_vim_in_tmux_pane_action import SendToVimInTmuxPaneAction
from ..actions.os_open_action import OsOpenAction


class TextFileTarget(OsOpenable, EditorOpenable):
    @property
    def file_or_url(self) -> str:
        return self.file_path

    def perform_primary_action(self) -> None:
        if re.search('^n?vim', os.environ['EDITOR']):
            SendToVimInTmuxPaneAction(self).perform()
        else:
            OsOpenAction(self).perform()
