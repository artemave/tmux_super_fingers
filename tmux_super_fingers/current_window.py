from typing import List
from functools import cached_property

from .pane_props import PaneProps
from .pane import Pane
from .tmux_adapter import TmuxAdapter
from .utils import strip, shell


class CurrentWindow:
    """Current tmux window"""

    def __init__(self, tmux_adapter: TmuxAdapter):
        self.tmux_adapter = tmux_adapter

    @cached_property
    def panes(self) -> List[Pane]:
        panes_props: List[PaneProps] = self.tmux_adapter.current_window_panes_props()

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
            unwrapped_text=strip(
                shell(f'tmux capture-pane -p -S {start} -E {end} -J -t {pane_props.pane_id}')
            ),
            text=strip(shell(f'tmux capture-pane -p -S {start} -E {end} -t {pane_props.pane_id}')),
            current_path=_get_tmux_pane_cwd(pane_props.pane_tty),
            left=int(pane_props.pane_left),
            right=int(pane_props.pane_right),
            top=int(pane_props.pane_top),
            bottom=pane_bottom,
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


# TODO: move to TmuxAdapter
def _get_tmux_pane_cwd(pane_tty: str) -> str:
    pane_shell_pid = shell(f'ps -o pid= -t {pane_tty}').split("\n")[0].strip()
    return shell(f'lsof -a -p {pane_shell_pid} -d cwd -Fn').split('\n')[-1][1:]
