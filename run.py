#!/usr/bin/env python3

from curses import wrapper, window

from tmux_super_fingers.pane import get_current_window_panes
from tmux_super_fingers.ui import UI
from tmux_super_fingers.panes_renderer import PanesRenderer


def main(stdscr: window) -> None:
    ui = UI(stdscr)
    panes = get_current_window_panes()

    renderer = PanesRenderer(ui, panes)
    renderer.loop()


wrapper(main)
