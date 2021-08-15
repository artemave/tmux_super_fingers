import re
from typing import Pattern, Optional, Match

from .file_path_finder_base import FilePathFinderBase
from .finder import BaseFinder
from ..mark import Mark


class TextFilePathFinder(BaseFinder, FilePathFinderBase):
    """finds text files with line numbers (if any)"""

    @classmethod
    def pattern(cls) -> Pattern[str]:
        return re.compile(
            r'([~./]?[-a-zA-Z0-9_+-,./]+)(?::(\d+))?'
        )

    def match_to_mark(self, match: Match[str]) -> Optional[Mark]:
        start = match.span()[0]
        text = match.group(0)
        file_path = match.group(1)
        line_number = match.group(2)

        return self._match_to_mark(
            self.path_prefix,
            start,
            text,
            file_path,
            line_number
        )
