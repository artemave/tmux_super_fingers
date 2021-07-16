#!/usr/bin/env python3

import sys
import os
import subprocess
import curses
from curses import wrapper
from curses import ascii
from typing import List, Any
from tmux_super_fingers.pane import Pane
from tmux_super_fingers.mark import Mark, UrlTarget, TextFileTarget
from tmux_super_fingers.utils import flatten

def shell(command):
    return subprocess.run(
        command.split(' '),
        stdout=subprocess.PIPE,
        check=True
    ).stdout.decode('utf-8').rstrip()

def strip(text):
    return '\n'.join(
        map(lambda line: line.rstrip(), text.split('\n'))
    )

def get_tmux_pane_cwd(pane_tty):
    pane_shell_pid = shell(f'ps -o pid= -t {pane_tty}').split("\n")[0].strip()
    return shell(f'readlink -e /proc/{pane_shell_pid}/cwd')

def get_panes() -> List[Pane]:
    panes_props = shell(
        'tmux list-panes -t ! -F #{pane_id},#{pane_tty},#{pane_left},#{pane_right},#{pane_top},#{pane_bottom},#{scroll_position}'
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

        marks_that_start_on_current_line = [
            m for m in pane.marks if line_end > m.start >= line_start
        ]

        if wrapped_mark_tail:
            marks_that_start_on_current_line = [wrapped_mark_tail] + marks_that_start_on_current_line

        for mark in marks_that_start_on_current_line:
            mark_line_start = mark.start - line_start
            mark_text = mark.mark_text

            if mark.end > line_end:
                tail_length = mark.end - line_end
                wrapped_mark_tail = Mark(
                    mark_text=mark_text[-tail_length:],
                    start=line_end,
                )
                mark_text = mark_text[:-tail_length]
            else:
                wrapped_mark_tail = None

            render_line(
                stdscr,
                pane.pane_top + ln,
                pane.pane_left + mark_line_start,
                mark_text,
                curses.A_BOLD
            )

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

is_macos: bool = 'darwin' in sys.platform.lower()

def perform_mark_action(mark: Mark):
    if isinstance(mark.target, UrlTarget):
        cmd = 'open' if is_macos else 'xdg-open'
        return shell(f'{cmd} {mark.target.url}')

    if isinstance(mark.target, TextFileTarget):
        window_names = shell('tmux list-windows -F #{window_name}').split('\n')
        vim_window_names = list(filter(lambda x: x == 'vim' or x == 'nvim', window_names))

        if len(vim_window_names) > 0:
            os.system('tmux select-window -t %s' %(vim_window_names[0]))
            vim_pane_id = shell('tmux list-panes -F "#{pane_id}" -t %s' %(vim_window_names[0])).split('\n')[0]
            os.system('tmux send-keys -t %s Escape' %(vim_pane_id))

            if mark.target.line_number:
                os.system('tmux send-keys -t %s ":e +%s %s" Enter zz' %(vim_pane_id, mark.target.line_number, mark.target.file_path))
            else:
                os.system('tmux send-keys -t %s ":e %s" Enter zz' %(vim_pane_id, mark.target.file_path))

            return

        raise Exception('Could not find "vim" or "nvim" window in the current session')

    raise Exception(f'Failed to perform_mark_action for {mark}')

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
            perform_mark_action(marks_left[0])
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
