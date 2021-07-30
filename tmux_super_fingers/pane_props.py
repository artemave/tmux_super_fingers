from __future__ import annotations  # https://stackoverflow.com/a/33533514/51209
from dataclasses import dataclass
from typing import List

from .utils import shell


@dataclass
class PaneProps:
    pane_id: str
    pane_tty: str
    pane_left: str
    pane_right: str
    pane_top: str
    pane_bottom: str
    scroll_position: str

    @classmethod
    def session_panes_props(cls) -> List[PaneProps]:
        return cls._get_panes_props('-s')

    @classmethod
    def current_window_panes_props(cls) -> List[PaneProps]:
        return cls._get_panes_props('-t !')

    @classmethod
    def _get_panes_props(cls, tmux_target: str) -> List[PaneProps]:
        props: List[str] = shell(
            'tmux list-panes ' + tmux_target + ' -F #{pane_id},#{pane_tty},#{pane_left},'
            '#{pane_right},#{pane_top},#{pane_bottom},#{scroll_position}'
        ).split('\n')

        panes_props = map(cls._create_pane_props, props)

        return list(panes_props)

    @classmethod
    def _create_pane_props(cls, props: str) -> PaneProps:
        pane_id, pane_tty, pane_left, pane_right, pane_top, pane_bottom, scroll_position = \
                props.split(',')

        return cls(
            pane_id=pane_id,
            pane_tty=pane_tty,
            pane_left=pane_left,
            pane_right=pane_right,
            pane_top=pane_top,
            pane_bottom=pane_bottom,
            scroll_position=scroll_position
        )
