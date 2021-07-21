#!/usr/bin/env python3

import curses
import os
from curses import ascii, wrapper
from typing import List

from tmux_super_fingers.mark import Highlight, Mark
from tmux_super_fingers.pane import Pane
from tmux_super_fingers.utils import flatten, shell, strip


def get_tmux_pane_cwd(pane_tty):
    pane_shell_pid = shell(f'ps -o pid= -t {pane_tty}').split("\n")[0].strip()
    return shell(f'lsof -a -p {pane_shell_pid} -d cwd -Fn').split('\n')[-1][1:]


def get_panes() -> List[Pane]:
    panes_props = shell(
        'tmux list-panes -t ! -F #{pane_id},#{pane_tty},#{pane_left},'
        '#{pane_right},#{pane_top},#{pane_bottom},#{scroll_position}'
    ).split('\n')

    panes = map(create_pane, panes_props)

    return list(panes)


def render_pane_text(stdscr, pane: Pane):
    if pane.pane_top > 0:
        pane_width = pane.pane_right - pane.pane_left + 1
        render_line(stdscr, pane.pane_top - 1, pane.pane_left, '─' * pane_width, curses.A_DIM)

    if pane.pane_left > 0:
        pane_height = pane.pane_bottom - pane.pane_top + 1
        for ln in range(pane_height):
            render_line(stdscr, pane.pane_top + ln, pane.pane_left - 1, '│', curses.A_DIM)

    lines = pane.text.split('\n')
    for ln, line in enumerate(lines):
        render_line(stdscr, pane.pane_top + ln, pane.pane_left, line, curses.A_DIM)

# Workaround for:
# https://stackoverflow.com/questions/7063128/last-character-of-a-window-in-python-curses


def render_line(stdscr, y, x, line, color):
    try:
        stdscr.addstr(y, x, line, color)
    except curses.error:
        stdscr.addstr(y, x, line[-1], color)
        stdscr.insstr(y, x, line[:-1], color)


def overlay_marks(stdscr, pane: Pane):
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

            render_line(
                stdscr,
                pane.pane_top + ln,
                pane.pane_left + mark_line_start,
                text,
                curses.A_BOLD
            )

            if isinstance(highlight, Mark):
                mark = highlight
                if mark.hint:
                    render_line(
                        stdscr,
                        pane.pane_top + ln,
                        pane.pane_left + mark_line_start,
                        mark.hint,
                        curses.color_pair(1) | curses.A_BOLD
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


def number_to_hint(number):
    prefix = int(number / 26)
    letter_number = number % 26
    letter = chr(97 + letter_number)

    if prefix > 0:
        return f'{prefix}{letter}'

    return letter


def create_pane(pane_props) -> Pane:
    pane_id, pane_tty, pane_left, pane_right, pane_top, pane_bottom, scroll_position = pane_props.split(',')

    vertical_offset = 0
    if len(scroll_position) > 0:
        vertical_offset = int(scroll_position)

    pane_bottom = int(pane_bottom)
    start = -vertical_offset
    end = pane_bottom - vertical_offset

    return Pane(
        unwrapped_text=strip(shell(f'tmux capture-pane -p -S {start} -E {end} -J -t {pane_id}')),
        text=strip(shell(f'tmux capture-pane -p -S {start} -E {end} -t {pane_id}')),
        pane_current_path=get_tmux_pane_cwd(pane_tty),
        pane_left=int(pane_left),
        pane_right=int(pane_right),
        pane_top=int(pane_top),
        pane_bottom=pane_bottom,
    )


def main(stdscr) -> None:
    # To inherit window background
    curses.use_default_colors()
    curses.curs_set(False)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_CYAN)

    panes = get_panes()

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
            render_pane_text(stdscr, pane)
            overlay_marks(stdscr, pane)

        stdscr.refresh()

        char = stdscr.getch()

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


os.environ.setdefault('ESCDELAY', '25')
wrapper(main)
# panes = list(map(get_pane_marks, get_panes()))
# print({'panes': panes})
