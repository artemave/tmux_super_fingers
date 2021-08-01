#!/usr/bin/env python3

from curses import ascii, wrapper, window
from typing import List

from tmux_super_fingers.mark import Highlight, Mark
from tmux_super_fingers.pane import Pane
from tmux_super_fingers.utils import flatten
from tmux_super_fingers.ui import UI


def render_pane_text(ui: UI, pane: Pane) -> None:
    if pane.top > 0:
        pane_width = pane.right - pane.left + 1
        ui.render_line(pane.top - 1, pane.left, '─' * pane_width, ui.DIM)

    if pane.left > 0:
        pane_height = pane.bottom - pane.top + 1
        for ln in range(pane_height):
            ui.render_line(pane.top + ln, pane.left - 1, '│', ui.DIM)

    lines = pane.text.split('\n')
    for ln, line in enumerate(lines):
        ui.render_line(pane.top + ln, pane.left, line, ui.DIM)


def overlay_marks(ui: UI, pane: Pane) -> None:
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

            ui.render_line(
                pane.top + ln,
                pane.left + mark_line_start,
                text,
                ui.BOLD
            )

            if isinstance(highlight, Mark):
                mark = highlight
                if mark.hint:
                    ui.render_line(
                        pane.top + ln,
                        pane.left + mark_line_start,
                        mark.hint,
                        ui.BLACK_ON_CYAN | ui.BOLD
                    )


def assign_hints(panes: List[Pane], filter: str) -> None:
    mark_number = 0
    for pane in reversed(panes):
        for mark in reversed(pane.marks):
            hint = number_to_hint(mark_number)

            if hint.startswith(filter):
                mark.hint = hint
            else:
                mark.hint = None

            mark_number += 1


def number_to_hint(number: int) -> str:
    prefix = int(number / 26)
    letter_number = number % 26
    letter = chr(97 + letter_number)

    if prefix > 0:
        return f'{prefix}{letter}'

    return letter


def main(stdscr: window) -> None:
    ui = UI(stdscr)

    panes: List[Pane] = Pane.get_current_window_panes()

    hint = ''
    while True:
        assign_hints(panes, hint)

        marks_left = flatten([
            [m for m in p.marks if m.hint] for p in panes
        ])

        if len(marks_left) == 1:
            chosen_mark = marks_left[0]
            chosen_mark.perform_primary_action()
            break

        for pane in panes:
            render_pane_text(ui, pane)
            overlay_marks(ui, pane)

        ui.refresh()

        char = ui.getch()

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


wrapper(main)
