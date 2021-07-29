import re
from .finder import BaseFinder
from typing import Optional, Pattern, Match
from ..mark import Mark
from ..targets import UrlTarget


class UrlFinder(BaseFinder):
    """url finder"""

    @classmethod
    def pattern(cls) -> Pattern[str]:
        return re.compile(
            r'(?:https?|tcp)://[-a-zA-Z0-9@:%._\+~#=]{2,256}\b[-a-zA-Z0-9@:%_\+.~#?&/=]*'
        )

    def match_to_mark(self, match: Match[str]) -> Optional[Mark]:
        start = match.span()[0]
        text = match.group(0)

        return Mark(
            start=start,
            text=text,
            target=UrlTarget(text.replace('tcp', 'http'))
        )
