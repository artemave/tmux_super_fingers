import os

from .action import Action
from ..targets.target_payload import EditorOpenable
from ..cli_adapter import RealCliAdapter, CliAdapter

# emacs go to line number:
#   send-keys -t %3 M-x goto-line Enter 3 Enter


class SendToVimInTmuxPaneAction(Action):
    def __init__(self, target_payload: EditorOpenable, cli_adapter: CliAdapter = RealCliAdapter()):
        self.target_payload = target_payload
        self.cli_adapter = cli_adapter

    def perform(self) -> None:
        editor_pane = self.cli_adapter.find_tmux_pane_with_running_process(os.environ['EDITOR'])

        if editor_pane:
            self.cli_adapter.select_tmux_window(editor_pane.pane_id)
            self.cli_adapter.tmux_send_keys(
                editor_pane.pane_id,
                f'Escape ":e {self._vim_e_args()}" Enter zz'
            )
            self.cli_adapter.select_tmux_pane(editor_pane.pane_id)
        else:
            self.cli_adapter.new_tmux_window(
                os.environ['EDITOR'],
                f" '{os.environ['EDITOR']} {self._vim_e_args()}; {os.environ['SHELL']} -i'"
            )

    def _vim_e_args(self) -> str:
        escaped_path = self.target_payload.file_path.replace('$', '\\$')

        if self.target_payload.line_number:
            return f'+{self.target_payload.line_number} {escaped_path}'

        return escaped_path
