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
    if "FINGERS_EXTEND" in os.environ and os.environ["FINGERS_EXTEND"] != "":
        eval_file(os.environ["FINGERS_EXTEND"])

    ui = CursesUI(stdscr)
    current_window = CurrentWindow(RealCliAdapter(), MarkFinder())

    renderer = PanesRenderer(ui, current_window.panes)
    renderer.loop()


# Make escape delay unnoticable (it is very noticable by default)
os.environ.setdefault('ESCDELAY', '25')
wrapper(main)
