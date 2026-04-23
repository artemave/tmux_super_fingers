import re
from typing import Pattern, Optional, Match

from .file_path_finder_base import FilePathFinderBase
from .finder import BaseFinder
from ..mark import Mark


class FilePathFinder(BaseFinder, FilePathFinderBase):
    """finds text files with line numbers (if any)"""

    @classmethod
    def pattern(cls) -> Pattern[str]:
        return re.compile(
            r'(?:\w+\()?'
            r'(([~./]?[-a-zA-Z0-9_./]'
            r'[-a-zA-Z0-9_+-,./@\[\]$]*'
            r'(?:\([-a-zA-Z0-9_+-,./@\[\]$]*\)[-a-zA-Z0-9_+-,./@\[\]$]*)*)'
            r'(?:(?::|", line )(\d+))?)\)?'
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
