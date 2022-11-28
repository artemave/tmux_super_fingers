from tmux_super_fingers.cli_adapter import RealCliAdapter


"""To debug tmux integration, put a breakpoint()/print() in the production code and run this file."""


cli_adapter = RealCliAdapter()
cli_adapter.find_tmux_pane_with_running_process('nvim')
