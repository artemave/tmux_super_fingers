#!/usr/bin/env python3

import os
from curses import wrapper, window

from tmux_super_fingers.current_window import CurrentWindow
from tmux_super_fingers.ui import CursesUI
from tmux_super_fingers.panes_renderer import PanesRenderer
from tmux_super_fingers.tmux_adapter import RealTmuxAdapter


def main(stdscr: window) -> None:
    ui = CursesUI(stdscr)
    current_window = CurrentWindow(RealTmuxAdapter())

    renderer = PanesRenderer(ui, current_window.panes)
    renderer.loop()


# Make escape delay unnoticable (it is very noticable by default)
os.environ.setdefault('ESCDELAY', '25')
wrapper(main)
