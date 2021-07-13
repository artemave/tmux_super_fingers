import re
from typing import Optional, List
import os
from os.path import abspath
from functools import cached_property
from dataclasses import dataclass
from .mark import MarkTarget, Mark, UrlTarget, TextFileTarget

PATTERN = re.compile(
    '(?P<rails_log_controller>(?:[A-Z]\\w*::)*[A-Z]\\w*Controller#\\w+)|'
    'Render(?:ed|ing) (?P<rails_log_partial>[-a-zA-Z0-9_+-,./]+)|'
    '(?P<url>(https?|tcp)://[-a-zA-Z0-9@:%._\\+~#=]{2,256}\\b([-a-zA-Z0-9@:%_\\+.~#?&/=]*))|'
    '\\+\\+\\+ b/?(?P<diff_path>([~./]?[-a-zA-Z0-9_+-,./]+(?::\\d+)?))|'
    '(?P<path>([~./]?[-a-zA-Z0-9_+-,./]+(?::\\d+)?))'
)

@dataclass
class Pane:
    unwrapped_text: str
    text: str
    pane_current_path: str
    pane_left: int
    pane_right: int
    pane_top: int
    pane_bottom: int

    @cached_property
    def marks(self) -> List[Mark]:
        pane_marks: List[Mark] = []
        path_prefix = self.pane_current_path
        unwrapped_text = self.unwrapped_text
        running_character_total = 0

        for line in unwrapped_text.split('\n'):
            matches = re.finditer(PATTERN, line)
            marks = compact(map(lambda m: find_match(m, path_prefix), matches))
            for mark in marks:
                mark.start += running_character_total
                mark.end += running_character_total

            running_character_total += len(line)
            pane_marks += marks

        # Concurrent map is actually _slower_ than a regular map.
        #
        # with futures.ThreadPoolExecutor() as executor:
        #     marks = compact(executor.map(lambda m: find_match(m, text, path_prefix), matches))

        return unique_sorted_marks(pane_marks)

def find_match(m, path_prefix) -> Optional[Mark]:
    start, end = m.span()
    mark_text = m[0]

    path_match = m.groupdict()['path']
    diff_path_match = m.groupdict()['diff_path']
    url_match = m.groupdict()['url']
    rails_controller_match = m.groupdict()['rails_log_controller']
    rails_partial_match = m.groupdict()['rails_log_partial']

    def create_mark(target: MarkTarget) -> Mark:
        return Mark(
            start=start,
            end=end,
            mark_text=mark_text,
            target=target
        )

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
                mark_target = TextFileTarget(file_path)
                if len(parts) > 1:
                    mark_target.line_number = int(parts[1])

                return create_mark(mark_target)

    elif rails_partial_match:
        start, end = m.span('rails_log_partial')
        mark_text = m.group('rails_log_partial')
        file_path = os.path.join(path_prefix, 'app/views/' + mark_text)

        if os.path.exists(file_path):
            return create_mark(TextFileTarget(file_path))

    elif url_match:
        return create_mark(UrlTarget(mark_text.replace('tcp', 'http')))

    elif rails_controller_match:
        controller_class, action = mark_text.split('#')
        controller_path = 'app/controllers/' + '/'.join(
            map(camel_to_snake, controller_class.split('::'))
        ) + '.rb'
        controller_path = os.path.join(path_prefix, controller_path)

        method_def_regex = re.compile('^\\s*def\\s+%s' % (action))

        if os.path.exists(controller_path):
            mark_target = TextFileTarget(controller_path)

            with open(controller_path) as ruby_file:
                line_number = 0
                for line in ruby_file:
                    line_number += 1

                    if method_def_regex.match(line):
                        mark_target.line_number = line_number

            return create_mark(mark_target)

    return None

def unique_sorted_marks(marks: List[Mark]) -> List[Mark]:
    index = {}
    for mark in marks:
        index[mark.mark_text] = mark

    return sorted(index.values(), key=lambda m: m.start)

def compact(l):
    return [e for e in l if e]

def camel_to_snake(string):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', string)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
