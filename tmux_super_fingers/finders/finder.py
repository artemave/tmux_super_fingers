import re
from functools import cached_property
from abc import ABCMeta, abstractmethod
from typing import Optional, Match, Pattern, List
from ..mark import Mark
from ..utils import compact

class BaseFinder(metaclass=ABCMeta):
    """Base finder class"""

    def __init__(self, text: str, path_prefix: str):
        self.text = text
        self.path_prefix = path_prefix

    @classmethod
    @abstractmethod
    def pattern(cls) -> Pattern:
        """regexp to find mark cadidate"""
        raise NotImplementedError

    @abstractmethod
    def match_to_mark(self, match: Match) -> Optional[Mark]:
        """additonal mark checks (e.g. file exists)"""
        raise NotImplementedError

    @cached_property
    def marks(self) -> List[Mark]:
        matches = re.finditer(self.pattern(), self.text)
        marks = compact(map(self.match_to_mark, matches))
        return marks
