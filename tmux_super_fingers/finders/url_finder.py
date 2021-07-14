import re
from .finder import BaseFinder
from typing import Optional, Pattern, Match
from ..mark import Mark, UrlTarget

class UrlFinder(BaseFinder):
    """url finder"""

    @classmethod
    def pattern(cls) -> Pattern:
        return re.compile(
            r'(?:https?|tcp)://[-a-zA-Z0-9@:%._\+~#=]{2,256}\b[-a-zA-Z0-9@:%_\+.~#?&/=]*'
        )

    def match_to_mark(self, match: Match) -> Optional[Mark]:
        start, end = match.span()
        mark_text = match.group(0)

        return Mark(
            start=start,
            end=end,
            mark_text=mark_text,
            target=UrlTarget(mark_text.replace('tcp', 'http'))
        )
