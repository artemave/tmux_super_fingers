from __future__ import annotations  # https://stackoverflow.com/a/33533514/51209
from dataclasses import dataclass
from typing import List

from .mark import Mark
from .finders import MarkFinder


@dataclass
class Pane:
    unwrapped_text: str
    text: str
    current_path: str
    left: int
    right: int
    top: int
    bottom: int
    mark_finder: MarkFinder

    @property
    def marks(self) -> List[Mark]:
        if not hasattr(self, '_marks'):
            pane_marks: List[Mark] = []
            path_prefix = self.current_path
            unwrapped_text = self.unwrapped_text
            running_character_total = 0

            for line in unwrapped_text.split('\n'):
                marks = self.mark_finder.find_marks(line, path_prefix)
                for mark in marks:
                    mark.start += running_character_total

                running_character_total += len(line)
                pane_marks += marks

            # Concurrent map is actually _slower_ than a regular map.
            #
            # with futures.ThreadPoolExecutor() as executor:
            #     marks = compact(executor.map(lambda m: find_match(m, text, path_prefix), matches))

            self._marks = pane_marks

        return self._marks

    @marks.setter
    def marks(self, marks: List[Mark]) -> None:
        self._marks = marks
