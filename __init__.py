# -*- coding: UTF-8 -*-

import sys
from functools import reduce
import operator
from pprint import pprint
import os
import re
import subprocess
from os.path import abspath
# from concurrent import futures
import curses
from curses import wrapper
from curses import ascii

PATTERN = re.compile(
    '(?P<rails_log_controller>(?:[A-Z]\\w*::)*[A-Z]\\w*Controller#\\w+)|'
    'Render(?:ed|ing) (?P<rails_log_partial>[-a-zA-Z0-9_+-,./]+)|'
    '(?P<url>(https?|tcp)://[-a-zA-Z0-9@:%._\\+~#=]{2,256}\\b([-a-zA-Z0-9@:%_\\+.~#?&/=]*))|'
    '\\+\\+\\+ b/?(?P<diff_path>([~./]?[-a-zA-Z0-9_+-,./]+(?::\\d+)?))|'
    '(?P<path>([~./]?[-a-zA-Z0-9_+-,./]+(?::\\d+)?))'
)

def compact(l):
    return [e for e in l if e]

def strip(text):
    return '\n'.join(
        map(lambda line: line.rstrip(), text.split('\n'))
    )

def shell(command):
    return subprocess.run(
        command.split(' '),
        stdout=subprocess.PIPE,
        check=True
    ).stdout.decode('utf-8').rstrip()

def camel_to_snake(string):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', string)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def get_tmux_pane_cwd(pane_tty):
    pane_shell_pid = shell(f'ps -o pid= -t {pane_tty}').split("\n")[0].strip()
    return shell(f'readlink -e /proc/{pane_shell_pid}/cwd')

def get_pane_data(pane_props):
    pane_id, pane_tty, pane_left, pane_right, pane_top, pane_bottom, scroll_position = pane_props.split(',')

    vertical_offset = 0
    if len(scroll_position) > 0:
        vertical_offset = int(scroll_position)

    pane_bottom = int(pane_bottom)
    start = -vertical_offset
    end = pane_bottom - vertical_offset

    return {
        'unwrapped_text': strip(shell(f'tmux capture-pane -p -S {start} -E {end} -J -t {pane_id}')),
        'text': strip(shell(f'tmux capture-pane -p -S {start} -E {end} -t {pane_id}')),
        'pane_current_path': get_tmux_pane_cwd(pane_tty),
        'pane_left': int(pane_left),
        'pane_right': int(pane_right),
        'pane_top': int(pane_top),
        'pane_bottom': pane_bottom,
    }

def get_panes():
    panes_props = shell(
        'tmux list-panes -t ! -F #{pane_id},#{pane_tty},#{pane_left},#{pane_right},#{pane_top},#{pane_bottom},#{scroll_position}'
    ).split('\n')
    return map(get_pane_data, panes_props)

def find_match(m, path_prefix):
    start, end = m.span()
    mark_text = m[0]

    path_match = m.groupdict()['path']
    diff_path_match = m.groupdict()['diff_path']
    url_match = m.groupdict()['url']
    rails_controller_match = m.groupdict()['rails_log_controller']
    rails_partial_match = m.groupdict()['rails_log_partial']

    mark_data = {}

    if path_match or diff_path_match:
        if diff_path_match:
            start, end = m.span('diff_path')
            mark_text = m.group('diff_path')

        parts = mark_text.rsplit(':', 1)
        file_path = parts[0]

        if file_path not in ('.', '..', '/'):
            file_path = abspath(os.path.join(
                path_prefix,
                os.path.expanduser(file_path)
            ))

            if os.path.isfile(file_path):
                mark_data = {'file_path': file_path}
                if len(parts) > 1:
                    mark_data['line_number'] = parts[1]

    elif rails_partial_match:
        start, end = m.span('rails_log_partial')
        mark_text = m.group('rails_log_partial')
        file_path = os.path.join(path_prefix, 'app/views/' + mark_text)

        if os.path.exists(file_path):
            mark_data = {
                'file_path': file_path
            }

    elif url_match:
        mark_data = {
            'url': mark_text.replace('tcp', 'http')
        }

    elif rails_controller_match:
        controller_class, action = mark_text.split('#')
        controller_path = 'app/controllers/' + '/'.join(
            map(camel_to_snake, controller_class.split('::'))
        ) + '.rb'
        controller_path = os.path.join(path_prefix, controller_path)

        method_def_regex = re.compile('^\\s*def\\s+%s' % (action))

        if os.path.exists(controller_path):
            mark_data = {'file_path': controller_path}

            with open(controller_path) as ruby_file:
                line_number = 0
                for line in ruby_file:
                    line_number += 1

                    if method_def_regex.match(line):
                        mark_data['line_number'] = line_number

    if mark_data:
        return {
            'start': int(start),
            'end': int(end),
            'mark_text': mark_text,
            'mark_data': mark_data
        }

def get_pane_marks(pane):
    pane['marks'] = []
    path_prefix = pane['pane_current_path']
    unwrapped_text = pane['unwrapped_text']
    running_total_of_chars = 0

    for line in unwrapped_text.split('\n'):
        matches = re.finditer(PATTERN, line)
        marks = compact(map(lambda m: find_match(m, path_prefix), matches))
        for mark in marks:
            mark['start'] += running_total_of_chars
            mark['end'] += running_total_of_chars

        running_total_of_chars += len(line)
        pane['marks'] += marks

    # Concurrent map is actually _slower_ than a regular map.
    #
    # with futures.ThreadPoolExecutor() as executor:
    #     marks = compact(executor.map(lambda m: find_match(m, text, path_prefix), matches))

    pane['marks'] = unique_marks(pane['marks'])

    return pane

def unique_marks(marks):
    index = {}
    for mark in marks:
        index[mark['mark_text']] = mark

    return sorted(index.values(), key=lambda m: m['start'])

def render_pane_text(stdscr, pane):
    if pane['pane_top'] > 0:
        pane_width = pane['pane_right'] - pane['pane_left'] + 1
        render_line(stdscr, pane['pane_top'] - 1, pane['pane_left'], '─' * pane_width)

    if pane['pane_left'] > 0:
        pane_height = pane['pane_bottom'] - pane['pane_top'] + 1
        for ln in range(pane_height):
            render_line(stdscr, pane['pane_top'] + ln, pane['pane_left'] - 1, '│', curses.A_DIM)

    lines = pane['text'].split('\n')
    for ln, line in enumerate(lines):
        render_line(stdscr, pane['pane_top'] + ln, pane['pane_left'], line, curses.A_DIM)

# Workaround for:
# https://stackoverflow.com/questions/7063128/last-character-of-a-window-in-python-curses
def render_line(stdscr, y, x, line, color):
    try:
        stdscr.addstr(y, x, line, color)
    except:
        stdscr.addstr(y, x, line[-1], color)
        stdscr.insstr(y, x, line[:-1], color)

def overlay_marks(stdscr, pane):
    running_total_of_chars = 0
    wrapped_mark_tail = None

    for ln, line in enumerate(pane['text'].split('\n')):
        line_start = running_total_of_chars
        running_total_of_chars += len(line)
        line_end = running_total_of_chars

        marks_that_start_on_current_line = [
            m for m in pane['marks'] if line_end > m['start'] >= line_start
        ]

        if wrapped_mark_tail:
            marks_that_start_on_current_line = [wrapped_mark_tail] + marks_that_start_on_current_line

        for mark in marks_that_start_on_current_line:
            mark_line_start = mark['start'] - line_start
            mark_text = mark['mark_text']

            if mark['end'] > line_end:
                tail_length = mark['end'] - line_end
                wrapped_mark_tail = {
                    'mark_text': mark_text[-tail_length:],
                    'start': line_end,
                    'end': mark['end']
                }
                mark_text = mark_text[:-tail_length]
            else:
                wrapped_mark_tail = None

            render_line(
                stdscr,
                pane['pane_top'] + ln,
                pane['pane_left'] + mark_line_start,
                mark_text,
                curses.A_BOLD
            )

            if 'hint' in mark:
                render_line(
                    stdscr,
                    pane['pane_top'] + ln,
                    pane['pane_left'] + mark_line_start,
                    mark['hint'],
                    curses.color_pair(1) | curses.A_BOLD
                )

def assign_hints(panes, filter):
    mark_number = 0
    for pane in reversed(panes):
        for mark in reversed(pane['marks']):
            hint = number_to_hint(mark_number)

            if hint.startswith(filter):
                mark['hint'] = hint
            else:
                mark.pop('hint', None)

            mark_number += 1

def number_to_hint(number):
    prefix = int(number / 26)
    letter_number = number % 26
    letter = chr(97 + letter_number)

    if prefix > 0:
        return f'{prefix}{letter}'

    return letter

def flatten(list):
    return sum(list, [])

is_macos: bool = 'darwin' in sys.platform.lower()

def perform_mark_action(mark):
    mark_data = mark['mark_data']

    if 'url' in mark_data:
        cmd = 'open' if is_macos else 'xdg-open'
        return shell(f'{cmd} {mark_data["url"]}')

    if 'file_path' in mark_data:
        window_names = shell('tmux list-windows -F #{window_name}').split('\n')
        vim_window_names = list(filter(lambda x: x == 'vim' or x == 'nvim', window_names))

        if len(vim_window_names) > 0:
            os.system('tmux select-window -t %s' %(vim_window_names[0]))
            vim_pane_id = shell('tmux list-panes -F "#{pane_id}" -t %s' %(vim_window_names[0])).split('\n')[0]
            os.system('tmux send-keys -t %s Escape' %(vim_pane_id))

            if 'line_number' in mark_data:
                os.system('tmux send-keys -t %s ":e +%s %s" Enter zz' %(vim_pane_id, mark_data['line_number'], mark_data['file_path']))
            else:
                os.system('tmux send-keys -t %s ":e %s" Enter zz' %(vim_pane_id, mark_data['file_path']))

            return
        else:
            raise Exception('Could not find "vim" or "nvim" window in the current session')

    raise Exception(f'Failed to perform_mark_action for {mark}')

def main(stdscr):
    panes = list(map(get_pane_marks, get_panes()))

    # To inherit window background
    curses.use_default_colors()
    curses.curs_set(False)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_CYAN)

    hint = ''
    while True:
        assign_hints(panes, hint)

        marks_left = [
            [m for m in p['marks'] if 'hint' in m] for p in panes
        ]
        marks_left = flatten(marks_left)

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

if __name__ == "__main__":
    os.environ.setdefault('ESCDELAY', '25')
    wrapper(main)
    # panes = list(map(get_pane_marks, get_panes()))
    # print({'panes': panes})
