from tmux_super_fingers.tmux_adapter import RealTmuxAdapter


"""To debug tmux integration, put a breakpoint()/print() in the production code and run this file."""


def find_pane_with_running_process():  # pragma: no cover
    tmux_adapter = RealTmuxAdapter()
    tmux_adapter.find_pane_with_running_process('nvim')
