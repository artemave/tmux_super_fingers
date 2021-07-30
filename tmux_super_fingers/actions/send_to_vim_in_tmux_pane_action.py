import re
from .action import Action
import os
from typing import Optional
from ..utils import shell
from ..targets import TextFileTarget
from ..pane_props import PaneProps

# emacs go to line number:
#   send-keys -t %3 M-x goto-line Enter 3 Enter


class SendToVimInTmuxPaneAction(Action):
    target: TextFileTarget

    def perform(self) -> None:
        vim_pane_id = self._find_editor_pane_id()

        if vim_pane_id:
            os.system(f'tmux select-window -t {vim_pane_id}')
            os.system(f'tmux send-keys -t {vim_pane_id} Escape')
            os.system(f'tmux send-keys -t {vim_pane_id} ":e {self._vim_e_args()}" Enter zz')
        else:
            os.system(
                f"tmux new-window -n {os.environ['EDITOR']}"
                f" '{os.environ['EDITOR']} {self._vim_e_args()}; {os.environ['SHELL']} -i'"
            )

    def _vim_e_args(self) -> str:
        if self.target.line_number:
            return f'+{self.target.line_number} {self.target.file_path}'

        return f'{self.target.file_path}'

    # TODO: this doesn't really belong here and can be reused as soon as we support
    # more terminal editors (e.g. emacs)
    def _find_editor_pane_id(self) -> Optional[str]:
        session_panes_props = PaneProps.session_panes_props()

        tty_list = [pane_props.pane_tty for pane_props in session_panes_props]

        tty_infos = shell(f"ps -o state= -o comm= -o tty= -t {','.join(tty_list)}").split('\n')

        vim_process_info = next(iter([
            info for info in tty_infos if re.search(r'^[^TXZ] +' + os.environ['EDITOR'], info)
        ]), None)

        if vim_process_info:
            vim_pane_tty = re.split(' +', vim_process_info)[-1]
            return [
                pane_props.pane_id for pane_props in session_panes_props
                if pane_props.pane_tty == f'/dev/{vim_pane_tty}'
            ][0]
