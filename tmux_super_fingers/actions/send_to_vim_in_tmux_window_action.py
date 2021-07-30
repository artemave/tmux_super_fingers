import re
from functools import cached_property
from dataclasses import dataclass
from .action import Action
import os
from typing import List, Optional
from ..utils import shell
from ..targets import TextFileTarget

# emacs go to line number:
#   send-keys -t %3 M-x goto-line Enter 3 Enter


@dataclass
class PaneInfo:
    id: str
    tty: str


class SendToVimInTmuxPaneAction(Action):
    target: TextFileTarget

    def perform(self) -> None:
        vim_pane_id = self._find_vim_pane_id()

        if vim_pane_id:
            os.system(f'tmux select-window -t {vim_pane_id}')
            os.system(f'tmux send-keys -t {vim_pane_id} Escape')
            os.system(f'tmux send-keys -t {vim_pane_id} ":e {self._vim_e_args}" Enter zz')
        else:
            os.system(
                f'tmux new-window -n {self._vim_cmd}'
                f" '{self._vim_cmd} {self._vim_e_args}; {os.environ['SHELL']} -i'"
            )

    @cached_property
    def _vim_cmd(self) -> str:
        try:
            os.system('command -v nvim')
            return 'nvim'
        except Exception:
            return 'vim'

    @cached_property
    def _vim_e_args(self) -> str:
        if self.target.line_number:
            return f'+{self.target.line_number} {self.target.file_path}'

        return f'{self.target.file_path}'

    def _find_vim_pane_id(self) -> Optional[str]:
        tty_list = [pane_info.tty for pane_info in self._session_panes]

        tty_infos = shell(f"ps -o state= -o comm= -o tty= -t {','.join(tty_list)}").split('\n')

        vim_process_info = next(iter([
            info for info in tty_infos if re.search(r'^[^TXZ] +n?vim', info)
        ]), None)

        if vim_process_info:
            vim_pane_tty = re.split(' +', vim_process_info)[-1]
            return [
                pane_info.id for pane_info in self._session_panes if pane_info.tty == f'/dev/{vim_pane_tty}'
            ][0]

    # TODO: move into its own thing because it'll be needed elsewhere
    @cached_property
    def _session_panes(self) -> List[PaneInfo]:
        session_panes: List[str] = shell('tmux list-panes -s -F #{pane_id},#{pane_tty}').split('\n')
        return [PaneInfo(*pane_info.split(',')) for pane_info in session_panes]
