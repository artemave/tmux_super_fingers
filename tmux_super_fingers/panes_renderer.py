from typing import List
from curses import ascii

from .pane import Pane
from .mark import Highlight, Mark
from .ui import UI
from .utils import flatten


class PanesRenderer:
    """Renders panes with marks and handles input"""

    def __init__(self, ui: UI, panes: List[Pane]):
        self.ui = ui
        self.panes = panes

    def loop(self) -> None:
        hint = ''

        while True:
            self._assign_hints(hint)

            marks_left = flatten([
                [m for m in p.marks if m.hint] for p in self.panes
            ])

            if len(marks_left) == 1:
                chosen_mark = marks_left[0]
                chosen_mark.perform_primary_action()
                break

            for pane in self.panes:
                self._render_pane_text(pane)
                self._overlay_marks(pane)

            self.ui.refresh()

            char = self.ui.getch()

            if char == ascii.ESC:
                break

            # backspace (ascii.BS does not work for some reason)
            if char == 127:
                if hint:
                    hint = hint[:-1]
                else:
                    break
            else:
                hint += chr(char)

    def _assign_hints(self, filter: str) -> None:
        mark_number = 0
        for pane in reversed(self.panes):
            for mark in reversed(pane.marks):
                hint = self._number_to_hint(mark_number)

                if hint.startswith(filter):
                    mark.hint = hint
                else:
                    mark.hint = None

                mark_number += 1

    def _number_to_hint(self, number: int) -> str:
        prefix = int(number / 26)
        letter_number = number % 26
        letter = chr(97 + letter_number)

        if prefix > 0:
            return f'{prefix}{letter}'

        return letter

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

    def _overlay_marks(self, pane: Pane) -> None:
        running_character_total = 0
        wrapped_mark_tail = None

        for ln, line in enumerate(pane.text.split('\n')):
            line_start = running_character_total
            running_character_total += len(line)
            line_end = running_character_total

            highlights_that_start_on_current_line: List[Highlight] = [
                m for m in pane.marks if line_end > m.start >= line_start
            ]

            if wrapped_mark_tail:
                highlights_that_start_on_current_line = [
                    wrapped_mark_tail] + highlights_that_start_on_current_line

            for highlight in highlights_that_start_on_current_line:
                mark_line_start = highlight.start - line_start
                text = highlight.text

                if highlight.end > line_end:
                    tail_length = highlight.end - line_end
                    wrapped_mark_tail = Highlight(
                        text=text[-tail_length:],
                        start=line_end,
                    )
                    text = text[:-tail_length]
                else:
                    wrapped_mark_tail = None

                self.ui.render_line(
                    pane.top + ln,
                    pane.left + mark_line_start,
                    text,
                    self.ui.BOLD
                )

                if isinstance(highlight, Mark):
                    mark = highlight
                    if mark.hint:
                        self.ui.render_line(
                            pane.top + ln,
                            pane.left + mark_line_start,
                            mark.hint,
                            self.ui.BLACK_ON_CYAN | self.ui.BOLD
                        )
