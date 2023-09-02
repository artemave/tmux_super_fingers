#!/usr/bin/env python3

import os
from curses import wrapper, window

from tmux_super_fingers.current_window import CurrentWindow
from tmux_super_fingers.ui import CursesUI
from tmux_super_fingers.panes_renderer import PanesRenderer
from tmux_super_fingers.cli_adapter import RealCliAdapter
from tmux_super_fingers.finders import MarkFinder
from tmux_super_fingers import eval_file


def main(stdscr: window) -> None:
    if "FINGERS_EXTEND" in os.environ:
        eval_file(os.environ["FINGERS_EXTEND"])

    ui = CursesUI(stdscr)
    cli_adapter = RealCliAdapter()
    current_window = CurrentWindow(cli_adapter, MarkFinder())

    renderer = PanesRenderer(ui, current_window.panes)
    renderer.loop(cli_adapter)

# Make escape delay unnoticeable (it is very noticeable by default)
os.environ.setdefault('ESCDELAY', '25')
wrapper(main)
