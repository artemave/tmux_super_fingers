from dataclasses import dataclass
from typing import Optional

from .target import Target


@dataclass
class EditorOpenable(Target):
    """ Anything that can be sent to vim """

    file_path: str
    line_number: Optional[int] = None
