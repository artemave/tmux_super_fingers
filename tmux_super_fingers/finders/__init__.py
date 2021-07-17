import re
from typing import List
from ..mark import Mark
from ..utils import flatten
from .rails_log_controller_finder import RailsLogControllerFinder
from .rails_log_partial_finder import RailsLogPartialFinder
from .url_finder import UrlFinder
from .text_file_path_finder import TextFilePathFinder
from .diff_file_path_finder import DiffFilePathFinder
# import image_file_path_finder

PATTERN = re.compile(
    'Render(?:ed|ing) (?P<rails_log_partial>[-a-zA-Z0-9_+-,./]+)|'
    '\\+\\+\\+ b/?(?P<diff_path>([~./]?[-a-zA-Z0-9_+-,./]+(?::\\d+)?))|'
)

FINDERS = [
    RailsLogControllerFinder,
    UrlFinder,
    TextFilePathFinder,
    RailsLogPartialFinder,
    DiffFilePathFinder
]


def find_marks(text: str, path_prefix: str) -> List[Mark]:
    all_marks = flatten(
        list(map(
            lambda finder_class: finder_class(text, path_prefix).marks,
            FINDERS
        ))
    )
    return _remove_overlapping_marks(all_marks)

# TODO: implement this


def _remove_overlapping_marks(marks: List[Mark]) -> List[Mark]:
    return marks
