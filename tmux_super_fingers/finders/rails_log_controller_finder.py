import re
import os
from typing import Optional, Pattern, Match
from ..mark import Mark
from ..targets.file_target import FileTarget, ContentType
from ..utils import camel_to_snake
from .finder import BaseFinder


class RailsLogControllerFinder(BaseFinder):
    """
    From a text that looks like this `Processing by OrdersController#show as HTML` this finder
    extracts file path of a rails controller (with line number pointing to action method)
    """

    @classmethod
    def pattern(cls) -> Pattern[str]:
        return re.compile(r'(?:[A-Z]\w*::)*[A-Z]\w*Controller#\w+')

    def match_to_mark(self, match: Match[str]) -> Optional[Mark]:
        start = match.span()[0]
        text = match.group(0)

        controller_class, action = text.split('#')
        controller_path = 'app/controllers/' + '/'.join(
            map(camel_to_snake, controller_class.split('::'))
        ) + '.rb'
        controller_path = os.path.join(self.path_prefix, controller_path)

        method_def_regex = re.compile('^\\s*def\\s+%s' % (action))

        if os.path.exists(controller_path):
            mark_target = FileTarget(controller_path, ContentType.TEXT)

            with open(controller_path) as ruby_file:
                line_number = 0
                for line in ruby_file:
                    line_number += 1

                    if method_def_regex.match(line):
                        mark_target.line_number = line_number

            return Mark(
                start=start,
                text=text,
                target=mark_target
            )

        return None
