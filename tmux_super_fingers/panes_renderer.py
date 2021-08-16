from typing import List, Optional, Generator
from copy import deepcopy
from curses import ascii

from .pane import Pane
from .mark import Highlight, Mark
from .ui import UI
from .utils import flatten


class BreakTheLoop(Exception):
    pass


class PanesRenderer:
    """Renders panes with marks and handles user_input"""

    def __init__(self, ui: UI, panes: List[Pane]):
        self.ui = ui
        self.panes = panes
        self.secondary_mode = False

    def loop(self) -> None:
        user_input = ''

        while True:
            panes = _discard_marks_that_dont_match_user_input(deepcopy(self.panes), user_input)

            if user_input:
                chosen_mark = _the_only_mark_left(panes)

                if chosen_mark:
                    if self.secondary_mode:
                        chosen_mark.perform_secondary_action()
                    else:
                        chosen_mark.perform_primary_action()

                    break

            for pane in panes:
                self._render_pane_text(pane)
                self._overlay_marks(pane, user_input)

            try:
                user_input = self._handle_user_input(user_input)
            except BreakTheLoop:
                break

    def _handle_user_input(self, user_input: str) -> str:
        char = self.ui.getch()

        if char == ascii.ESC:
            raise BreakTheLoop

        # backspace (ascii.BS does not work for some reason)
        if char == 127:
            if user_input:
                user_input = user_input[:-1]
            else:
                raise BreakTheLoop
        elif char == ascii.SP:
            if self.secondary_mode:
                self.secondary_mode = False
            else:
                self.secondary_mode = True

            return user_input
        else:
            user_input += chr(char)

        return user_input

    def _render_top_border(self, pane: Pane) -> None:
        pane_width = pane.right - pane.left + 1
        self.ui.render_line(pane.top - 1, pane.left, '─' * pane_width, self.ui.DIM)

    def _render_left_border(self, pane: Pane) -> None:
        pane_height = pane.bottom - pane.top + 1
        for ln in range(pane_height):
            self.ui.render_line(pane.top + ln, pane.left - 1, '│', self.ui.DIM)

    def _render_pane_text(self, pane: Pane) -> None:
        if pane.top > 0:
            self._render_top_border(pane)

        if pane.left > 0:
            self._render_left_border(pane)

        lines = pane.text.split('\n')
        for ln, line in enumerate(lines):
            self.ui.render_line(pane.top + ln, pane.left, line, self.ui.DIM)

    def _overlay_marks(self, pane: Pane, user_input: str) -> None:
        for line_start, line_top, highlight in _get_highlights(pane):
            mark_left = pane.left + highlight.start - line_start
            self.ui.render_line(line_top, mark_left, highlight.text, self.ui.BOLD)

            if isinstance(highlight, Mark) and highlight.hint:
                hint_left = mark_left + len(user_input)
                hint = highlight.hint[len(user_input):]

                bg = self.ui.BLACK_ON_YELLOW if self.secondary_mode else self.ui.BLACK_ON_CYAN
                self.ui.render_line(line_top, hint_left, hint, bg | self.ui.BOLD)


def _get_highlights(pane: Pane) -> Generator[tuple[int, int, Highlight], None, None]:
    running_character_total = 0

    for ln, line in enumerate(pane.text.split('\n')):
        line_start = running_character_total
        running_character_total += len(line)
        line_end = running_character_total
        line_top = pane.top + ln

        marks_that_start_on_current_line: List[Highlight] = [
            m for m in pane.marks if line_end > m.start >= line_start
        ]

        for mark in marks_that_start_on_current_line:
            if mark.end > line_end:
                tail_length = mark.end - line_end
                tail_text = mark.text[-tail_length:]

                mark.text = mark.text[:-tail_length]
                yield (line_start, line_top, mark)

                wrapped_mark_tail = Highlight(text=tail_text, start=line_end)
                yield (line_end, line_top + 1, wrapped_mark_tail)
            else:
                yield (line_start, line_top, mark)


def _discard_marks_that_dont_match_user_input(panes: List[Pane], user_input: str) -> List[Pane]:
    for pane in panes:
        pane.marks = [
            m for m in pane.marks if m.hint and m.hint.startswith(user_input)
        ]

    return panes


def _the_only_mark_left(panes: List[Pane]) -> Optional[Mark]:
    marks_left = flatten([
        [m for m in p.marks] for p in panes
    ])

    if len(marks_left) == 1:
        return marks_left[0]
