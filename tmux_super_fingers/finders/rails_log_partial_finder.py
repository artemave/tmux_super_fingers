import re
import os
from typing import Optional, Pattern, Match
from ..mark import Mark, TextFileTarget
from ..utils import camel_to_snake
from .finder import BaseFinder

class RailsLogPartialFinder(BaseFinder):
    """
    From a text that looks like this:
        Rendered layouts/_base.html.erb (Duration: 32.9ms | Allocations: 2204)

    this finder extracts file path of a rails controller (with line number pointing to action method).
    """

    @classmethod
    def pattern(cls) -> Pattern:
        return re.compile(
            r'Render(?:ed|ing) ([-a-zA-Z0-9_+-,./]+)'
        )

    def match_to_mark(self, match: Match) -> Optional[Mark]:
        start, end = match.span(1)
        text = match.group(1)
        file_path = os.path.join(self.path_prefix, 'app/views/' + text)

        if os.path.exists(file_path):
            return Mark(
                start=start,
                text=text,
                target=TextFileTarget(file_path)
            )

        return None
