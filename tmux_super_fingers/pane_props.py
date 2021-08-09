from dataclasses import dataclass


@dataclass
class PaneProps:
    pane_id: str
    pane_tty: str
    pane_left: str
    pane_right: str
    pane_top: str
    pane_bottom: str
    scroll_position: str
