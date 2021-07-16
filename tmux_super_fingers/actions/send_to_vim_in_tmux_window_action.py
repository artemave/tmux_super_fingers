from .action import Action
import os
from ..utils import shell
from ..targets import TextFileTarget

class SendToVimInTmuxWindowAction(Action):
    target: TextFileTarget

    def perform(self) -> None:
        window_names = shell('tmux list-windows -F #{window_name}').split('\n')
        vim_window_names = list(filter(lambda x: x == 'vim' or x == 'nvim', window_names))

        if len(vim_window_names) > 0:
            os.system('tmux select-window -t %s' %(vim_window_names[0]))
            vim_pane_id = shell('tmux list-panes -F "#{pane_id}" -t %s' %(vim_window_names[0])).split('\n')[0]
            os.system('tmux send-keys -t %s Escape' %(vim_pane_id))

            if self.target.line_number:
                os.system('tmux send-keys -t %s ":e +%s %s" Enter zz' %(vim_pane_id, self.target.line_number, self.target.file_path))
            else:
                os.system('tmux send-keys -t %s ":e %s" Enter zz' %(vim_pane_id, self.target.file_path))

            return

        raise Exception('Could not find "vim" or "nvim" window in the current session')
