import os
import re
from .os_openable import OsOpenable
from .editor_openable import EditorOpenable
from ..actions import send_to_vim_in_tmux_pane_action
from ..actions import os_open_action


class TextFileTarget(OsOpenable, EditorOpenable):
    @property
    def file_or_url(self) -> str:
        return self.file_path

    def perform_primary_action(self) -> None:
        if re.search('^n?vim', os.environ['EDITOR']):
            send_to_vim_in_tmux_pane_action.SendToVimInTmuxPaneAction(self).perform()
        else:
            os_open_action.OsOpenAction(self).perform()
