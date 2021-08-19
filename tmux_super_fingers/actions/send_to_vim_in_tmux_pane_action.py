import os

from .action import Action
from ..targets.target_payload import EditorOpenable
from ..tmux_adapter import RealTmuxAdapter, TmuxAdapter

# emacs go to line number:
#   send-keys -t %3 M-x goto-line Enter 3 Enter


class SendToVimInTmuxPaneAction(Action):
    def __init__(self, target_payload: EditorOpenable, tmux_adapter: TmuxAdapter = RealTmuxAdapter()):
        self.target_payload = target_payload
        self.tmux_adapter = tmux_adapter

    def perform(self) -> None:
        editor_pane = self.tmux_adapter.find_pane_with_running_process(os.environ['EDITOR'])

        if editor_pane:
            self.tmux_adapter.select_window(editor_pane.pane_id)
            self.tmux_adapter.send_keys(editor_pane.pane_id, f'Escape ":e {self._vim_e_args()}" Enter zz')
        else:
            self.tmux_adapter.new_window(
                os.environ['EDITOR'],
                f" '{os.environ['EDITOR']} {self._vim_e_args()}; {os.environ['SHELL']} -i'"
            )

    def _vim_e_args(self) -> str:
        if self.target_payload.line_number:
            return f'+{self.target_payload.line_number} {self.target_payload.file_path}'

        return f'{self.target_payload.file_path}'
