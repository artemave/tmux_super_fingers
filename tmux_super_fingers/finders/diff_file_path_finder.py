import re
from os import path
from .finder import BaseFinder
from typing import Optional, Pattern, Match
from ..mark import Mark, TextFileTarget

class DiffFilePathFinder(BaseFinder):
    """
    Finds file path from text like this:

        +++ b/app/controllers/orders_controller.rb
    """

    @classmethod
    def pattern(cls) -> Pattern:
        return re.compile(
            r'\+\+\+ b/?(([~./]?[-a-zA-Z0-9_+-,./]+)(?::(\d+))?)'
        )

    def match_to_mark(self, match: Match) -> Optional[Mark]:
        start, end = match.span(1)
        mark_text = match.group(1)
        file_path = match.group(2)
        line_number = match.group(3)

        if file_path not in ('.', '..', '/'):
            file_path = path.abspath(path.join(
                self.path_prefix,
                path.expanduser(file_path)
            ))

            if path.isfile(file_path):
                mark_target = TextFileTarget(file_path)
                if line_number:
                    mark_target.line_number = int(line_number)

                return Mark(
                    start=start,
                    end=end,
                    mark_text=mark_text,
                    target=mark_target
                )

        return None
