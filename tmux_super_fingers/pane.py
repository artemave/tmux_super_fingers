from __future__ import annotations  # https://stackoverflow.com/a/33533514/51209
from dataclasses import dataclass
from typing import List, Dict, Optional

from .finders import find_marks
from .mark import Mark
from .utils import shell, strip
from .pane_props import PaneProps


def _unique_sorted_marks(marks: List[Mark]) -> List[Mark]:
    index: Dict[str, Mark] = {}
    for mark in marks:
        index[mark.text] = mark

    return sorted(index.values(), key=lambda m: m.start)


@dataclass
class Pane:
    unwrapped_text: str
    text: str
    current_path: str
    left: int
    right: int
    top: int
    bottom: int
    _marks: Optional[List[Mark]] = None

    @property
    def marks(self) -> List[Mark]:
        if self._marks is None:
            pane_marks: List[Mark] = []
            path_prefix = self.current_path
            unwrapped_text = self.unwrapped_text
            running_character_total = 0

            for line in unwrapped_text.split('\n'):
                marks = find_marks(line, path_prefix)
                for mark in marks:
                    mark.start += running_character_total

                running_character_total += len(line)
                pane_marks += marks

            # Concurrent map is actually _slower_ than a regular map.
            #
            # with futures.ThreadPoolExecutor() as executor:
            #     marks = compact(executor.map(lambda m: find_match(m, text, path_prefix), matches))

            self._marks = _unique_sorted_marks(pane_marks)

        return self._marks

    @marks.setter
    def marks(self, marks: List[Mark]) -> None:
        self._marks = marks


def get_current_window_panes() -> List[Pane]:
    panes_props: List[PaneProps] = PaneProps.current_window_panes_props()

    panes = list(map(_create_pane_from_props, panes_props))

    _assign_hints(panes)

    return panes


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


def _create_pane_from_props(pane_props: PaneProps) -> Pane:
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


def _get_tmux_pane_cwd(pane_tty: str) -> str:
    pane_shell_pid = shell(f'ps -o pid= -t {pane_tty}').split("\n")[0].strip()
    return shell(f'lsof -a -p {pane_shell_pid} -d cwd -Fn').split('\n')[-1][1:]
