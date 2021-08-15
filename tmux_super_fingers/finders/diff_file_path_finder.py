import re
from typing import Pattern, Optional, Match

from .file_path_finder_base import FilePathFinderBase
from .finder import BaseFinder
from ..mark import Mark


class DiffFilePathFinder(BaseFinder, FilePathFinderBase):
    """
    Finds file path from text like this:

        +++ b/app/controllers/orders_controller.rb
    """

    @classmethod
    def pattern(cls) -> Pattern[str]:
        return re.compile(
            r'\+\+\+ b/?(([~./]?[-a-zA-Z0-9_+-,./]+)(?::(\d+))?)'
        )

    def match_to_mark(self, match: Match[str]) -> Optional[Mark]:
        start = match.span(1)[0]
        text = match.group(1)
        file_path = match.group(2)
        line_number = match.group(3)

        return self._match_to_mark(
            self.path_prefix,
            start,
            text,
            file_path,
            line_number
        )
