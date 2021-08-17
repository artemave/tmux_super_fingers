from dataclasses import dataclass
from typing import Optional

from .target_payload import TargetPaylod


@dataclass
class EditorOpenable(TargetPaylod):
    """ Anything that can be sent to vim """

    file_path: str
    line_number: Optional[int] = None
