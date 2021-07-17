from .action import Action
import os
from ..utils import shell
from ..targets import TextFileTarget


class SendToVimInTmuxWindowAction(Action):
    target: TextFileTarget

    def perform(self) -> None:
        window_names = shell('tmux list-windows -F #{window_name}').split('\n')
        vim_window_names = list(filter(lambda x: x == 'vim' or x == 'nvim', window_names))

        vim_window_name = vim_window_names[0]

        if vim_window_name:
            os.system(f'tmux select-window -t {vim_window_name}')
            vim_pane_id = shell(
                'tmux list-panes -F "#{pane_id}" -t %s' % (vim_window_name)
            ).split('\n')[0]
            os.system(f'tmux send-keys -t {vim_pane_id} Escape')
            os.system(f'tmux send-keys -t {vim_pane_id} ":e {self._vim_e_args()}" Enter zz')
            return

        raise Exception('Could not find "vim" or "nvim" window in the current session')

    def _vim_e_args(self) -> str:
        if self.target.line_number:
            return f'+{self.target.line_number} {self.target.file_path}'

        return f'{self.target.file_path}'
