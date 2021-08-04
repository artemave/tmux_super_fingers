#!/usr/bin/env python3

import os
from curses import wrapper, window

from tmux_super_fingers.pane import get_current_window_panes
from tmux_super_fingers.ui import CursesUI
from tmux_super_fingers.panes_renderer import PanesRenderer


def main(stdscr: window) -> None:
    ui = CursesUI(stdscr)
    panes = get_current_window_panes()

    renderer = PanesRenderer(ui, panes)
    renderer.loop()


# Make escape delay unnoticable (it is very noticable by default)
os.environ.setdefault('ESCDELAY', '25')
wrapper(main)
