from typing import List
from functools import cached_property

from .pane_props import PaneProps
from .pane import Pane
from .cli_adapter import CliAdapter
from .finders import MarkFinder


class CurrentWindow:
    """Current tmux window"""

    def __init__(self, cli_adapter: CliAdapter, mark_finder: MarkFinder):
        self.cli_adapter = cli_adapter
        self.mark_finder = mark_finder

    @cached_property
    def panes(self) -> List[Pane]:
        panes_props: List[PaneProps] = self.cli_adapter.current_tmux_window_panes_props()

        panes = list(map(self._create_pane_from_props, panes_props))

        _assign_hints(panes)

        return panes

    def _create_pane_from_props(self, pane_props: PaneProps) -> Pane:
        vertical_offset = 0
        if len(pane_props.scroll_position) > 0:
            vertical_offset = int(pane_props.scroll_position)

        pane_bottom = int(pane_props.pane_bottom)
        start = -vertical_offset
        end = pane_bottom - vertical_offset

        return Pane(
            unwrapped_text=self.cli_adapter.capture_tmux_viewport(
                pane_props.pane_id,
                start,
                end,
                unwrapped=True
            ),
            text=self.cli_adapter.capture_tmux_viewport(pane_props.pane_id, start, end),
            current_path=self.cli_adapter.get_tmux_pane_cwd(pane_props.pane_tty),
            left=int(pane_props.pane_left),
            right=int(pane_props.pane_right),
            top=int(pane_props.pane_top),
            bottom=pane_bottom,
            mark_finder=self.mark_finder,
        )


def _assign_hints(panes: List[Pane]) -> None:
    mark_number = 0
    for pane in reversed(panes):
        for mark in reversed(pane.marks):
            mark.hint = _number_to_hint(mark_number)
            mark_number += 1


def _number_to_hint(number: int) -> str:
    prefix = int(number / 26)
    letter_number = number % 26
    letter = chr(97 + letter_number)

    if prefix > 0:
        return f'{prefix}{letter}'

    return letter
