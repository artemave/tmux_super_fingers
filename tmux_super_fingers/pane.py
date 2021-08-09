from __future__ import annotations  # https://stackoverflow.com/a/33533514/51209
from dataclasses import dataclass
from typing import List, Dict, Optional

from .finders import find_marks
from .mark import Mark


def _unique_sorted_marks(marks: List[Mark]) -> List[Mark]:
    index: Dict[str, Mark] = {}
    for mark in marks:
        index[mark.text] = mark

    return sorted(index.values(), key=lambda m: m.start)


@dataclass
class Pane:
    unwrapped_text: str
    text: str
    current_path: str
    left: int
    right: int
    top: int
    bottom: int
    _marks: Optional[List[Mark]] = None

    @property
    def marks(self) -> List[Mark]:
        if self._marks is None:
            pane_marks: List[Mark] = []
            path_prefix = self.current_path
            unwrapped_text = self.unwrapped_text
            running_character_total = 0

            for line in unwrapped_text.split('\n'):
                marks = find_marks(line, path_prefix)
                for mark in marks:
                    mark.start += running_character_total

                running_character_total += len(line)
                pane_marks += marks

            # Concurrent map is actually _slower_ than a regular map.
            #
            # with futures.ThreadPoolExecutor() as executor:
            #     marks = compact(executor.map(lambda m: find_match(m, text, path_prefix), matches))

            self._marks = _unique_sorted_marks(pane_marks)

        return self._marks

    @marks.setter
    def marks(self, marks: List[Mark]) -> None:
        self._marks = marks
