from typing import List, Type
from ..mark import Mark
from ..utils import flatten
from .rails_log_controller_finder import RailsLogControllerFinder
from .rails_log_partial_finder import RailsLogPartialFinder
from .url_finder import UrlFinder
from .text_file_path_finder import TextFilePathFinder
from .diff_file_path_finder import DiffFilePathFinder
from .finder import BaseFinder
# import image_file_path_finder


class MarkFinder:
    """Finds marks using different finders"""

    FINDERS: List[Type[BaseFinder]] = [
        RailsLogControllerFinder,
        UrlFinder,
        TextFilePathFinder,
        RailsLogPartialFinder,
        DiffFilePathFinder
    ]

    def __init__(self, *, finders: List[Type[BaseFinder]] = FINDERS):
        self.finders = finders

    def find_marks(self, text: str, path_prefix: str) -> List[Mark]:
        all_marks = flatten(
            list(map(
                lambda finder_class: finder_class(text, path_prefix).marks,
                self.finders
            ))
        )
        return _remove_overlapping_marks(all_marks)


# TODO: implement this
def _remove_overlapping_marks(marks: List[Mark]) -> List[Mark]:
    return marks
