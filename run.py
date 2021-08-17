#!/usr/bin/env python3

import sys
import os
from curses import wrapper, window

from tmux_super_fingers.current_window import CurrentWindow
from tmux_super_fingers.ui import CursesUI
from tmux_super_fingers.panes_renderer import PanesRenderer
from tmux_super_fingers.tmux_adapter import RealTmuxAdapter
from tmux_super_fingers.finders import MarkFinder
from tmux_super_fingers import eval_file


def main(stdscr: window) -> None:
    if len(sys.argv) > 1:
        eval_file(sys.argv[1])

    ui = CursesUI(stdscr)
    current_window = CurrentWindow(RealTmuxAdapter(), MarkFinder())

    renderer = PanesRenderer(ui, current_window.panes)
    renderer.loop()


# Make escape delay unnoticable (it is very noticable by default)
os.environ.setdefault('ESCDELAY', '25')
wrapper(main)
